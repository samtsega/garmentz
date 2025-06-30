import React, { Component } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  StatusBar,
  Image,
  Alert,
  ActivityIndicator,
  Platform,
  Dimensions,
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system';
import { CameraView, useCameraPermissions, useMicrophonePermissions } from 'expo-camera';

const { width, height } = Dimensions.get('window');

class CameraScreen extends Component {
  state = {
    capturedUri: null,
    isUploading: false,
    isAnalyzing: false,
    hasCameraPermission: null,
    hasGalleryPermission: null,
    isLoading: true,
    isBackendConnected: false,
    isCameraReady: false,
    facing: 'back',
  };

  cameraRef = null;

  // Use environment variable or config for backend URL
  BACKEND_URL = __DEV__
    ? process.env.EXPO_PUBLIC_BACKEND_URL || 'http://192.168.1.153:5050'
    : process.env.EXPO_PUBLIC_PRODUCTION_BACKEND_URL || 'https://your-production-backend.com';

  async componentDidMount() {
    await this.requestPermissions();
    await this.checkBackendConnection();
  }

  componentWillUnmount() {
    // Clean up any pending requests or timers
    this.setState = () => {}; // Prevent setState on unmounted component
  }

  requestPermissions = async () => {
    this.setState({ isLoading: true });
    try {
      // Request camera permissions using new API
      const cameraPermission = await ImagePicker.requestCameraPermissionsAsync();
      
      // Request media library permissions  
      const mediaPermission = await ImagePicker.requestMediaLibraryPermissionsAsync();

      this.setState({
        hasCameraPermission: cameraPermission.status === 'granted',
        hasGalleryPermission: mediaPermission.status === 'granted',
        isLoading: false,
      });

      if (cameraPermission.status !== 'granted' || mediaPermission.status !== 'granted') {
        Alert.alert(
          'Permissions Required',
          'Camera and media library permissions are required for this app to function properly.',
          [
            { text: 'Settings', onPress: () => this.openAppSettings() },
            { text: 'Retry', onPress: this.requestPermissions },
          ]
        );
      }
    } catch (error) {
      console.error('Permission error:', error);
      this.setState({ isLoading: false });
      Alert.alert('Permission Error', 'Failed to request permissions. Please try again.');
    }
  };

  openAppSettings = () => {
    if (Platform.OS === 'ios') {
      Linking.openURL('app-settings:');
    } else {
      Linking.openSettings();
    }
  };

  checkBackendConnection = async () => {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout

      const response = await fetch(`${this.BACKEND_URL}/health`, {
        method: 'GET',
        signal: controller.signal,
        headers: {
          'Accept': 'application/json',
        },
      });

      clearTimeout(timeoutId);
      this.setState({ isBackendConnected: response.ok });
    } catch (error) {
      console.error('Backend connection error:', error);
      this.setState({ isBackendConnected: false });
    }
  };

  onCameraReady = () => {
    this.setState({ isCameraReady: true });
  };

  takePicture = async () => {
    if (this.cameraRef && this.state.isCameraReady) {
      try {
        const photo = await this.cameraRef.takePictureAsync({
          quality: 0.8,
          base64: false,
          skipProcessing: false,
        });
        
        if (photo && photo.uri) {
          this.setState({ capturedUri: photo.uri });
        } else {
          throw new Error('Failed to capture image');
        }
      } catch (error) {
        console.error('Take picture error:', error);
        Alert.alert('Error', 'Failed to take picture. Please try again.');
      }
    } else {
      Alert.alert('Camera not ready', 'Please wait for the camera to initialize.');
    }
  };

  pickImage = async () => {
    try {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        quality: 0.8,
        aspect: [16, 9],
      });

      if (!result.canceled && result.assets && result.assets[0]) {
        this.setState({ capturedUri: result.assets[0].uri });
      }
    } catch (error) {
      console.error('Pick image error:', error);
      Alert.alert('Error', 'Failed to pick image. Please try again.');
    }
  };

  validateImageUri = async (uri) => {
    try {
      const fileInfo = await FileSystem.getInfoAsync(uri);
      return fileInfo.exists && fileInfo.size > 0;
    } catch (error) {
      console.error('Image validation error:', error);
      return false;
    }
  };

  calculateDepreciation = async () => {
    const { capturedUri } = this.state;
    
    if (!capturedUri) {
      Alert.alert('No Image', 'Please take or upload an image first.');
      return;
    }

    if (!this.state.isBackendConnected) {
      Alert.alert(
        'Backend Offline', 
        'Cannot connect to the backend server. Please check your internet connection and try again.',
        [
          { text: 'Retry Connection', onPress: this.checkBackendConnection },
          { text: 'OK' },
        ]
      );
      return;
    }

    // Validate image exists and is readable
    const isValidImage = await this.validateImageUri(capturedUri);
    if (!isValidImage) {
      Alert.alert('Invalid Image', 'The selected image is corrupted or inaccessible. Please try again.');
      return;
    }

    this.setState({ isAnalyzing: true });

    try {
      const base64 = await FileSystem.readAsStringAsync(capturedUri, {
        encoding: FileSystem.EncodingType.Base64,
      });

      if (!base64) {
        throw new Error('Failed to encode image');
      }

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

      const response = await fetch(`${this.BACKEND_URL}/depreciation`, {
        method: 'POST',
        signal: controller.signal,
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          image_data: base64,
          platform: Platform.OS,
          timestamp: new Date().toISOString(),
          image_size: base64.length,
        }),
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server error ${response.status}: ${errorText || 'Unknown error'}`);
      }

      const result = await response.json();

      if (result.error) {
        throw new Error(result.error);
      }

      // Validate response data
      const score = result.depreciation_score || 'N/A';
      const value = result.estimated_value || 'N/A';

      Alert.alert(
        'Depreciation Analysis Complete',
        `Depreciation Score: ${score}\nEstimated Value: ${typeof value === 'number' ? `$${value.toFixed(2)}` : value}`,
        [
          { text: 'Take Another Photo', onPress: this.resetCapture },
          { text: 'OK' },
        ]
      );
    } catch (error) {
      console.error('Depreciation calculation error:', error);
      
      let errorMessage = 'Failed to calculate depreciation. ';
      if (error.name === 'AbortError') {
        errorMessage += 'Request timed out.';
      } else if (error.message.includes('Network')) {
        errorMessage += 'Network error occurred.';
      } else {
        errorMessage += error.message;
      }

      Alert.alert('Analysis Error', errorMessage);
    } finally {
      this.setState({ isAnalyzing: false });
    }
  };

  resetCapture = () => {
    this.setState({ capturedUri: null });
  };

  toggleCameraFacing = () => {
    this.setState(prevState => ({
      facing: prevState.facing === 'back' ? 'front' : 'back'
    }));
  };

  render() {
    const {
      isLoading,
      hasCameraPermission,
      hasGalleryPermission,
      capturedUri,
      isAnalyzing,
      isBackendConnected,
      isCameraReady,
      facing,
    } = this.state;

    if (isLoading) {
      return (
        <SafeAreaView style={styles.container}>
          <StatusBar barStyle="light-content" backgroundColor="#000" />
          <View style={styles.center}>
            <ActivityIndicator size="large" color="#fff" />
            <Text style={styles.loadingText}>Loading permissions...</Text>
          </View>
        </SafeAreaView>
      );
    }

    if (!hasCameraPermission || !hasGalleryPermission) {
      return (
        <SafeAreaView style={styles.container}>
          <StatusBar barStyle="light-content" backgroundColor="#000" />
          <View style={styles.center}>
            <Text style={styles.errorText}>Permissions Required</Text>
            <Text style={styles.subText}>
              {!hasCameraPermission && 'Camera permission is required. '}
              {!hasGalleryPermission && 'Media library permission is required. '}
              Please grant permissions to continue.
            </Text>
            <TouchableOpacity
              style={styles.button}
              onPress={this.requestPermissions}
            >
              <Text style={styles.buttonText}>Grant Permissions</Text>
            </TouchableOpacity>
          </View>
        </SafeAreaView>
      );
    }

    return (
      <SafeAreaView style={styles.container}>
        <StatusBar barStyle="light-content" backgroundColor="#000" />

        <View style={styles.cameraContainer}>
          <CameraView
            style={styles.camera}
            facing={facing}
            ref={(ref) => (this.cameraRef = ref)}
            onCameraReady={this.onCameraReady}
          >
            <View style={styles.cameraOverlay}>
              <TouchableOpacity
                style={styles.flipButton}
                onPress={this.toggleCameraFacing}
              >
                <Text style={styles.flipButtonText}>🔄</Text>
              </TouchableOpacity>
            </View>
          </CameraView>
        </View>

        <View style={styles.content}>
          {capturedUri && (
            <View style={styles.previewContainer}>
              <Image source={{ uri: capturedUri }} style={styles.preview} />
              <TouchableOpacity
                style={styles.resetButton}
                onPress={this.resetCapture}
              >
                <Text style={styles.resetButtonText}>✕</Text>
              </TouchableOpacity>
            </View>
          )}

          <TouchableOpacity
            style={[
              styles.primaryButton,
              !isCameraReady && styles.disabledButton,
            ]}
            onPress={this.takePicture}
            disabled={!isCameraReady}
          >
            <Text style={styles.primaryButtonText}>
              {!isCameraReady ? '⏳ CAMERA LOADING...' : '📷 TAKE PICTURE'}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity 
            style={styles.secondaryButton} 
            onPress={this.pickImage}
          >
            <Text style={styles.secondaryButtonText}>🖼️ UPLOAD IMAGE</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.primaryButton,
              (!capturedUri || isAnalyzing || !isBackendConnected) && styles.disabledButton,
            ]}
            onPress={this.calculateDepreciation}
            disabled={!capturedUri || isAnalyzing || !isBackendConnected}
          >
            <Text style={styles.primaryButtonText}>
              {isAnalyzing ? '⏳ ANALYZING...' : '🧮 CALCULATE DEPRECIATION'}
            </Text>
          </TouchableOpacity>

          <View style={styles.statusContainer}>
            <Text style={styles.statusText}>
              {isBackendConnected ? '🟢 Backend Connected' : '🔴 Backend Offline'}
            </Text>
            <TouchableOpacity
              style={styles.refreshButton}
              onPress={this.checkBackendConnection}
            >
              <Text style={styles.refreshButtonText}>Refresh</Text>
            </TouchableOpacity>
          </View>
        </View>
      </SafeAreaView>
    );
  }
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    backgroundColor: '#000' 
  },
  cameraContainer: {
    flex: 3,
    width: '100%',
    borderWidth: 2,
    borderColor: '#fff',
    position: 'relative',
  },
  camera: {
    flex: 1,
  },
  cameraOverlay: {
    position: 'absolute',
    top: 10,
    right: 10,
  },
  flipButton: {
    backgroundColor: 'rgba(0,0,0,0.5)',
    borderRadius: 25,
    width: 50,
    height: 50,
    justifyContent: 'center',
    alignItems: 'center',
  },
  flipButtonText: {
    fontSize: 20,
  },
  content: {
    flex: 4,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  previewContainer: {
    position: 'relative',
    width: '90%',
    marginBottom: 20,
  },
  preview: {
    width: '100%',
    height: 200,
    borderWidth: 2,
    borderColor: '#fff',
    resizeMode: 'cover',
    borderRadius: 5,
  },
  resetButton: {
    position: 'absolute',
    top: -10,
    right: -10,
    backgroundColor: '#ff4444',
    borderRadius: 15,
    width: 30,
    height: 30,
    justifyContent: 'center',
    alignItems: 'center',
  },
  resetButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  primaryButton: {
    backgroundColor: '#fff',
    paddingVertical: 15,
    paddingHorizontal: 30,
    marginBottom: 15,
    width: '80%',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#fff',
    borderRadius: 8,
  },
  primaryButtonText: {
    fontSize: 16,
    color: '#000',
    letterSpacing: 1,
    fontWeight: 'bold',
  },
  secondaryButton: {
    backgroundColor: 'transparent',
    paddingVertical: 15,
    paddingHorizontal: 30,
    marginBottom: 15,
    width: '80%',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#fff',
    borderRadius: 8,
  },
  secondaryButtonText: {
    fontSize: 16,
    color: '#fff',
    letterSpacing: 1,
    fontWeight: 'bold',
  },
  disabledButton: { 
    opacity: 0.5 
  },
  center: { 
    flex: 1, 
    justifyContent: 'center', 
    alignItems: 'center',
    padding: 20,
  },
  loadingText: { 
    color: '#fff', 
    marginTop: 10,
    textAlign: 'center',
  },
  errorText: { 
    color: '#fff', 
    fontSize: 18, 
    marginBottom: 10,
    textAlign: 'center',
    fontWeight: 'bold',
  },
  subText: {
    color: '#ccc',
    fontSize: 14,
    marginBottom: 20,
    textAlign: 'center',
    paddingHorizontal: 20,
    lineHeight: 20,
  },
  button: {
    borderWidth: 2,
    borderColor: '#fff',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    marginBottom: 10,
  },
  buttonText: { 
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  statusContainer: { 
    marginTop: 20,
    alignItems: 'center',
  },
  statusText: { 
    color: '#fff', 
    fontSize: 14,
    textAlign: 'center',
    marginBottom: 5,
  },
  refreshButton: {
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderWidth: 1,
    borderColor: '#fff',
    borderRadius: 4,
  },
  refreshButtonText: {
    color: '#fff',
    fontSize: 12,
  },
});

export default CameraScreen;

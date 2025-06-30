export async function calculateDepreciation(data) {
  try {
    const response = await fetch('http://192.168.1.153:5000/depreciation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const result = await response.json();
    return result.depreciation_score;
  } catch (error) {
    console.error('Error calculating depreciation:', error);
    throw error;
  }
}

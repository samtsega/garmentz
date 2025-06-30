import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import { ComponentProps } from 'react';
import { OpaqueColorValue, StyleProp, TextStyle } from 'react-native';

type IconMapping = Record<string, ComponentProps<typeof MaterialIcons>['name']>;

/**
 * Map SF Symbols names (or any custom names) to MaterialIcons names here.
 */
const MAPPING: IconMapping = {
  'house.fill': 'home',
  'paperplane.fill': 'send',
  'chevron.left.forwardslash.chevron.right': 'code',
  'chevron.right': 'chevron-right',
};

type IconSymbolProps = {
  name: keyof typeof MAPPING | string;
  size?: number;
  color: string | OpaqueColorValue;
  style?: StyleProp<TextStyle>;
};

export function IconSymbol({ name, size = 24, color, style }: IconSymbolProps) {
  // If the name doesn't exist in the mapping, fallback to 'help-outline'
  const iconName = MAPPING[name] || 'help-outline';

  return <MaterialIcons name={iconName} size={size} color={color} style={style} />;
}

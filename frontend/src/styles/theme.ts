import { createTheme } from '@mui/material/styles';

export const colors = {
  primary: '#F2913B',
  secondary: '#21709A',
  success: '#10b981',
  dark: '#1f2937',
  light: '#f3f4f6',
  shadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  borderRadius: '8px',
  transition: 'all 0.3s ease',
};

// 타입 확장
declare module '@mui/material/styles' {
  interface Palette {
    custom: {
      primary: string;
      secondary: string;
      success: string;
    };
  }

  interface PaletteOptions {
    custom?: {
      primary?: string;
      secondary?: string;
      success?: string;
    };
  }
}

// MUI 테마 생성
const theme = createTheme({
  palette: {
    mode: 'light',
    custom: {
      primary: colors.primary,
      secondary: colors.secondary,
      success: colors.success,
    },
  },
  shape: {
    borderRadius: 8,
  },
});

export default theme;

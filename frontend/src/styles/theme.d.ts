import { PaletteOptions, Palette } from '@mui/material/styles';

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
      primary: string;
      secondary: string;
      success: string;
    };
  }
}

import { createContext, useMemo, useState, ReactNode, useContext } from 'react';
import { createTheme, ThemeProvider, CssBaseline } from '@mui/material';
import { colors } from './theme';

interface ThemeContextProps {
  toggleColorMode: () => void;
}

// ex) import { useTheme } from '@mui/material/styles';
// ex) const theme = useTheme(); + theme.palette.custom.primary
const ColorModeContext = createContext<ThemeContextProps | undefined>(undefined);

export const useColorMode = () => {
  const context = useContext(ColorModeContext);
  if (!context) {
    throw new Error('useColorMode must be used within ColorModeProvider');
  }
  return context;
};

export const ColorModeProvider = ({ children }: { children: ReactNode }) => {
  const [mode, setMode] = useState<'light' | 'dark'>('light');

  const toggleColorMode = () => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  };

  const theme = useMemo(() =>
    createTheme({
      palette: {
        mode,
        ...(mode === 'light'
          ? {
              background: {
                default: '#f5f5f5',
                paper: '#fff',
              },
              text: {
                primary: '#000',
              },
              custom: {
                primary: colors.primary,
                secondary: colors.secondary,
                success: colors.success,
              },
            }
          : {
              background: {
                default: '#121212',
                paper: '#1e1e1e',
              },
              text: {
                primary: '#fff',
              },
              custom: {
                primary: colors.primary,
                secondary: colors.secondary,
                success: colors.success,
              },
            }),
      },
      typography: {
        fontFamily: 'Pretendard, system-ui, sans-serif',
      },
    }), [mode]);

  return (
    <ColorModeContext.Provider value={{ toggleColorMode }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
};

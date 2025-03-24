import React from 'react';
import { AppBar, Toolbar, Typography, IconButton, Box } from '@mui/material';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import { useTheme } from '@mui/material/styles';
import { Link } from 'react-router-dom';
import { useColorMode } from '../../styles/ThemeContext';

interface HeaderProps {
  logoSrc: string;
}

const Header: React.FC<HeaderProps> = ({ logoSrc }) => {
  const theme = useTheme();
  const { toggleColorMode } = useColorMode();

  return (
    <AppBar position="static" sx={{ backgroundColor: '#FFFFFF' }}
   enableColorOnDark>
      <Toolbar sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Link to="/" style={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}>
            <img src={logoSrc} alt="Logo" style={{ height: 40, marginRight: 16 }} />
            <Typography variant="h6" sx={{ color: 'black', fontWeight: 'bold' }}>
              PseudoLab ToolBox
            </Typography>
          </Link>
          {/* <Typography variant="h4" align="center" gutterBottom>
            PseudoLab ToolBox
          </Typography> */}
        </Box>

        <IconButton onClick={toggleColorMode}>
          {theme.palette.mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
        </IconButton>
      </Toolbar>
    </AppBar>
  );
};

export default Header;

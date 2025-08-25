import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import { Link } from 'react-router-dom';

interface HeaderProps {
  logoSrc: string;
}

const Header: React.FC<HeaderProps> = ({ logoSrc }) => {
  return (
    <AppBar position="static" sx={{ backgroundColor: 'rgb(30, 54, 97)' }} enableColorOnDark>
      <Toolbar sx={{ display: 'flex', justifyContent: 'center' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Link to="/" style={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}>
            <img src={logoSrc} alt="PseudoLab logo" style={{ height: 20, marginRight: 8, color: 'white' }} />
            <Typography variant='h6' sx={{ color: 'white', fontWeight: 'bold' }}>
              PseudoLab
            </Typography>
          </Link>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;

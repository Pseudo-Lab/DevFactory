import React from 'react';
import { Box, Container, Typography } from '@mui/material';
import { colors } from '../../styles/theme';

const Footer: React.FC = () => {
  return (
    <Box component="footer" sx={{ backgroundColor: colors.dark, color: '#fff', py: 3 }}>
      <Container>
        <Box sx={{ textAlign: 'center', pt: 1 }}>
          <Typography variant="body2" color="#9ca3af">
            &copy; 2020 PseudoLab. All rights reserved.
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;
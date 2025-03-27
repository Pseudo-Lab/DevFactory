import React from 'react';
import { Box, Container, Typography } from '@mui/material';
import { colors } from '../../../styles/theme';

const Hero: React.FC = () => {
  return (
    <Box
      component="section"
      sx={{
        backgroundColor: colors.primary,
        color: '#fff',
        py: 6,
        mb: 6,
        borderRadius: `0 0 ${colors.borderRadius} ${colors.borderRadius}`,
      }}
    >
      <Container>
        <Box sx={{ width: "100%" }}>
          <Typography variant="h3" component="h1" gutterBottom>
            PseudoLab 서비스 툴박스
          </Typography>
          <Typography variant="h6" sx={{ opacity: 0.9 }}>
            PseudoLab 커뮤니티를 위한 다양한 서비스를 간편하게 이용하세요.
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Hero;
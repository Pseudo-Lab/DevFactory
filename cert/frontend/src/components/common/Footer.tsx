import React from 'react';
import { Box, Container, Grid, Typography, Link } from '@mui/material';
import { colors } from '../../styles/theme';

const Footer: React.FC = () => {
  return (
    <Box component="footer" sx={{ backgroundColor: colors.dark, color: '#fff', py: 4, mt: 0.5 }}>
      <Container>
        <Grid container spacing={4} className="footer-content">
          <Grid item xs={12} md={4} className="footer-section">
            <Typography variant="h6" gutterBottom>PseudoLab</Typography>
            <Typography>
              PseudoLab은 인공지능과 데이터 사이언스 분야에서 함께 성장하는 커뮤니티입니다.
            </Typography>
          </Grid>

          <Grid item xs={12} md={4} className="footer-section">
            <Typography variant="h6" gutterBottom>링크</Typography>
            <Box component="ul" sx={{ listStyle: 'none', p: 0 }}>
              {['홈페이지', '서비스', '커뮤니티', '연락처'].map((link, idx) => (
                <li key={idx}>
                  <Link href="#" color="#d1d5db" underline="none" sx={{ transition: colors.transition, '&:hover': { color: '#fff' } }}>
                    {link}
                  </Link>
                </li>
              ))}
            </Box>
          </Grid>

          <Grid item xs={12} md={4} className="footer-section">
            <Typography variant="h6" gutterBottom>연락처</Typography>
            <Typography>이메일: info@pseudolab.com</Typography>
            <Typography>전화: 02-123-4567</Typography>
          </Grid>
        </Grid>

        <Box sx={{ textAlign: 'center', pt: 4, borderTop: '1px solid rgba(255, 255, 255, 0.1)', mt: 4 }}>
          <Typography variant="body2" color="#9ca3af">
            &copy; 2025 PseudoLab. All rights reserved.
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;
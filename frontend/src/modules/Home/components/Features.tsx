import React from 'react';
import { Box, Container, Typography } from '@mui/material';
import Grid2 from '@mui/material/Grid2';
import { useTheme } from '@mui/material/styles';

const Features: React.FC = () => {
  const theme = useTheme();

  // Dynamically switch backgrounds and colors depending on theme
  const isDarkMode = theme.palette.mode === 'dark';

  const features = [
    {
      icon: '📝',
      title: '간편한 신청',
      description: '몇 번의 클릭만으로 빠르게 서비스를 신청하세요.',
      color: theme.palette.custom?.pseudolabOrange || '#F2913B',
    },
    {
      icon: '🎨',
      title: '맞춤형 콘텐츠, 디자인',
      description: '필요한 콘텐츠와 디자인을 요청할 수 있습니다.',
      color: theme.palette.custom?.pseudolabBlue || '#21709A',
    },
    {
      icon: '🏢',
      title: '공간 활용',
      description: '다양한 목적에 맞는 공간을 예약하고 이용하세요.',
      color: theme.palette.custom?.success || '#10b981',
    },
  ];

  return (
    <Box
      sx={{
        backgroundColor: isDarkMode ? theme.palette.background.paper : '#fff',
        py: 6,
        my: 6,
        borderRadius: '8px',
        boxShadow: isDarkMode ? '0 4px 6px rgba(0, 0, 0, 0.3)' : '0 4px 6px rgba(0, 0, 0, 0.1)',
        color: theme.palette.text.primary,
        transition: 'all 0.3s ease',
      }}
    >
      <Container>
        <Grid2 container spacing={4}>
          {features.map((feature, idx) => (
            <Grid2 size={{ xs: 12, md: 4 }} key={idx}>
              <Box sx={{ textAlign: 'center', p: 2 }}>
                <Box
                  sx={{
                    backgroundColor: isDarkMode ? theme.palette.background.default : '#f3f4f6',
                    width: 60,
                    height: 60,
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    m: '0 auto 1rem',
                    fontSize: '1.5rem',
                    color: feature.color,
                    transition: 'all 0.3s ease',
                  }}
                >
                  {feature.icon}
                </Box>
                <Typography variant="h6" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography>{feature.description}</Typography>
              </Box>
            </Grid2>
          ))}
        </Grid2>
      </Container>
    </Box>
  );
};

export default Features;
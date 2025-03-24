import React from 'react';
import { Card, CardContent, Typography, Button, Box } from '@mui/material';
import Grid2 from '@mui/material/Grid2';
import { colors } from '../../../styles/theme';

interface ServicesProps {
  onOpenCert: () => void;
  onOpenContent: () => void;
  onOpenStudyRoom: () => void;
}

const Services: React.FC<ServicesProps> = ({
  onOpenCert,
  onOpenContent,
  onOpenStudyRoom,
}) => {
  return (
    <Grid2 container spacing={4} justifyContent="center">
      {/* Certificate */}
      <Grid2 size={{ xs: 12, md: 4 }}>
        <Box
          sx={{
            backgroundColor: '#fff',
            borderRadius: colors.borderRadius,
            boxShadow: colors.shadow,
            overflow: 'hidden',
            transition: colors.transition,
            '&:hover': {
              transform: 'translateY(-5px)',
              boxShadow: '0 10px 15px rgba(0, 0, 0, 0.1)',
            },
          }}
        >
          <Box
            sx={{
              height: 140,
              background: `linear-gradient(rgba(242, 145, 59, 0.8), rgba(242, 145, 59, 0.9)), url('/api/placeholder/400/320')`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              display: 'flex',
              alignItems: 'flex-end',
              p: 3,
            }}
          >
            <Typography variant="h6" sx={{ color: '#fff', fontWeight: 'bold' }}>
              수료증 발급 신청 및 출력
            </Typography>
          </Box>

          <Box sx={{ p: 3 }}>
            <Typography sx={{ color: '#4b5563', mb: 3 }}>
              PseudoLab 수료증 발급 신청서 작성
            </Typography>
            <Button
              variant="contained"
              fullWidth
              sx={{
                backgroundColor: colors.primary,
                borderRadius: colors.borderRadius,
                textTransform: 'none',
                '&:hover': { opacity: 0.9, transform: 'translateY(-2px)' },
              }}
              onClick={onOpenCert}
            >
              REQUEST NOW
            </Button>
          </Box>
        </Box>
      </Grid2>

      {/* Content Request */}
      <Grid2 size={{ xs: 12, md: 4 }}>
        <Box
          sx={{
            backgroundColor: '#fff',
            borderRadius: colors.borderRadius,
            boxShadow: colors.shadow,
            overflow: 'hidden',
            transition: colors.transition,
            '&:hover': {
              transform: 'translateY(-5px)',
              boxShadow: '0 10px 15px rgba(0, 0, 0, 0.1)',
            },
          }}
        >
          <Box
            sx={{
              height: 140,
              background: `linear-gradient(rgba(33, 112, 154, 0.8), rgba(33, 112, 154, 0.9)), url('/api/placeholder/400/320')`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              display: 'flex',
              alignItems: 'flex-end',
              p: 3,
            }}
          >
            <Typography variant="h6" sx={{ color: '#fff', fontWeight: 'bold' }}>
              콘텐츠/디자인 요청
            </Typography>
          </Box>

          <Box sx={{ p: 3 }}>
            <Typography sx={{ color: '#4b5563', mb: 3 }}>
              PseudoLab 필요한 콘텐츠/디자인 요청
            </Typography>
            <Button
              variant="contained"
              fullWidth
              sx={{
                backgroundColor: colors.secondary,
                borderRadius: colors.borderRadius,
                textTransform: 'none',
                '&:hover': { opacity: 0.9, transform: 'translateY(-2px)' },
              }}
              onClick={onOpenContent}
            >
              REQUEST NOW
            </Button>
          </Box>
        </Box>
      </Grid2>

      {/* Study Room Request */}
      <Grid2 size={{ xs: 12, md: 4 }}>
        <Box
          sx={{
            backgroundColor: '#fff',
            borderRadius: colors.borderRadius,
            boxShadow: colors.shadow,
            overflow: 'hidden',
            transition: colors.transition,
            '&:hover': {
              transform: 'translateY(-5px)',
              boxShadow: '0 10px 15px rgba(0, 0, 0, 0.1)',
            },
          }}
        >
          <Box
            sx={{
              height: 140,
              background: `linear-gradient(rgba(16, 185, 129, 0.8), rgba(16, 185, 129, 0.9)), url('/api/placeholder/400/320')`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              display: 'flex',
              alignItems: 'flex-end',
              p: 3,
            }}
          >
            <Typography variant="h6" sx={{ color: '#fff', fontWeight: 'bold' }}>
              공간 대여 신청
            </Typography>
          </Box>

          <Box sx={{ p: 3 }}>
            <Typography sx={{ color: '#4b5563', mb: 3 }}>
              OpenUP 공간 대여 신청서 작성
            </Typography>
            <Button
              variant="contained"
              fullWidth
              sx={{
                backgroundColor: colors.success,
                borderRadius: colors.borderRadius,
                textTransform: 'none',
                '&:hover': { opacity: 0.9, transform: 'translateY(-2px)' },
              }}
              onClick={onOpenStudyRoom}
            >
              RESERVE NOW
            </Button>
          </Box>
        </Box>
      </Grid2>
    </Grid2>
  );
};

export default Services;
import React, { useState } from 'react';
import { Container, Card, CardContent, Typography, Button, Box } from '@mui/material';
import Grid from '@mui/material/Grid2';

import Header from '../../components/common/Header';
import CertificateModal from './components/CertificateModal';
import ContentRequestModal from './components/ContentRequestModal';
import StudyRoomRequestModal from './components/StudyRoomRequestModal';
import logo from '../../assets/logo.png';

const HomePage: React.FC = () => {
  const [openCert, setOpenCert] = useState(false);
  const [openContent, setOpenContent] = useState(false);
  const [openStudyRoom, setOpenStudyRoom] = useState(false);

  return (
    <>
      <Header logoSrc={logo} />
      <Container sx={{ mt: 4 }}>
        <Grid container spacing={4} justifyContent="center">
          {/* Certificate */}
          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: 'bold' }} gutterBottom>수료증 발급 신청 및 출력</Typography>
                <Typography variant="body2" gutterBottom>
                  PseudoLab 수료증 발급 신청서 작성
                </Typography>
                <Box mt={2}>
                  <Button variant="contained" fullWidth onClick={() => setOpenCert(true)}>
                    Request Now
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Content Request */}
          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: 'bold' }} gutterBottom>콘텐츠/디자인 요청</Typography>
                <Typography variant="body2" gutterBottom>
                  PseudoLab에 필요한 콘텐츠/디자인 요청
                </Typography>
                <Box mt={2}>
                  <Button variant="contained" color="secondary" fullWidth onClick={() => setOpenContent(true)}>
                    Request Now
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Study Room Request */}
          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: 'bold' }} gutterBottom>공간 대여 신청</Typography>
                <Typography variant="body2" gutterBottom>
                  OpenUP 공간 대여 신청서 작성
                </Typography>
                <Box mt={2}>
                  <Button variant="contained" color="success" fullWidth onClick={() => setOpenStudyRoom(true)}>
                    Reserve Now
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Modals */}
        <CertificateModal open={openCert} onClose={() => setOpenCert(false)} />
        <ContentRequestModal open={openContent} onClose={() => setOpenContent(false)} />
        <StudyRoomRequestModal open={openStudyRoom} onClose={() => setOpenStudyRoom(false)} />
      </Container>
    </>
  );
};

export default HomePage;

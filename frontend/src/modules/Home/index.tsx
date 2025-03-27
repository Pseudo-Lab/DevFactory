import React, { useState } from 'react';
import { Container } from '@mui/material';

import CertificateModal from './components/CertificateModal';
import ContentRequestModal from './components/ContentRequestModal';
import StudyRoomRequestModal from './components/StudyRoomRequestModal';
import Services from './components/Services';

const HomePage: React.FC = () => {
  const [openCert, setOpenCert] = useState(false);
  const [openContent, setOpenContent] = useState(false);
  const [openStudyRoom, setOpenStudyRoom] = useState(false);

  return (
    <>
      <Container sx={{ mt: 4 }}>
        {/* Services Component */}
        <Services
          onOpenCert={() => setOpenCert(true)}
          onOpenContent={() => setOpenContent(true)}
          onOpenStudyRoom={() => setOpenStudyRoom(true)}
        />

        {/* Modals */}
        <CertificateModal open={openCert} onClose={() => setOpenCert(false)} />
        <ContentRequestModal open={openContent} onClose={() => setOpenContent(false)} />
        <StudyRoomRequestModal open={openStudyRoom} onClose={() => setOpenStudyRoom(false)} />
      </Container>
    </>
  );
};

export default HomePage;
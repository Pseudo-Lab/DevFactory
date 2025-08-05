import React from 'react';
import { Modal, Box, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

interface Props {
  open: boolean;
  onClose: () => void;
}

const ContentRequestModal: React.FC<Props> = ({ open, onClose }) => {
  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={modalStyle}>
        {/* Close Button */}
        <IconButton
          onClick={onClose}
          sx={{
            position: 'absolute',
            top: 8,
            right: 8,
            zIndex: 10,
            color: 'grey.500',
          }}
        >
          <CloseIcon />
        </IconButton>

        {/* Notion Embed */}
        <Box
          sx={{
            width: '100%',
            height: '600px',
            borderRadius: '8px',
            overflow: 'hidden',
          }}
        > 
          <iframe
            src="https://bailandoys.notion.site/ebd/1c03a2a2eed580de9a92ce32f49f4e7e"
            width="100%"
            height="600"
            allowFullScreen
            title="수료증 발급 신청 Notion Form"
            style={{
              border: 'none',
            }}
          />
        </Box>
      </Box>
    </Modal>
  );
};

const modalStyle = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '80%',
  maxWidth: 800,
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
  borderRadius: 2,
};

export default ContentRequestModal;

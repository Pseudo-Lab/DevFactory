import React from 'react';
import { Modal, Box, Typography, TextField, Button } from '@mui/material';

interface Props {
  open: boolean;
  onClose: () => void;
}

const ContentRequestModal: React.FC<Props> = ({ open, onClose }) => {
  const handleSubmit = () => {
    // TODO: Submit logic
    onClose();
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={modalStyle}>
        <Typography variant="h6" mb={2}>콘텐츠/디자인 요청</Typography>
        <TextField label="Name" fullWidth margin="normal" />
        <TextField label="Email" fullWidth margin="normal" />
        <TextField label="Request Details" fullWidth multiline rows={4} margin="normal" />
        <Button variant="contained" fullWidth onClick={handleSubmit} sx={{ mt: 2 }}>Submit</Button>
      </Box>
    </Modal>
  );
};

const modalStyle = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
  borderRadius: 2,
};

export default ContentRequestModal;

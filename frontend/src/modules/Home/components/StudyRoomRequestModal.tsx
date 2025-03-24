import React from 'react';
import { Modal, Box, Typography, TextField, Button } from '@mui/material';

interface Props {
  open: boolean;
  onClose: () => void;
}

const StudyRoomRequestModal: React.FC<Props> = ({ open, onClose }) => {
  const handleSubmit = () => {
    // TODO: Submit logic
    onClose();
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={modalStyle}>
        <Typography variant="h6" mb={2}>공간 대여 신청</Typography>
        <TextField label="Name" fullWidth margin="normal" />
        <TextField label="Email" fullWidth margin="normal" />
        <TextField
          label="Date (YYYY-MM-DD)"
          type="date"
          fullWidth
          margin="normal"
          slotProps={{
            inputLabel: { shrink: true },
          }}
        />
        <TextField label="Room Number" fullWidth margin="normal" />
        <TextField label="Time (e.g. 10:00 - 12:00)" fullWidth margin="normal" />
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

export default StudyRoomRequestModal;

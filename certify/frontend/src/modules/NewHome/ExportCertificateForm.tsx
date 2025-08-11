import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Chip,
  Paper,
  Grid,
  InputAdornment,
  Dialog,
  DialogContent,
  CircularProgress
} from '@mui/material';
import { Search as SearchIcon, Close as CloseIcon, CheckCircle as CheckCircleIcon } from '@mui/icons-material';
import { styled } from '@mui/material/styles';

// Styled components
const StyledContainer = styled(Box)({
  minHeight: '100vh',
  background: 'linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  padding: '16px',
});

const StyledPaper = styled(Paper)({
  padding: '32px',
  borderRadius: '16px',
  boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  maxWidth: '500px',
  width: '100%',
});

const StyledTextField = styled(TextField)({
  '& .MuiOutlinedInput-root': {
    '& fieldset': {
      border: 'none',
      borderBottom: '1px solid #d1d5db',
      borderRadius: 0,
    },
    '&:hover fieldset': {
      borderBottom: '1px solid #6b7280',
    },
    '&.Mui-focused fieldset': {
      borderBottom: '2px solid #3b82f6',
    },
  },
  '& .MuiInputLabel-root': {
    color: '#374151',
    fontSize: '14px',
    fontWeight: 500,
  },
});

const StyledFormControl = styled(FormControl)({
  '& .MuiOutlinedInput-root': {
    '& fieldset': {
      border: 'none',
      borderBottom: '1px solid #d1d5db',
      borderRadius: 0,
    },
    '&:hover fieldset': {
      borderBottom: '1px solid #6b7280',
    },
    '&.Mui-focused fieldset': {
      borderBottom: '2px solid #3b82f6',
    },
  },
  '& .MuiInputLabel-root': {
    color: '#374151',
    fontSize: '14px',
    fontWeight: 500,
  },
});

const StyledButton = styled(Button)({
  borderRadius: '25px',
  padding: '12px 24px',
  fontWeight: 600,
  textTransform: 'none',
});

const ExportCertificateForm = () => {
  const [formData, setFormData] = useState({
    name: '홍길동',
    email: 'psuedoLab@naver.com',
    period: '20',
    searchText: ''
  });

  const [tags, setTags] = useState<string[]>([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  const exampleStudies = ['DevFactory', 'JobPT', 'AI Research Club', '3D Vision', 'Test Study'];
  const filteredStudies = exampleStudies.filter(study =>
    study.toLowerCase().includes(formData.searchText.toLowerCase())
  );

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | { name?: string; value: unknown }>) => {
    const { name, value } = e.target as HTMLInputElement;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleTagDelete = (tagToDelete: string) => {
    setTags(prevTags => prevTags.filter(tag => tag !== tagToDelete));
  };

  const handleSubmit = () => {
    setModalOpen(true);
    setIsLoading(true);
    setIsComplete(false);
    
    // 2초 후 로딩 완료
    setTimeout(() => {
      setIsLoading(false);
      setIsComplete(true);
    }, 2000);
  };

  const handleModalClose = () => {
    setModalOpen(false);
    setIsLoading(false);
    setIsComplete(false);
  };

  const handleCancel = () => {
    setFormData({
      name: '홍길동',
      email: 'pseudoLab@naver.com',
      period: '20',
      searchText: ''
    });
    setTags([]);
  };

  return (
    <StyledContainer>
      {/* Header */}
      <Box
        sx={{
          position: 'absolute',
          top: 16,
          left: 16,
          color: 'white',
          fontSize: '14px',
          opacity: 0.8,
        }}
      >
        수료증 특이사항
      </Box>

      <Container maxWidth="sm">
        {/* Logo */}
        <Box textAlign="center" mb={5}>
          <Typography
            variant="h5"
            component="div"
            sx={{ color: 'white', fontWeight: 500 }}
          >
            PseudoLab
          </Typography>
        </Box>

        {/* Title */}
        <Box textAlign="center" mb={4}>
          <Typography
            variant="h3"
            component="h1"
            sx={{
              color: 'white',
              fontWeight: 'bold',
              mb: 1,
              fontSize: { xs: '2rem', sm: '3rem' }
            }}
          >
            수료증 발급 신청
          </Typography>
          <Typography
            variant="body1"
            sx={{ color: '#bfdbfe' }}
          >
            PseudoLab 수료증 발급 신청 및 출력
          </Typography>
        </Box>

        {/* Form */}
        <StyledPaper>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            {/* Name Field */}
            <Grid container alignItems="center" spacing={2}>
              <Grid item xs={3}>
                <Typography variant="body2" sx={{ fontWeight: 500, color: '#374151' }}>
                  이름<span style={{ color: '#ef4444' }}>*</span>
                </Typography>
              </Grid>
              <Grid item xs={9}>
                <StyledTextField
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  fullWidth
                  variant="outlined"
                  size="medium"
                />
              </Grid>
            </Grid>

            {/* Email Field */}
            <Grid container alignItems="center" spacing={2}>
              <Grid item xs={3}>
                <Typography variant="body2" sx={{ fontWeight: 500, color: '#374151' }}>
                  이메일<span style={{ color: '#ef4444' }}>*</span>
                </Typography>
              </Grid>
              <Grid item xs={9}>
                <StyledTextField
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  fullWidth
                  variant="outlined"
                  size="medium"
                />
              </Grid>
            </Grid>

            {/* Period Field */}
            <Grid container alignItems="center" spacing={2}>
              <Grid item xs={3}>
                <Typography variant="body2" sx={{ fontWeight: 500, color: '#374151' }}>
                  참여 기수<span style={{ color: '#ef4444' }}>*</span>
                </Typography>
              </Grid>
              <Grid item xs={9}>
                <StyledFormControl fullWidth size="medium">
                  <Select
                    name="period"
                    value={formData.period}
                    onChange={handleInputChange}
                  >
                    <MenuItem value="20">20</MenuItem>
                    <MenuItem value="21">21</MenuItem>
                    <MenuItem value="22">22</MenuItem>
                    <MenuItem value="23">23</MenuItem>
                  </Select>
                </StyledFormControl>
              </Grid>
            </Grid>

            {/* Study Name Field */}
            <Grid container alignItems="flex-start" spacing={2}>
              <Grid item xs={3}>
                <Typography variant="body2" sx={{ fontWeight: 500, color: '#374151', mt: 1 }}>
                  스터디명<span style={{ color: '#ef4444' }}>*</span>
                </Typography>
              </Grid>
              <Grid item xs={9}>
                <Box>
                  {/* Tags */}
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                    {tags.map((tag, index) => (
                      <Chip
                        key={index}
                        label={tag}
                        onDelete={() => handleTagDelete(tag)}
                        deleteIcon={<CloseIcon />}
                        sx={{
                          backgroundColor: '#10b981',
                          color: 'white',
                          '& .MuiChip-deleteIcon': {
                            color: 'white',
                          },
                        }}
                      />
                    ))}
                  </Box>
                  
                  {/* Search Input */}
                  <StyledTextField
                    name="searchText"
                    value={formData.searchText}
                    onChange={handleInputChange}
                    fullWidth
                    placeholder="스터디명을 검색하세요"
                    variant="outlined"
                    size="medium"
                    InputProps={{
                      endAdornment: (
                        <InputAdornment position="end">
                          <SearchIcon sx={{ color: '#9ca3af' }} />
                        </InputAdornment>
                      ),
                    }}
                  />

                  {/* Filtered Results */}
                  {filteredStudies.length > 0 && (
                    <Box sx={{ mt: 2 }}>
                      {filteredStudies.map((study, index) => (
                        <Typography
                          key={index}
                          variant="body2"
                          sx={{
                            padding: '8px',
                            backgroundColor: '#f3f4f6',
                            borderRadius: '4px',
                            marginBottom: '4px',
                            cursor: 'pointer',
                            '&:hover': {
                              backgroundColor: '#e5e7eb',
                            },
                          }}
                          onClick={() => setTags([...tags, study])}
                        >
                          {study}
                        </Typography>
                      ))}
                    </Box>
                  )}
                </Box>
              </Grid>
            </Grid>

            {/* Buttons */}
            <Box sx={{ display: 'flex', gap: 2, mt: 4 }}>
              <StyledButton
                variant="contained"
                onClick={handleCancel}
                sx={{
                  flex: 1,
                  backgroundColor: '#9ca3af',
                  '&:hover': {
                    backgroundColor: '#6b7280',
                  },
                }}
              >
                취소
              </StyledButton>
              <StyledButton
                variant="contained"
                onClick={handleSubmit}
                sx={{
                  flex: 1,
                  backgroundColor: '#10b981',
                  '&:hover': {
                    backgroundColor: '#059669',
                  },
                }}
              >
                발급신청
              </StyledButton>
            </Box>
          </Box>
        </StyledPaper>

        {/* Modal */}
        <Dialog
          open={modalOpen}
          onClose={isComplete ? handleModalClose : undefined}
          PaperProps={{
            sx: {
              borderRadius: '16px',
              padding: '24px',
              minWidth: '320px',
              textAlign: 'center'
            }
          }}
        >
          <DialogContent sx={{ padding: '32px 24px' }}>
            {isLoading ? (
              // 로딩 상태
              <Box>
                <CircularProgress
                  size={60}
                  sx={{ color: '#10b981', mb: 3 }}
                />
                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
                  수료증 발급 진행중
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  수료증 발급이 진행중입니다
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  잠시만 기다려주세요
                </Typography>
              </Box>
            ) : isComplete ? (
              // 완료 상태
              <Box>
                <CheckCircleIcon
                  sx={{
                    fontSize: '60px',
                    color: '#10b981',
                    mb: 2
                  }}
                />
                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
                  수료증 발급 완료
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  수료증 발급이 성공적으로
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  이메일로 전송됐습니다
                </Typography>
                <StyledButton
                  variant="contained"
                  onClick={handleModalClose}
                  sx={{
                    backgroundColor: '#10b981',
                    '&:hover': {
                      backgroundColor: '#059669',
                    },
                    px: 4
                  }}
                >
                  확인
                </StyledButton>
              </Box>
            ) : null}
          </DialogContent>
        </Dialog>
      </Container>
    </StyledContainer>
  );
};

export default ExportCertificateForm;
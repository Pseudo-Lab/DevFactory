import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  Button,
  Chip,
  Paper,
  InputAdornment,
  Dialog,
  DialogContent,
  LinearProgress,
  Autocomplete,
} from '@mui/material';
import { Search as SearchIcon, CheckCircle as CheckCircleIcon } from '@mui/icons-material';
import CancelIcon from '@mui/icons-material/Cancel';
import { styled } from '@mui/material/styles';

// Styled components
const StyledContainer = styled(Box)({
  minHeight: '100vh',
  background: 'rgb(24, 43, 77)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  padding: '16px',
});

const StyledPaper = styled(Paper)(({ theme }) => ({
  paddingTop: '60px',
  paddingBottom: '60px',
  paddingLeft: '60px',
  paddingRight: '60px',
  borderRadius: '12px',
  boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
  maxWidth: '600px',
  width: '100%',
  backgroundColor: '#ffffff',
  // 375px 이하에서만 좌우 패딩 20px
  '@media (max-width:450px)': {
    paddingLeft: '20px',
    paddingRight: '20px',
  },
}));

const StyledTextField = styled(TextField)({
  '& .MuiOutlinedInput-root': {
    backgroundColor: '#f8fafc',
    borderRadius: '12px',
    '& fieldset': {
      border: '1px solid #e2e8f0',
    },
    '&:hover fieldset': {
      border: '1px solid #cbd5e1',
    },
    '&.Mui-focused fieldset': {
      border: '2px solid #3b82f6',
    },
  },
  '& .MuiInputLabel-root': {
    color: '#64748b',
    fontSize: '14px',
    fontWeight: 500,
  },
  '& .MuiInputBase-input': {
    padding: '16px 14px',
  },
});

const StyledFormControl = styled(FormControl)({
  '& .MuiOutlinedInput-root': {
    backgroundColor: '#f8fafc',
    borderRadius: '12px',
    '& fieldset': {
      border: '1px solid #e2e8f0',
    },
    '&:hover fieldset': {
      border: '1px solid #cbd5e1',
    },
    '&.Mui-focused fieldset': {
      border: '2px solid #3b82f6',
    },
  },
  '& .MuiInputLabel-root': {
    color: '#64748b',
    fontSize: '14px',
    fontWeight: 500,
  },
  '& .MuiSelect-select': {
    padding: '16px 14px',
  },
});

const StyledButton = styled(Button)({
  borderRadius: '25px',
  padding: '8px 16px',
  fontWeight: 600,
  textTransform: 'none',
  fontSize: '16px',
});

const FieldLabel = styled(Typography)({
  fontWeight: 600,
  color: '#1f2937',
  marginBottom: '12px',
  fontSize: '16px',
});

const FieldRow: React.FC<{
  label: React.ReactNode;
  children: React.ReactNode;
  alignTop?: boolean;
}> = ({ label, children, alignTop }) => (
  <Box
    sx={{
      display: 'grid',
      gridTemplateColumns: '90px 1fr',
      alignItems: alignTop ? 'start' : 'center',
      rowGap: 1.5,
      columnGap: 3,
      '@media (max-width:375px)': {
        gridTemplateColumns: '1fr',
        alignItems: 'start',
      },
    }}
  >
    <Typography
      variant="body1"
      sx={{ fontWeight: 600, color: '#1f2937', fontSize: '16px' }}
    >
      {label}
    </Typography>

    <Box sx={{ width: '100%', minWidth: 0 }}>
      {children}
    </Box>
  </Box>
);

const ExportCertificateForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    period: '',
    searchText: ''
  });

  const [tags, setTags] = useState<string[]>([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [progress, setProgress] = useState(0);

  const exampleStudies = ['DevFactory', 'JobPT', 'AI Research Club', '3D Vision', 'Test Study'];

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
    setProgress(0);

    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsLoading(false);
          setIsComplete(true);
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  const handleModalClose = () => {
    setModalOpen(false);
    setIsLoading(false);
    setIsComplete(false);
  };

  const handleCancel = () => {
    setFormData({
      name: '',
      email: '',
      period: '',
      searchText: ''
    });
    setTags([]);
  };

  return (
    <StyledContainer>
      <Container maxWidth="sm">
        {/* Title */}
        <Box textAlign="center" mb={6}>
          <Typography
            variant="h3"
            component="h1"
            sx={{
              color: 'white',
              fontWeight: 'bold',
              mb: 2,
              fontSize: { xs: '2.5rem', sm: '3.5rem' }
            }}
          >
            수료증 발급 신청
          </Typography>
          <Typography
            variant="h6"
            sx={{ color: '#bfdbfe', fontWeight: 400 }}
          >
            가짜연구소 수료증 발급 신청 및 출력
          </Typography>
        </Box>

        {/* Form */}
        <StyledPaper>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            {/* Name Field */}
            <FieldRow label={<>이름<span style={{ color: '#ef4444' }}>*</span></>}>
              <StyledTextField
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                fullWidth
                variant="outlined"
                placeholder="이름을 입력하세요"
                size="medium"
              />
            </FieldRow>

            {/* Email Field */}
            <FieldRow label={<>이메일<span style={{ color: '#ef4444' }}>*</span></>}>
              <StyledTextField
                name="email"
                type="email"
                value={formData.email}
                onChange={handleInputChange}
                fullWidth
                variant="outlined"
                placeholder="pseudoLab@naver.com"
                size="medium"
              />
            </FieldRow>

            {/* Period Field */}
            <FieldRow label={<>참여 기수<span style={{ color: '#ef4444' }}>*</span></>}>
              <StyledFormControl fullWidth size="medium">
                <Select
                  name="period"
                  value={formData.period}
                  onChange={handleInputChange}
                  displayEmpty
                  renderValue={(selected) =>
                    !selected ? <span style={{ color: '#9ca3af' }}>참여 기수를 선택하세요</span> : (selected as string)
                  }
                >
                  <MenuItem value="10">10</MenuItem>
                  <MenuItem value="11">11</MenuItem>
                </Select>
              </StyledFormControl>
            </FieldRow>

            {/* Study Name Field */}
            <FieldRow
              label={<>스터디명<span style={{ color: '#ef4444' }}>*</span></>}
            >
              <Autocomplete
                multiple
                disableCloseOnSelect
                options={exampleStudies}
                value={tags}
                onChange={(_, newValue) => setTags(Array.from(new Set(newValue)))}
                inputValue={formData.searchText}
                onInputChange={(_, newInputValue) =>
                  setFormData(prev => ({ ...prev, searchText: newInputValue }))
                }
                filterOptions={(options, { inputValue }) =>
                  options.filter(o => o.toLowerCase().includes(inputValue.toLowerCase()))
                }
                renderTags={(value, getTagProps) =>
                  value.map((option, index) => (
                    <Chip
                      {...getTagProps({ index })}
                      key={option}
                      label={option}
                      sx={{
                        backgroundColor: '#10b981',
                        color: 'white',
                        fontWeight: 500,
                        '& .MuiChip-deleteIcon': { color: 'white' },
                      }}
                    />
                  ))
                }
                renderInput={(params) => (
                  <StyledTextField
                    {...params}
                    placeholder={tags.length === 0 ? '스터디 이름을 입력하세요' : ''}
                    variant="outlined"
                    size="medium"
                    InputProps={{
                      ...params.InputProps,
                      endAdornment: (
                        <>
                          {params.InputProps.endAdornment}
                          <InputAdornment position="end">
                            <SearchIcon sx={{ color: '#9ca3af' }} />
                          </InputAdornment>
                        </>
                      ),
                    }}
                  />
                )}
              />
            </FieldRow>

            {/* Buttons */}
            <Box sx={{ display: 'flex', gap: 3, mt: 6 }}>
              <StyledButton
                variant="contained"
                onClick={handleCancel}
                sx={{
                  flex: 1,
                  backgroundColor: '#9ca3af',
                  color: 'white',
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
                  color: 'white',
                  '&:hover': {
                    backgroundColor: '#059669',
                  },
                }}
              >
                발급하기
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
          <DialogContent sx={{ padding: '12px 6px' }}>
            {isLoading ? (
              // 로딩 상태
              <Box>
                <Typography variant="body2" sx={{ fontWeight: 'bold', my: 2, color: '#1f2937' }}>
                  수료증을 발급 중이에요.
                </Typography>
                {/* PNG 이미지 */}
                <Box
                  component="img"
                  src="/sticky_notes.png" // public 폴더 안에 넣었다면 /images/... 로 접근
                  alt="loading"
                  sx={{
                    width: 120,
                    height: 120,
                    mb: 3,
                    mx: 'auto', // 가운데 정렬
                    display: 'block'
                  }}
                />
                <LinearProgress
                  variant="determinate"
                  value={progress}
                  sx={{ 
                    mb: 5, 
                    height: '10px', 
                    borderRadius: '5px', 
                    backgroundColor: '#e5e7eb',
                    '& .MuiLinearProgress-bar': {
                      backgroundColor: '#10b981'
                    }
                  }}
                />
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
                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1, color: '#1f2937' }}>
                  수료증 발급 완료
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0 }}>
                  제출하신 이메일로
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0 }}>
                  수료증 발급이 완료됐습니다!
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  메일함을 확인해보세요.
                </Typography>
                <StyledButton
                  variant="contained"
                  onClick={handleModalClose}
                  sx={{
                    backgroundColor: '#10b981',
                    color: 'white',
                    '&:hover': {
                      backgroundColor: '#059669',
                    },
                    width: '100%',
                    height: '40px'
                  }}
                >
                  확인
                </StyledButton>
              </Box>
            ) : (
              // 실패 상태
              <Box>
                <CancelIcon
                  sx={{
                    fontSize: '60px',
                    color: '#ef4444',
                    mb: 2,
                  }}
                />
                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1, color: '#1f2937' }}>
                  수료증 발급 실패
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0 }}>
                  수료증 발급에 실패했습니다.
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0 }}>
                  디스코드를 통해
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  김찬란에게 문의해주세요.
                </Typography>
                <StyledButton
                  variant="contained"
                  onClick={handleModalClose}
                  sx={{
                    backgroundColor: '#10b981',
                    color: 'white',
                    '&:hover': {
                      backgroundColor: '#059669',
                    },
                    width: '100%',
                    height: '40px'
                  }}
                >
                  확인
                </StyledButton>
              </Box>
              )
            }
          </DialogContent>
        </Dialog>
      </Container>
    </StyledContainer>
  );
};

export default ExportCertificateForm;
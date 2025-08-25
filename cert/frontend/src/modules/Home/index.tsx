import React, { useState, useMemo, useEffect } from 'react';
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
  InputLabel
} from '@mui/material';
import { ButtonProps } from "@mui/material/Button";
import { Search as SearchIcon } from '@mui/icons-material';
import { styled } from '@mui/material/styles';
import successImg from "../../assets/success.png";
import failImg from "../../assets/fail.png";


type StudyMeta = {
  periods: string[]; 
  studiesByPeriod?: Record<string, string[]>;
  studies?: string[];
};

type IssuePayload = {
  name: string;
  email: string;
  period: string;
  studies: string[];
};

type IssueResponse = {
  returnCode: number; // 200, 404, 500 등
};

async function fetchStudyMeta(): Promise<StudyMeta> {
  // const res = await fetch('/api/studies/meta');
  // if (!res.ok) throw new Error('Failed to load meta');
  // return (await res.json()) as StudyMeta;

  await new Promise(r => setTimeout(r, 300));
  return {
    periods: ["10", "11"],
    studiesByPeriod: {
      "10": ["DevFactory", "JobPT", "3D Vision"],
      "11": ["AI Research Club", "Test Study"]
    },
    studies: ["DevFactory", "JobPT", "AI Research Club", "3D Vision", "Test Study"]
  };
}

async function issueCertificate(payload: IssuePayload): Promise<IssueResponse> {
  // const res = await fetch('/api/certificates/issue', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify(payload),
  // });
  // if (!res.ok) throw new Error('Issue API failed');
  // return (await res.json()) as IssueResponse;
  await new Promise(r => setTimeout(r, 500));
  return { returnCode: 200 };
}

const SuccessIcon: React.FC = () => {
  return (
    <Box
      component="img"
      src={successImg}
      alt="success"
      sx={{
        width: 60,
        height: 60,
        mb: 2,
      }}
    />
  );
};

const FailIcon: React.FC = () => {
  return (
    <Box
      component="img"
      src={failImg}
      alt="fail"
      sx={{
        width: 60,
        height: 60,
        mb: 2,
      }}
    />
  );
};

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

const StyledButton = styled(Button)<ButtonProps<"a">>({
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

const DiscordButton: React.FC<{ onClick?: () => void }> = ({ onClick }) => {
  return (
    <StyledButton
      variant="contained"
      component="a"
      href="https://discord.com/channels/944032730050621450/944039762052923403"
      target="_blank"
      rel="noopener noreferrer"
      sx={{
        backgroundColor: "rgb(22, 43, 77)",
        color: "white",
        "&:hover": {
          backgroundColor: "rgb(14, 30, 56)",
        },
        width: "100%",
        height: "40px",
      }}
      onClick={onClick}
    >
      디스코드 바로가기
    </StyledButton>
  );
};

const ExportCertificateForm = () => {
  // 폼 데이터
  const [formData, setFormData] = useState({ name: '', email: '', period: '', searchText: '' });
  const [tags, setTags] = useState<string[]>([]);

  // 메타데이터
  const [periods, setPeriods] = useState<string[]>([]);
  const [allStudies, setAllStudies] = useState<string[]>([]);
  const [studiesByPeriod, setStudiesByPeriod] = useState<Record<string, string[]> | undefined>(undefined);
  const [metaLoading, setMetaLoading] = useState<boolean>(true);
  const [metaError, setMetaError] = useState<string | null>(null);

  // 모달 & 로딩
  const [modalOpen, setModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [progress, setProgress] = useState(0);

  const [returnCode, setReturnCode] = useState<number | null>(null);

  const [testReturnCode, setTestReturnCode] = useState<number>(200);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        setMetaLoading(true);
        const meta = await fetchStudyMeta();
        if (!mounted) return;
        setPeriods(meta.periods ?? []);
        setAllStudies(meta.studies ?? []);
        setStudiesByPeriod(meta.studiesByPeriod);
        setMetaError(null);
      } catch (e: any) {
        setMetaError(e?.message ?? '메타데이터 로드 실패');
      } finally {
        if (mounted) setMetaLoading(false);
      }
    })();
    return () => { mounted = false; };
  }, []);

  // period에 따라 Autocomplete 옵션 필터 (studiesByPeriod가 있으면 활용)
  const studyOptions = useMemo(() => {
    if (studiesByPeriod && formData.period) {
      return studiesByPeriod[formData.period] ?? [];
    }
    return allStudies;
  }, [studiesByPeriod, formData.period, allStudies]);

  // 입력 변경
  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> | { target: { name?: string; value: unknown } }
  ) => {
    const { name, value } = (e as any).target;
    setFormData(prev => ({ ...prev, [name as keyof typeof prev]: value as string }));
    // period 변경 시 현재 선택한 tags가 옵션에 없으면 제거
    if (name === 'period' && Array.isArray(tags) && studiesByPeriod) {
      const valid = new Set(studiesByPeriod[value as string] ?? []);
      setTags(prev => prev.filter(t => valid.has(t)));
    }
  };

  const isEmailValid = useMemo(() => {
    if (!formData.email) return false;
    // 이메일 체크
    return /\S+@\S+\.\S+/.test(formData.email);
  }, [formData.email]);
  

  const handleTagDelete = (tagToDelete: string) => {
    setTags(prevTags => prevTags.filter(tag => tag !== tagToDelete));
  };

  const isFormValid = useMemo(() => {
    return (
      !!formData.name.trim() &&
      !!formData.period &&
      isEmailValid &&
      tags.length > 0
    );
  }, [formData.name, formData.period, isEmailValid, tags.length]);

  const handleSubmit = async () => {
    setModalOpen(true);
    setIsLoading(true);
    setIsComplete(false);
    setReturnCode(null);
    setProgress(0);

    // 가짜 진행바
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 10;
      });
    }, 150);

    try {
      // 실제 API 호출 (응답 returnCode는 무시하고, UI에서 선택한 testReturnCode를 반영)
      await issueCertificate({
        name: formData.name.trim(),
        email: formData.email.trim(),
        period: formData.period,
        studies: tags,
      });

      // 테스트용 returnCode 적용
      // 200: 성공, 300: 일반 실패, 나머지(예: 302): “명단에 없음” 시나리오
      setReturnCode(testReturnCode);
    } catch (e) {
      // 호출 자체 실패 시 일반 실패로 처리
      setReturnCode(300);
    } finally {
      setIsLoading(false);
      setIsComplete(true);
    }
  };

  const handleModalClose = () => {
    setModalOpen(false);
    setIsLoading(false);
    setIsComplete(false);
    setProgress(0);
    setReturnCode(null);
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
          <Typography variant="h3" component="h1" sx={{ color: 'white', fontWeight: 'bold', mb: 2, fontSize: { xs: '2.5rem', sm: '3.5rem' } }}>
            수료증 발급 신청
          </Typography>
          <Typography variant="h6" sx={{ color: '#bfdbfe', fontWeight: 400 }}>
            가짜연구소 수료증 발급 신청 및 출력
          </Typography>
        </Box>

        <StyledPaper>
          {/* 메타 로딩/에러 */}
          {metaLoading ? (
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="body2" sx={{ color: '#1f2937', mb: 2 }}>옵션을 불러오는 중…</Typography>
              <LinearProgress />
            </Box>
          ) : metaError ? (
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="body2" color="error" sx={{ mb: 1 }}>옵션을 불러오지 못했어요.</Typography>
              <Typography variant="caption" color="text.secondary">{metaError}</Typography>
            </Box>
          ) : (
            <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              {/* Name */}
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

              {/* Email */}
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
                  error={!!formData.email && !isEmailValid}
                />
              </FieldRow>

              {/* Period */}
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
                    {periods.map(p => (
                      <MenuItem key={p} value={p}>{p}</MenuItem>
                    ))}
                  </Select>
                </StyledFormControl>
              </FieldRow>

              {/* Study names (Autocomplete, multiple) */}
              <FieldRow label={<>스터디명<span style={{ color: '#ef4444' }}>*</span></>}>
                <Autocomplete
                  multiple
                  disableCloseOnSelect
                  options={studyOptions}
                  value={tags}
                  onChange={(_, newValue) => setTags(Array.from(new Set(newValue)))}
                  inputValue={formData.searchText}
                  onInputChange={(_, newInputValue) => setFormData(prev => ({ ...prev, searchText: newInputValue }))}
                  filterOptions={(options, { inputValue }) =>
                    options.filter(o => o.toLowerCase().includes(inputValue.toLowerCase()))
                  }
                  popupIcon={null}
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
                        startAdornment: (
                          <>
                            <InputAdornment position="start">
                              <SearchIcon sx={{ ml: 1, color: '#9ca3af' }} />
                            </InputAdornment>
                            {params.InputProps.startAdornment}
                          </>
                        ),
                      }}
                    />
                  )}
                />
              </FieldRow>

              <FieldRow label="테스트 코드">
                <StyledFormControl fullWidth size="medium">
                  <InputLabel id="returncode-label">returnCode (테스트)</InputLabel>
                  <Select
                    labelId="returncode-label"
                    value={String(testReturnCode)}
                    label="returnCode (테스트)"
                    onChange={(e) => setTestReturnCode(Number(e.target.value))}
                  >
                    <MenuItem value="200">200 (성공)</MenuItem>
                    <MenuItem value="404">404 (명단 없음)</MenuItem>
                    <MenuItem value="500">500 (실패)</MenuItem>
                  </Select>
                </StyledFormControl>
              </FieldRow>

              {/* Buttons */}
              <Box sx={{ display: 'flex', gap: 3, mt: 2 }}>
                <StyledButton
                  variant="contained"
                  onClick={handleCancel}
                  sx={{
                    flex: 1,
                    backgroundColor: '#9ca3af',
                    color: 'white',
                    '&:hover': { backgroundColor: '#6b7280' },
                  }}
                >
                  취소
                </StyledButton>
                <StyledButton
                  variant="contained"
                  onClick={handleSubmit}
                  disabled={!isFormValid}
                  sx={{
                    flex: 1,
                    backgroundColor: isFormValid ? '#10b981' : '#a7f3d0',
                    color: 'white',
                    '&:hover': { backgroundColor: isFormValid ? '#059669' : '#a7f3d0' },
                  }}
                >
                  발급하기
                </StyledButton>
              </Box>
            </Box>
          )}
        </StyledPaper>

        {/* Modal */}
        <Dialog
          open={modalOpen}
          onClose={isComplete ? handleModalClose : undefined}
          PaperProps={{ sx: { borderRadius: '16px', padding: '24px', minWidth: '320px', textAlign: 'center' } }}
        >
          <DialogContent sx={{ padding: '12px 6px' }}>
            {isLoading && (
              <Box>
                <Typography variant="body2" sx={{ fontWeight: 'bold', my: 2, color: '#1f2937' }}>
                  수료증을 발급 중이에요.
                </Typography>
                <Box
                  component="img"
                  src="/sticky_notes.png"
                  alt="loading"
                  sx={{ width: 120, height: 120, mb: 3, mx: 'auto', display: 'block' }}
                />
                <LinearProgress
                  variant="determinate"
                  value={progress}
                  sx={{
                    mb: 5,
                    height: '10px',
                    borderRadius: '5px',
                    backgroundColor: '#e5e7eb',
                    '& .MuiLinearProgress-bar': { backgroundColor: '#10b981' }
                  }}
                />
              </Box>
            )}

            {!isLoading && returnCode === 200 && (
              /* 성공 */
              <Box>
                <SuccessIcon />
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
                    '&:hover': { backgroundColor: '#059669' },
                    width: '100%',
                    height: '40px'
                  }}
                >
                  확인
                </StyledButton>
              </Box>
            )}

            {!isLoading && returnCode === 500 && (
              /* 일반 실패 */
              <Box>
                <FailIcon />
                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1, color: '#1f2937' }}>
                  수료증 발급 실패
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0 }}>
                  수료증 발급에 실패했습니다. 🥲
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0 }}>
                  디스코드를 통해
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  질문게시판에 문의해주세요.
                </Typography>
                <DiscordButton onClick={handleModalClose}/>
              </Box>
            )}

            {!isLoading && returnCode === 404 && (
              /* 명단 없음 */
              <Box>
                <FailIcon />
                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1, color: '#1f2937' }}>
                  수료증 발급 실패
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0 }}>
                  수료 명단에 존재하지 않습니다. 🥲
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0 }}>
                  디스코드를 통해
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  질문게시판에 문의해주세요.
                </Typography>
                <DiscordButton onClick={handleModalClose}/>
              </Box>
            )}
          </DialogContent>
        </Dialog>
      </Container>
    </StyledContainer>
  );
};

export default ExportCertificateForm;
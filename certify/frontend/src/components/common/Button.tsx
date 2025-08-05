import React from 'react';
import Button from '@mui/material/Button';

interface CommonButtonProps {
  label: string;
  onClick?: () => void;
  color?: 'primary' | 'secondary' | 'inherit' | 'error' | 'info' | 'success' | 'warning';
  variant?: 'text' | 'outlined' | 'contained';
}

const CommonButton: React.FC<CommonButtonProps> = ({
  label,
  onClick,
  color = 'primary',
  variant = 'contained',
}) => {
  return (
    <Button variant={variant} color={color} onClick={onClick}>
      {label}
    </Button>
  );
};

export default CommonButton;
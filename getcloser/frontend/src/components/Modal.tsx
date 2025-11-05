"use client";

import React from 'react';

interface ModalProps {
  title: string;
  content: string;
  onConfirm: () => void;
  onDoNotShowAgain: () => void;
  isOpen: boolean;
}

const Modal: React.FC<ModalProps> = ({ title, content, onConfirm, onDoNotShowAgain, isOpen }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
      <div className="bg-[hsl(160_30%_25%)] text-card-foreground p-6 rounded-lg shadow-lg max-w-sm w-full">
        <h2 className="text-xl font-bold mb-4">{title}</h2>
        <p className="mb-6" dangerouslySetInnerHTML={{ __html: content }}></p>
        <div className="flex justify-end space-x-4">
          <button
            onClick={onDoNotShowAgain}
            className="px-4 py-2 rounded hover:bg-secondary/80"
          >
            다시 보지 않기
          </button>
          <button
            onClick={onConfirm}
            className="px-4 py-2 rounded hover:bg-primary/80"
          >
            확인
          </button>
        </div>
      </div>
    </div>
  );
};

export default Modal;

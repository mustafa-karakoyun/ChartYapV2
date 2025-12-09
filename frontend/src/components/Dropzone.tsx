import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileType, Image as ImageIcon } from 'lucide-react';

interface DropzoneProps {
  onDrop: (files: File[]) => void;
  accept: Record<string, string[]>;
  label: string;
  icon?: 'data' | 'image';
  preview?: string | null;
}

export const Dropzone: React.FC<DropzoneProps> = ({ onDrop, accept, label, icon = 'data', preview }) => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop,
    accept,
    multiple: false
  });

  return (
    <div 
      {...getRootProps()} 
      className={`
        border-2 border-dashed h-64 flex flex-col items-center justify-center cursor-pointer transition-all
        relative overflow-hidden
        ${isDragActive ? 'border-[var(--swiss-red)] bg-red-50' : 'border-black hover:border-[var(--swiss-red)]'}
      `}
    >
      <input {...getInputProps()} />
      
      {preview ? (
        <img src={preview} alt="Preview" className="absolute inset-0 w-full h-full object-cover opacity-50" />
      ) : null}

      <div className="z-10 bg-white/80 p-4 rounded backdrop-blur-sm text-center">
        {icon === 'data' ? <FileType size={32} className="mx-auto mb-2" /> : <ImageIcon size={32} className="mx-auto mb-2" />}
        <p className="font-bold uppercase text-sm">{label}</p>
        <p className="text-xs text-gray-500 mt-1">{isDragActive ? 'DROP HERE' : 'DRAG & DROP OR CLICK'}</p>
      </div>
    </div>
  );
};

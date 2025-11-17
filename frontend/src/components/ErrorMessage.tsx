interface ErrorMessageProps {
  message: string;
  onClose?: () => void;
}

export default function ErrorMessage({ message, onClose }: ErrorMessageProps) {
  return (
    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4 flex justify-between items-center">
      <span>{message}</span>
      {onClose && (
        <button onClick={onClose} className="text-red-700 hover:text-red-900">
          ×
        </button>
      )}
    </div>
  );
}


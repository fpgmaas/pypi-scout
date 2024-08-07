import React from "react";

interface ToggleSwitchProps {
  option1: string;
  option2: string;
  selectedOption: string;
  onToggle: (option: string) => void;
}

const ToggleSwitch: React.FC<ToggleSwitchProps> = ({
  option1,
  option2,
  selectedOption,
  onToggle,
}) => {
  return (
    <div className="flex space-x-4 bg-sky-900 p-2 rounded-lg shadow-md">
      <button
        className={`px-4 py-2 w-[80px] rounded ${
          selectedOption === option1
            ? "bg-white text-sky-900"
            : " bg-sky-950 text-white hover:bg-sky-700"
        }`}
        onClick={() => onToggle(option1)}
      >
        {option1}
      </button>
      <button
        className={`px-4 py-2 w-[80px] rounded ${
          selectedOption === option2
            ? "bg-white text-sky-900"
            : " bg-sky-950 text-white hover:bg-sky-700"
        }`}
        onClick={() => onToggle(option2)}
      >
        {option2}
      </button>
    </div>
  );
};

export default ToggleSwitch;

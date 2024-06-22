import React from "react";

const SupportButton: React.FC = () => {
  return (
    <a
      href="https://ko-fi.com/fpgmaas"
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-center p-2 border border-gray-700 rounded bg-gray-900 text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-700"
    >
      <img
        src="kofi.png"
        alt="Ko-fi logo"
        width="24"
        height="24"
        className="mr-2"
      />
      Support
    </a>
  );
};

export default SupportButton;

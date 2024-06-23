import { useState } from "react";
import GitHubButton from "./GitHubButton";
import SupportButton from "./SupportButton";
import { FaBars, FaTimes } from "react-icons/fa";

const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className="w-full flex justify-end items-center p-4 bg-sky-950">
      <div className="hidden md:flex space-x-4 ">
        <GitHubButton />
        <SupportButton />
      </div>
      <div className="md:hidden flex-grow flex justify-end">
        <button
          onClick={toggleMenu}
          className="text-white focus:outline-none focus:ring-2 focus:ring-sky-700"
        >
          {isMenuOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
        </button>
      </div>
      {isMenuOpen && (
        <div className="absolute top-16 right-4 bg-sky-900 p-4 rounded shadow-lg flex flex-col space-y-4 md:hidden">
          <GitHubButton />
          <SupportButton />
        </div>
      )}
    </header>
  );
};

export default Header;

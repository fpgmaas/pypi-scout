import React from "react";

interface InfoBoxProps {
  infoBoxVisible: boolean;
}

const InfoBox: React.FC<InfoBoxProps> = ({ infoBoxVisible }) => {
  if (!infoBoxVisible) return null;

  return (
    <div className="w-3/5 bg-gray-800 p-6 rounded-lg shadow-lg mt-4 text-white">
      <h2 className="text-2xl font-bold mb-2">How does this work?</h2>
      <p className="text-gray-300">
        This application allows you to search for Python packages on PyPI using
        natural language. An example query would be &quot;a package that creates
        plots and beautiful visualizations&quot;.
      </p>
      <br />
      <p className="text-gray-300">
        Once you click search, your query will be matched against the summary
        and the first part of the description of all PyPI packages with more
        than 50 weekly downloads. The results are then scored based on their
        similarity and their number of weekly downloads, and the best results
        are displayed in the table below.
      </p>
    </div>
  );
};

export default InfoBox;

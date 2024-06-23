import React from "react";

interface InfoBoxProps {
  infoBoxVisible: boolean;
}

const InfoBox: React.FC<InfoBoxProps> = ({ infoBoxVisible }) => {
  if (!infoBoxVisible) return null;

  return (
    <div className="w-3/5 bg-sky-900 p-6 rounded-lg shadow-lg mt-4 text-white">
      <h2 className="text-2xl text-bold mb-2 text-gray-100">
        How does this work?
      </h2>
      <p className="text-gray-100">
        This application allows you to search for Python packages on PyPI using
        natural language queries. For example, a query could be &quot;a package
        that creates plots and beautiful visualizations&quot;.
      </p>
      <br />
      <p className="text-gray-100">
        Once you click search, your query will be matched against the summary
        and the first part of the description of the ~100.000 most popular
        packages on PyPI, which includes all packages with at least ~100
        downloads per week. The results are then scored based on their
        similarity to the query and their number of weekly downloads, and the
        best results are displayed in the table below.
      </p>
    </div>
  );
};

export default InfoBox;

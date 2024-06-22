"use client";

import { useState } from "react";
import { handleSearch, sortResults } from "./utils/search";
import SearchResultsTable from "./components/SearchResultsTable";
import InfoBox from "./components/InfoBox";
import { ClipLoader } from "react-spinners";
import GitHubButton from "./components/GitHubButton";
import SupportButton from "./components/SupportButton";

interface Match {
  name: string;
  similarity: number;
  weekly_downloads: number;
  summary: string;
}

export default function Home() {
  const [text, setText] = useState<string>("");
  const [results, setResults] = useState<Match[]>([]);
  const [sortField, setSortField] = useState<string>("similarity");
  const [sortDirection, setSortDirection] = useState<string>("desc");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [infoBoxVisible, setInfoBoxVisible] = useState<boolean>(false);

  const handleSort = (field: string) => {
    const direction =
      sortField === field && sortDirection === "asc" ? "desc" : "asc";
    setSortField(field);
    setSortDirection(direction);
    setResults(sortResults(results, field, direction));
  };

  return (
    <main className="flex flex-col items-center justify-start min-h-screen p-4 space-y-4 max-w-[2200px] mx-auto relative">
      <header className="w-full flex justify-end p-4">
        <div className="flex space-x-4">
          <GitHubButton />
          <SupportButton />
        </div>
      </header>

      <div className="flex flex-col items-center text-center mb-4">
        <picture>
          <img
            alt="pypi-scout logo"
            width="420"
            height="220"
            src="./pypi.svg"
            className="mx-auto"
          ></img>
        </picture>
        <p className="text-lg text-gray-300 mt-2">
          Enter your query to search for Python packages
        </p>
      </div>

      <div className="flex flex-col items-center space-y-4 w-3/5 bg-gray-800 p-6 rounded-lg shadow-lg">
        <textarea
          className="w-full h-24 p-2 border border-gray-700 rounded resize-none overflow-auto focus:outline-none focus:ring-2 focus:ring-blue-700 bg-gray-700 text-white"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter your query here..."
        ></textarea>
        <button
          className="w-full max-w-[250px] p-2 border border-gray-700 rounded bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-700"
          onClick={() =>
            handleSearch(
              text,
              sortField,
              sortDirection,
              setResults,
              setLoading,
              setError,
            )
          }
        >
          Search
        </button>
        {loading && (
          <ClipLoader color={"#123abc"} loading={loading} size={50} />
        )}
        {error && <p className="text-red-500">{error}</p>}
      </div>

      <div className="w-full flex justify-center mt-6">
        <button
          className="w-full max-w-[250px] p-2 border border-gray-700 rounded bg-gray-600 text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-700"
          onClick={() => setInfoBoxVisible(!infoBoxVisible)}
        >
          {infoBoxVisible ? "Hide Info" : "How does this work?"}
        </button>
      </div>

      <InfoBox infoBoxVisible={infoBoxVisible} />

      {results.length > 0 && (
        <div className="w-full flex justify-center mt-6">
          <div className="w-11/12 bg-gray-800 p-6 rounded-lg shadow-lg flex flex-col items-center">
            <SearchResultsTable
              results={results}
              sortField={sortField}
              sortDirection={sortDirection}
              onSort={handleSort}
            />
          </div>
        </div>
      )}
    </main>
  );
}

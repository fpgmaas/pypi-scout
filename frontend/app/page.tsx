"use client";

import { useState } from "react";
import { handleSearch, sortResults } from "./utils/search";
import SearchResultsTable from "./components/SearchResultsTable";
import InfoBox from "./components/InfoBox";
import { ClipLoader } from "react-spinners";
import Header from "./components/Header";

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

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSearch(
        text,
        sortField,
        sortDirection,
        setResults,
        setLoading,
        setError,
      );
    }
  };

  return (
    <div className="min-h-screen w-full bg-sky-950 flex flex-col items-center">
      <Header />
      <main className="w-full max-w-[1800px] flex flex-col items-center p-4 md:p-12 lg:p-18 space-y-4">
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
          <p className="text-gray-100 text-xl ">
            Find packages on PyPI with natural language queries
          </p>
        </div>

        <div className="flex flex-col items-center space-y-4 w-full max-w-3xl bg-sky-900 p-6 rounded-lg shadow-lg">
          <textarea
            className="placeholder-gray-400 w-full h-24 p-2 border border-sky-900 rounded resize-none overflow-auto focus:outline-none focus:ring-2 focus:ring-sky-800 bg-white text-sky-950"
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe what you are looking for... "
          ></textarea>
          <button
            className="w-full max-w-[250px] p-2 border border-sky-900 rounded bg-sky-950 text-white hover:bg-sky-700 hover:outline-none hover:ring-1 hover:ring-sky-700"
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
            <ClipLoader color={"#ffffff"} loading={loading} size={70} />
          )}
          {error && <p className="text-red-500">{error}</p>}
        </div>

        <div className="w-full flex justify-center mt-6">
          <button
            className="w-full max-w-[250px] p-2 border border-sky-700 rounded bg-sky-800 text-white hover:bg-sky-700 focus:outline-none focus:ring-2 focus:ring-sky-700"
            onClick={() => setInfoBoxVisible(!infoBoxVisible)}
          >
            {infoBoxVisible ? "Hide Info" : "How does this work?"}
          </button>
        </div>

        <InfoBox infoBoxVisible={infoBoxVisible} />

        {results.length > 0 && (
          <div className="w-full flex justify-center mt-6">
            <div className="w-full max-w-[1800px] bg-sky-900 p-6 rounded-lg shadow-lg flex flex-col items-center">
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
    </div>
  );
}

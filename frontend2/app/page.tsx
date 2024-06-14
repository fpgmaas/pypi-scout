"use client";

import { useState } from "react";
import axios from "axios";
import SearchResultsTable from "../components/SearchResultsTable";
import { ClipLoader } from "react-spinners";

export default function Home() {
  const [text, setText] = useState("");
  const [results, setResults] = useState([]);
  const [sortField, setSortField] = useState("weekly_downloads");
  const [sortDirection, setSortDirection] = useState("desc");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await axios.post(
        "http://localhost:8000/search",
        {
          query: text,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );
      const sortedResults = response.data.matches.sort(
        (a, b) => b.weekly_downloads - a.weekly_downloads,
      );
      setResults(sortedResults);
    } catch (error) {
      setError("Error fetching search results.");
      console.error("Error fetching search results:", error);
    } finally {
      setLoading(false);
    }
  };

  const sortResults = (field) => {
    const direction =
      sortField === field && sortDirection === "asc" ? "desc" : "asc";
    const sorted = [...results].sort((a, b) => {
      if (a[field] < b[field]) return direction === "asc" ? -1 : 1;
      if (a[field] > b[field]) return direction === "asc" ? 1 : -1;
      return 0;
    });
    setResults(sorted);
    setSortField(field);
    setSortDirection(direction);
  };

  return (
    <main className="flex flex-col items-center justify-start min-h-screen p-4 space-y-4 bg-gray-100">
      <header className="w-full text-center mb-4">
        <h1 className="text-4xl font-bold p-2 mt-4">✨PyPi Package Finder</h1>
        <p className="text-lg text-gray-600">
          Enter your query to search for Python packages
        </p>
      </header>
      <div className="flex flex-col items-center space-y-4 w-3/5 bg-white p-6 rounded-lg shadow-lg">
        <textarea
          className="w-full h-24 p-2 border rounded resize-none overflow-auto focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter your query here..."
        ></textarea>
        <button
          className="w-[250px] p-2 border rounded bg-blue-500 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          onClick={handleSearch}
        >
          Search
        </button>
        {loading && (
          <ClipLoader color={"#123abc"} loading={loading} size={50} />
        )}
        {error && <p className="text-red-500">{error}</p>}
      </div>

      {results.length > 0 && (
        <div className="w-full flex justify-center mt-6">
          <div className="w-11/12 bg-white p-6 rounded-lg shadow-lg flex flex-col items-center">
            <p className="mb-4 text-gray-700">
              Displaying the {results.length} most similar results:
            </p>
            <SearchResultsTable
              results={results}
              sortField={sortField}
              sortDirection={sortDirection}
              onSort={sortResults}
            />
          </div>
        </div>
      )}
    </main>
  );
}

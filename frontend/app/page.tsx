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
  const [infoBoxVisible, setInfoBoxVisible] = useState(false);

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
      const fetchedResults = response.data.matches;
      setResults(sortResults(fetchedResults, sortField, sortDirection));
    } catch (error) {
      setError("Error fetching search results.");
      console.error("Error fetching search results:", error);
    } finally {
      setLoading(false);
    }
  };

  const sortResults = (data, field, direction) => {
    return [...data].sort((a, b) => {
      if (a[field] < b[field]) return direction === "asc" ? -1 : 1;
      if (a[field] > b[field]) return direction === "asc" ? 1 : -1;
      return 0;
    });
  };

  const handleSort = (field) => {
    const direction =
      sortField === field && sortDirection === "asc" ? "desc" : "asc";
    setSortField(field);
    setSortDirection(direction);
    setResults(sortResults(results, field, direction));
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

      <div className="w-full flex justify-center mt-6">
        <button
          className="w-[250px] p-2 border rounded bg-gray-300 hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500"
          onClick={() => setInfoBoxVisible(!infoBoxVisible)}
        >
          {infoBoxVisible ? "Hide Info" : "How does this work?"}
        </button>
      </div>

      {infoBoxVisible && (
        <div className="w-3/5 bg-white p-6 rounded-lg shadow-lg mt-4">
          <h2 className="text-2xl font-bold mb-2">How does this work?</h2>
          <p className="text-gray-700">
            This application allows you to search for Python packages on PyPi
            using natural language. So an example query would be "a package that
            creates plots and beautiful visualizations". Once you click search,
            your query will be matched against the summary and the first part of
            the description of all PyPi packages with more than 50 weekly
            downloads, and the 50 most similar results will be displayed in a
            table below.
          </p>
        </div>
      )}

      {results.length > 0 && (
        <div className="w-full flex justify-center mt-6">
          <div className="w-11/12 bg-white p-6 rounded-lg shadow-lg flex flex-col items-center">
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

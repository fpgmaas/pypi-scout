import React from "react";
import { FaExternalLinkAlt } from "react-icons/fa"; // Import the icon

interface Match {
  name: string;
  similarity: number;
  weekly_downloads: number;
  summary: string;
}

interface SearchResultsTableProps {
  results: Match[];
  sortField: string;
  sortDirection: string;
  onSort: (field: string) => void;
}

const SearchResultsTable: React.FC<SearchResultsTableProps> = ({
  results,
  sortField,
  sortDirection,
  onSort,
}) => {
  const getSortIndicator = (field: string) => {
    return sortField === field ? (sortDirection === "asc" ? "▲" : "▼") : "";
  };

  return (
    <div className="overflow-x-auto w-full">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th
              className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer whitespace-nowrap"
              onClick={() => onSort("name")}
            >
              <div className="flex items-center">
                Name <span className="ml-1">{getSortIndicator("name")}</span>
              </div>
            </th>
            <th
              className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer whitespace-nowrap"
              onClick={() => onSort("similarity")}
            >
              <div className="flex items-center">
                Similarity{" "}
                <span className="ml-1">{getSortIndicator("similarity")}</span>
              </div>
            </th>
            <th
              className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer whitespace-nowrap"
              onClick={() => onSort("weekly_downloads")}
            >
              <div className="flex items-center">
                Weekly Downloads{" "}
                <span className="ml-1">
                  {getSortIndicator("weekly_downloads")}
                </span>
              </div>
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Summary
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Link
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {results.map((result, index) => (
            <tr key={index} className="hover:bg-gray-100">
              <td className="px-4 py-2 whitespace-nowrap">{result.name}</td>
              <td className="px-4 py-2 whitespace-nowrap">
                {result.similarity.toFixed(3)}
              </td>
              <td className="px-4 py-2 whitespace-nowrap">
                {result.weekly_downloads.toLocaleString()}
              </td>
              <td className="px-4 py-2 whitespace-normal break-words">
                {result.summary}
              </td>
              <td className="px-4 py-2 whitespace-nowrap">
                <a
                  href={`https://pypi.org/project/${result.name}/`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 hover:underline flex items-center"
                >
                  <FaExternalLinkAlt className="mr-1" />
                  PyPI
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SearchResultsTable;
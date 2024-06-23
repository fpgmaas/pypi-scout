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

  const truncateText = (text: string, maxLength: number) => {
    return text.length > maxLength
      ? `${text.substring(0, maxLength)}...`
      : text;
  };

  return (
    <div className="overflow-x-auto w-full">
      <table className="min-w-full divide-y divide-sky-800">
        <thead className="bg-sky-950">
          <tr>
            <th
              className="px-4 py-2 text-left text-xs font-medium text-gray-200 uppercase tracking-wider cursor-pointer whitespace-nowrap"
              onClick={() => onSort("name")}
            >
              <div className="flex items-center">
                Name <span className="ml-1">{getSortIndicator("name")}</span>
              </div>
            </th>
            <th
              className="px-4 py-2 text-left text-xs font-medium text-gray-200 uppercase tracking-wider cursor-pointer whitespace-nowrap"
              onClick={() => onSort("similarity")}
            >
              <div className="flex items-center">
                Similarity{" "}
                <span className="ml-1">{getSortIndicator("similarity")}</span>
              </div>
            </th>
            <th
              className="px-4 py-2 text-left text-xs font-medium text-gray-200 uppercase tracking-wider cursor-pointer whitespace-nowrap"
              onClick={() => onSort("weekly_downloads")}
            >
              <div className="flex items-center">
                Weekly Downloads{" "}
                <span className="ml-1">
                  {getSortIndicator("weekly_downloads")}
                </span>
              </div>
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-200 uppercase tracking-wider">
              Summary
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-200 uppercase tracking-wider">
              Link
            </th>
          </tr>
        </thead>
        <tbody className="bg-sky-900 divide-y divide-sky-800">
          {results.map((result, index) => (
            <tr key={index} className="hover:bg-sky-800">
              <td className="px-4 py-2 whitespace-nowrap text-gray-200">
                {truncateText(result.name, 20)}
              </td>
              <td className="px-4 py-2 whitespace-nowrap text-gray-200">
                {result.similarity.toFixed(3)}
              </td>
              <td className="px-4 py-2 whitespace-nowrap text-gray-200">
                {result.weekly_downloads.toLocaleString()}
              </td>
              <td className="px-4 py-2 whitespace-normal break-words text-gray-200 min-w-[400px]">
                {result.summary}
              </td>
              <td className="px-4 py-2 whitespace-nowrap">
                <a
                  href={`https://pypi.org/project/${result.name}/`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sky-500 hover:underline flex items-center hover:text-orange-800"
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

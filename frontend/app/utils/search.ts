import axios from "axios";

interface Match {
  name: string;
  similarity: number;
  weekly_downloads: number;
  summary: string;
}

export const handleSearch = async (
  query: string,
  sortField: string,
  sortDirection: string,
  setResults: React.Dispatch<React.SetStateAction<Match[]>>,
  setLoading: React.Dispatch<React.SetStateAction<boolean>>,
  setError: React.Dispatch<React.SetStateAction<string>>,
) => {
  setLoading(true);
  setError("");
  try {
    const response = await axios.post(
      "http://localhost:8000/search",
      {
        query: query,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      },
    );
    const fetchedResults: Match[] = response.data.matches;
    setResults(sortResults(fetchedResults, sortField, sortDirection));
  } catch (error) {
    setError("Error fetching search results.");
    console.error("Error fetching search results:", error);
  } finally {
    setLoading(false);
  }
};

export const sortResults = (
  data: Match[],
  field: string,
  direction: string,
): Match[] => {
  return [...data].sort((a, b) => {
    if (a[field] < b[field]) return direction === "asc" ? -1 : 1;
    if (a[field] > b[field]) return direction === "asc" ? 1 : -1;
    return 0;
  });
};

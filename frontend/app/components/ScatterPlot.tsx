import React from "react";
import { Scatter } from "react-chartjs-2";
import {
  Chart,
  Tooltip,
  Legend,
  PointElement,
  LinearScale,
  Title,
  LogarithmicScale,
  CategoryScale,
} from "chart.js";

Chart.register(
  Tooltip,
  Legend,
  PointElement,
  LinearScale,
  Title,
  LogarithmicScale,
  CategoryScale,
);

interface Match {
  name: string;
  similarity: number;
  weekly_downloads: number;
  summary: string;
}

interface ScatterPlotProps {
  results: Match[];
}

const getColor = (
  similarity: number,
  downloads: number,
  minSim: number,
  maxSim: number,
  minLogDownloads: number,
  maxLogDownloads: number,
) => {
  const baseColor = [54, 162, 235]; // Blue
  const highlightColor = [255, 99, 132]; // Red

  const normalizedSimilarity = (similarity - minSim) / (maxSim - minSim);
  const normalizedDownloads =
    (Math.log10(downloads) - minLogDownloads) /
    (maxLogDownloads - minLogDownloads);

  const weight = Math.min(
    ((normalizedSimilarity + normalizedDownloads) / 2) * 1.5,
    1,
  );

  const color = baseColor.map((base, index) =>
    Math.round(base + weight * (highlightColor[index] - base)),
  );

  return `rgba(${color.join(",")}, 0.8)`;
};

const getPointSize = (
  similarity: number,
  downloads: number,
  minSim: number,
  maxSim: number,
  minLogDownloads: number,
  maxLogDownloads: number,
) => {
  const normalizedSimilarity = (similarity - minSim) / (maxSim - minSim);
  const normalizedDownloads =
    (Math.log10(downloads) - minLogDownloads) /
    (maxLogDownloads - minLogDownloads);

  const minSize = 2;
  const size = Math.min(
    (normalizedSimilarity + normalizedDownloads) * 10 + minSize,
    25,
  );
  return size;
};

const ScatterPlot: React.FC<ScatterPlotProps> = ({ results }) => {
  const similarities = results.map((result) => result.similarity);
  const downloads = results.map((result) => result.weekly_downloads);
  const logDownloads = downloads.map((download) => Math.log10(download));

  const minSim = Math.min(...similarities);
  const maxSim = Math.max(...similarities);
  const minLogDownloads = Math.min(...logDownloads);
  const maxLogDownloads = Math.max(...logDownloads);

  const data = {
    datasets: [
      {
        label: "Packages",
        data: results.map((result) => ({
          x: result.similarity,
          y: result.weekly_downloads,
          name: result.name,
          summary: result.summary,
          link: `https://pypi.org/project/${result.name}/`,
        })),
        backgroundColor: results.map((result) =>
          getColor(
            result.similarity,
            result.weekly_downloads,
            minSim,
            maxSim,
            minLogDownloads,
            maxLogDownloads,
          ),
        ),
        borderColor: results.map((result) =>
          getColor(
            result.similarity,
            result.weekly_downloads,
            minSim,
            maxSim,
            minLogDownloads,
            maxLogDownloads,
          ),
        ),
        pointRadius: results.map((result) =>
          getPointSize(
            result.similarity,
            result.weekly_downloads,
            minSim,
            maxSim,
            minLogDownloads,
            maxLogDownloads,
          ),
        ),
        hoverBackgroundColor: results.map((result) =>
          getColor(
            result.similarity,
            result.weekly_downloads,
            minSim,
            maxSim,
            minLogDownloads,
            maxLogDownloads,
          ),
        ),
        hoverBorderColor: results.map((result) =>
          getColor(
            result.similarity,
            result.weekly_downloads,
            minSim,
            maxSim,
            minLogDownloads,
            maxLogDownloads,
          ),
        ),
        pointHoverRadius: 15,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      tooltip: {
        callbacks: {
          title: (context: any) => {
            const dataPoint = context[0].raw;
            return dataPoint.name;
          },
          beforeLabel: (context: any) => {
            const dataPoint = context.raw;
            return dataPoint.summary;
          },
          label: () => "",
          afterLabel: (context: any) => {
            const dataPoint = context.raw;
            return `\nWeekly downloads: ${dataPoint.y.toLocaleString()}`;
          },
        },
        titleFont: { size: 16, weight: "bold" },
        bodyFont: { size: 14 },
        footerFont: { size: 12 },
        displayColors: false,
        backgroundColor: "rgba(0, 0, 0, 0.8)",
        padding: 10,
        bodySpacing: 4,
        titleAlign: "left",
        bodyAlign: "left",
        footerAlign: "left",
      },
      legend: {
        display: false,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Similarity",
          color: "#FFFFFF",
          font: {
            size: 24,
          },
        },
        ticks: {
          color: "#FFFFFF",
        },
      },
      y: {
        title: {
          display: true,
          text: "Weekly Downloads",
          color: "#FFFFFF",
          font: {
            size: 24,
          },
        },
        ticks: {
          callback: function (value: any) {
            return value.toLocaleString();
          },
          color: "#FFFFFF",
          maxTicksLimit: 5,
        },
        type: "logarithmic",
      },
    },
    onClick: (event: any, elements: any) => {
      if (elements.length > 0) {
        const elementIndex = elements[0].index;
        const datasetIndex = elements[0].datasetIndex;
        const link = data.datasets[datasetIndex].data[elementIndex].link;
        window.open(link, "_blank");
      }
    },
    onHover: (event: any, elements: any) => {
      event.native.target.style.cursor = elements[0] ? "pointer" : "default";
    },
    elements: {
      point: {
        hoverRadius: 15,
      },
    },
  };

  const plugins = [
    {
      id: "customLabels",
      afterDatasetsDraw: (chart: any) => {
        const ctx = chart.ctx;
        chart.data.datasets.forEach((dataset: any) => {
          dataset.data.forEach((dataPoint: any, index: number) => {
            const { x, y } = chart
              .getDatasetMeta(0)
              .data[index].tooltipPosition();
            ctx.fillStyle = "white";
            ctx.textAlign = "center";
            ctx.fillText(dataPoint.name, x, y - 10);
          });
        });
      },
    },
  ];

  return (
    <div className="overflow-auto w-full flex flex-col items-center">
      <h2 className="text-center text-white mb-4">
        Click a package to go to PyPI
      </h2>
      <hr className="border-gray-500 mb-4 w-full" />
      <div className="w-full h-[600px]">
        <Scatter data={data} options={options} plugins={plugins} />
      </div>
    </div>
  );
};

export default ScatterPlot;

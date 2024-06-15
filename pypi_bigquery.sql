WITH recent_downloads AS (
  SELECT
    project,
    COUNT(*) AS download_count
  FROM
    `bigquery-public-data.pypi.file_downloads`
  WHERE
    DATE(timestamp) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 28 DAY) AND CURRENT_DATE()
  GROUP BY
    project
  HAVING
    download_count >= 250
)
SELECT
  rd.project AS name,
  dm.description AS description,
  dm.summary AS summary,
  dm.version AS latest_version,
  rd.download_count AS number_of_downloads
FROM
  recent_downloads rd
JOIN
  `bigquery-public-data.pypi.distribution_metadata` dm
ON
  rd.project = dm.name
WHERE
  dm.upload_time = (
    SELECT
      MAX(upload_time)
    FROM
      `bigquery-public-data.pypi.distribution_metadata` sub_dm
    WHERE
      sub_dm.name = dm.name
  )
ORDER BY
  rd.download_count DESC;

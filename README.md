# pypi-llm

[![Release](https://img.shields.io/github/v/release/fpgmaas/pypi-llm)](https://img.shields.io/github/v/release/fpgmaas/pypi-llm)
[![Build status](https://img.shields.io/github/actions/workflow/status/fpgmaas/pypi-llm/main.yml?branch=main)](https://github.com/fpgmaas/pypi-llm/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/fpgmaas/pypi-llm/branch/main/graph/badge.svg)](https://codecov.io/gh/fpgmaas/pypi-llm)
[![Commit activity](https://img.shields.io/github/commit-activity/m/fpgmaas/pypi-llm)](https://img.shields.io/github/commit-activity/m/fpgmaas/pypi-llm)
[![License](https://img.shields.io/github/license/fpgmaas/pypi-llm)](https://img.shields.io/github/license/fpgmaas/pypi-llm)

This is a template repository for Python projects that use Poetry for their dependency management.

- **Github repository**: <https://github.com/fpgmaas/pypi-llm/>
- **Documentation** <https://fpgmaas.github.io/pypi-llm/>

## Getting started with your project

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:fpgmaas/pypi-llm.git
git push -u origin main
```

Finally, install the environment and the pre-commit hooks with

```bash
make install
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPi or Artifactory, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/codecov/).

## Releasing a new version

- Create an API Token on [Pypi](https://pypi.org/).
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/fpgmaas/pypi-llm/settings/secrets/actions/new).
- Create a [new release](https://github.com/fpgmaas/pypi-llm/releases/new) on Github.
- Create a new tag in the form `*.*.*`.

For more details, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/cicd/#how-to-trigger-a-release).

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).

---

## total

```sql
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
```

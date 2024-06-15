# ✨PyPI Scout

PyPI Scout helps you find PyPI packages using natural language prompts powered by Large Language Models (LLMs).

![Demo](./demo.gif)

The project works by collecting project summaries and descriptions for all packages on PyPI with more than 50 weekly downloads. These are then converted into vector representations using [Sentence Transformers](https://www.sbert.net/). When the user enters a query, it is converted into a vector representation, and the most similar package descriptions are fetched from the vector database. Additional weight is given to weekly downloads before presenting the results to the user in a dashboard.

## Getting Started

### Prerequisites

1. **Create a `.env` File**

   Copy the `.env.template` to create a new `.env` file:

   ```sh
   cp .env.template .env
   ```

2. **Set Up Pinecone**

   Since PyPI Scout uses [Pinecone](https://www.pinecone.io/) as the vector database, register for a free account on their website. Obtain your API key from [here](https://docs.pinecone.io/guides/get-started/quickstart) and add it to your `.env` file.

### Build and Setup

#### 1. **Run the Setup Script**

The setup script will:

- Download and process the PyPI dataset and store the results in the `data` directory.
- Set up your Pinecone index.
- Create vector embeddings for the PyPI dataset and upsert them to the Pinecone index.

There are three methods to run the setup script, dependent on if you have a NVIDIA GPU and [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) installed. Please run the setup script using the method that is applicable for you:

- [Option 1: Using Poetry](SETUP.md#option-1-using-poetry)
- [Option 2: Using Docker with NVIDIA GPU and NVIDIA Container Toolkit](SETUP.md#option-2-using-docker-with-nvidia-gpu-and-nvidia-container-toolkit)
- [Option 3: Using Docker without NVIDIA GPU and NVIDIA Container Toolkit](SETUP.md#option-3-using-docker-without-nvidia-gpu-and-nvidia-container-toolkit)

> [!IMPORTANT]
> Since the creation of embedding vectors can take quite some time, by default only the 10% of the dataset with the most weekly downloads is used. To use the full dataset, set `FRAC_DATA_TO_INCLUDE` to `1.0` in `pypi_scout/config.py`

#### 2. **Run the Application**

Start the application using Docker Compose:

```sh
docker-compose up
```

After a short while, your application will be live at [http://localhost:3000](http://localhost:3000).

## Data

The dataset for this project is created using the [PyPI dataset on Google BigQuery](https://console.cloud.google.com/marketplace/product/gcp-public-data-pypi/pypi?project=regal-net-412415). The SQL query used can be found in [pypi_bigquery.sql](./pypi_bigquery.sql). The resulting dataset is available as a CSV file on [Google Drive](https://drive.google.com/file/d/1huR7-VD3AieBRCcQyRX9MWbPLMb_czjq/view?usp=sharing).

## Running the setup script

Next to running the setup script with

```sh
poetry install
poetry run python pypi_scout/scripts/setup.py
```

you can also run it using the Docker image. Below are two options, depending on whether you have an NVIDIA GPU and the NVIDIA Container Toolkit installed.

### Option 1: With NVIDIA GPU and NVIDIA Container Toolkit

Build the Docker image with

```sh
docker build -t pypi-scout .
```

Then run:

```sh
docker run --rm \
  --gpus all \
  --env-file .env \
  -v $(pwd)/data:/code/data \
  pypi-scout \
  python /code/pypi_scout/scripts/setup.py
```

**Option 2: Without NVIDIA GPU and NVIDIA Container Toolkit**

If you do not have an NVIDIA GPU or the NVIDIA Container Toolkit installed, omit `--gpus all` in the command above:

```sh
docker run --rm \
  --env-file .env \
  -v $(pwd)/data:/code/data \
  pypi-scout \
  python /code/pypi_scout/scripts/setup.py
```

Alternatively, you can use Poetry to set up the environment and run the setup script directly:

```sh
poetry install
poetry run python /code/pypi_scout/scripts/setup.py
```

---

By following these instructions, you'll have PyPI Scout up and running, enabling you to find the best PyPI packages with ease using natural language queries. Enjoy exploring!

# ✨PyPi Scout

<video width="820">
  <source src="./pypi-scout.mov" type="video/mov">
</video>

![](./pypi-scout.mov)

PyPi Scout helps you find PyPi packages using natural language prompts powered by Large Language Models (LLMs).

The project works by collecting project summaries and descriptions for all packages on PyPI with more than 50 weekly downloads. These are then converted into vector representations using [Sentence Transformers](https://www.sbert.net/). When the user enters a query, it is converted into a vector representation, and the most similar package descriptions are fetched from the vector database. Additional weight is given to weekly downloads before presenting the results to the user in a dashboard.

## Getting Started

### Prerequisites

1. **Create a `.env` File**

   Copy the `.env.template` to create a new `.env` file:

   ```sh
   cp .env.template .env
   ```

2. **Set Up Pinecone**

   Since PyPi Scout uses [Pinecone](https://www.pinecone.io/) as the vector database, register for a free account on their website. Obtain your API key from [here](https://docs.pinecone.io/guides/get-started/quickstart) and add it to your `.env` file.

### Build and Setup

1. **Build the Docker Image**

   From the root of the project, build the Docker image:

   ```sh
   docker build -t pypi-scout .
   ```

2. **Run the Setup Script**

   Execute the setup script to download and process the PyPI dataset, set up your Pinecone index, create vector embeddings, and upsert them to the Pinecone index:

   ```sh
   docker run --rm \
     --env-file .env \
     -v $(pwd)/data:/code/data \
     pypi-scout \
     python /code/pypi_scout/scripts/setup.py
   ```

   This script will:

   - Download and process the PyPI dataset and store the results in the `data` directory
   - Set up your Pinecone index
   - Create vector embeddings for the PyPI dataset and upsert them to the Pinecone index

3. **Run the Application**

   Start the application using Docker Compose:

   ```sh
   docker-compose up
   ```

   After a short while, your application will be live at [http://localhost:3000](http://localhost:3000).

## Data

The dataset for this project is created using the [PyPI dataset on Google BigQuery](https://console.cloud.google.com/marketplace/product/gcp-public-data-pypi/pypi?project=regal-net-412415). The SQL query used can be found in [pypi_bigquery.sql](./pypi_bigquery.sql). The resulting dataset is available as a CSV file on [Google Drive](https://drive.google.com/file/d/1huR7-VD3AieBRCcQyRX9MWbPLMb_czjq/view?usp=sharing).

---

By following these instructions, you'll have PyPi Scout up and running, enabling you to find the best PyPi packages with ease using natural language queries. Enjoy exploring!

# Running the Setup Script

The setup script will:

- Download and process the PyPI dataset and store the results in the `data` directory.
- Create vector embeddings for the PyPI dataset.
- If the `STORAGE_BACKEND` environment variable is set to `BLOB`: Upload the datasets to blob storage.

There are three ways to run the setup script:

### Option 1: Using Poetry

You can run the setup script using a virtual environment with Poetry. This method will automatically utilize your GPU for the vector embeddings if it is detected.

1. Install dependencies and set up the virtual environment:

   ```sh
   poetry install
   ```

2. Run the setup script:

   ```sh
   poetry run python pypi_scout/scripts/setup.py
   ```

### Option 2: Using Docker with NVIDIA GPU and NVIDIA Container Toolkit

If you have an NVIDIA GPU and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) installed, follow these steps:

1. Build the Docker image:

   ```sh
   docker build -t pypi-scout .
   ```

2. Run the setup script in a Docker container with GPU support:

   ```sh
   docker run --rm \
      --gpus all \
     --env-file .env \
     -v $(pwd)/data:/code/data \
     --entrypoint "/bin/bash" \
     pypi-scout \
     -c "python /code/pypi_scout/scripts/setup.py"
   ```

### Option 3: Using Docker without NVIDIA GPU and NVIDIA Container Toolkit

If you do not have an NVIDIA GPU or the NVIDIA Container Toolkit installed, follow these steps:

1. Build the Docker image:

   ```sh
   docker build -f DockerfileCPU -t pypi-scout .
   ```

2. Run the setup script in a Docker container without GPU support:

   ```sh
   docker run --rm \
     --env-file .env \
     -v $(pwd)/data:/code/data \
     --entrypoint "/bin/bash" \
     pypi-scout \
     -c "python /code/pypi_scout/scripts/setup.py"
   ```

### Running the Application

After setting up the dataset, start the application using Docker Compose:

```sh
docker-compose up
```

After a short while, your application will be live at [http://localhost:3000](http://localhost:3000).

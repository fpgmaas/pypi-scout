# ✨PyPi Scout

https://drive.google.com/file/d/1huR7-VD3AieBRCcQyRX9MWbPLMb_czjq/view?usp=sharing

# setup

```sh
cp .env.template .env
```

add API token

```
docker build -t pypi-scout .
```

```
docker run --rm \
  --env-file .env \
  -v $(pwd)/data:/code/data \
  pypi-scout \
  python /code/pypi_scout/scripts/setup.py
```

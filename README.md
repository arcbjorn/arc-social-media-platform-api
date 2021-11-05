# Social media platform backend

using FastAPI

## Clone repository

```sh
git clone <this-repo>
```

### Make sure you have Python installed

```sh
python -V
```

## Setup virtual environment (venv)

```sh
python3 -m venv venv
```

## Activate venv and install dependencies

**Important: check the correct way of activation depending on your shell. Consult [here.](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)** (I use [fish shell](https://fishshell.com/))

```sh
source ./venv/bin/activate
python -m pip install -r requirements.txt
```

## Run app in Development mode

```sh
uvicorn app.main:app --reload
```

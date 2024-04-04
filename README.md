## Getting Started!

## Set up .env
Make a copy of the `.env.example` file and name it as `.env` in the same directory. Remember to fill in the necessary fields

### Create a virtual environment if you have yet to.

```
python3 -m venv venv
```

### Activate virtual environment

#### MAC users

```
source venv/bin/activate
```

#### Windows users

```
venv\Scripts\activate
```

### Install the latest dependencies used by others

```
pip install -r requirements.txt
```

### Start the server

```
cd app
uvicorn main:app --reload --port 8081
```

## Before pushing

### Update requirements.txt with the latest dependencies you installed

```
pip freeze > requirements.txt
```

### Add test cases

Make sure that there is a `__init__.py` file at every level of the test cases

Run the following command at the root of the repository
`pytest`

### Check style
Run the following command at the root of the repository
`black .`


## Common issues

### No module named 'app'

export PYTHONPATH="/Users/{MAC_NAME}/brain:$PYTHONPATH"


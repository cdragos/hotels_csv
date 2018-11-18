# Hotels

Convert data from hotels.csv in a given format. The output is based on the
format and it can be output.yml (for YAML) or output.db (for sqlite).

## Requirements

* Python 3.x
* Virtualenv

## Installation

1. Create a virtualenv with python3:

    ```virtualenv venv -p python3```

2. Activate the virtualenv:

    ```. venv/bin/activate```

3. Install python requirements with pip

    ```pip install -r requirements.txt```

## Run the converter
    python manage.py convert hotels.csv --output_format=yaml
    python manage.py convert hotels.csv --output_format=sqlite

## Running the tests
    python -m unittest hotels.tests

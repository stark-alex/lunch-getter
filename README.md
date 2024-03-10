# Lunch Getter

## Pre-reqs

* python3
* pip3
* virtualenv

## How run locally

From the src directory

* Create virtual env:

`virtualenv venv`

* Activate virtual env:

`source venv/bin/activate`

* Install the module requirements

`pip install -r ./requirements.txt`

* Export env var inputs

```
export SCHOOL_ID=<school id>
export PERSON_ID=<person id>
```

* Run the program:

`./lunch_getter.py`
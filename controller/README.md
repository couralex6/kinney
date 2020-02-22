## Installation

### Setup virtual environment

```python3 -m venv venv```

### Start environment

```. venv/bin/activate```

### Install dependencies

```pip install -r requirements.txt```

### Change directory to `chargepoint/`

```cd chargepoint```

### Start flask app

```python -m flask run --host=0.0.0.0```

### Configure your system

1) Edit config.yaml to specify your ChargePoint station group and staion IDs. Whether you would like to stream load data, where to save files, enable DEBUG logging etc.

2) Specify the following environment variables, possibly adding  them to your .bashrc:

    ```export CP_USERNAME='changeme'```

    ```export CP_PASSWORD='changeme'```

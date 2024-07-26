# Documentation API

## Introduction

This API aims to expose a machine learning model. It contains a single endpoint allowing a prediction to be made from the explanatory variables. It includes token-based authentication.



## Code Structure

- **main.py**: The entry point of the API application. It initializes the FastAPI application, sets up routing, and may include logic for starting the server.
- **predict.py**: Contains the logic for making predictions with the machine learning model. It likely defines FastAPI endpoints to receive prediction requests and return the results.
- **opentelemetry_setup.py**: Configures OpenTelemetry for monitoring and tracing the application. It helps in collecting metrics and traces for monitoring and debugging.
- **utils.py**: Contains utility functions used across the API application. This may include authentication logic, helpers for data processing, etc.
- **database.py**: contains the logic for connecting to and interacting with the database. It may include functions for creating database sessions, data models, and CRUD operations
- **model_loader.py**: contains the logic for loading the machine learning model from a file or external source. It's used to prepare the model for predictions.
- **launch_app.sh**: A shell script used to launch the API application. It checks if the machine learning model is loaded and, if not, runs a script to load it before starting the API with Uvicorn.

### Authentification

You need a token to use the predict endpoint of the api.
To get this token you need to call the generate_token("admin") function in the api/utils.py file

```bash
python3 -m api.utils
```

## Endpoints

### Prediction

- **URL**: `/predict`
- **Method**: `POST`
- **Authentication required**: Yes
- **Request body**: Model-specific data for prediction.
- **Response**: Prediction result.
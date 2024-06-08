import json
from typing import Any

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger

# Imports from our deployed model as package
from regression_model import __version__ as model_version
from regression_model.predict import make_prediction

from app import __version__, schemas
from app.config import settings

api_router = APIRouter()

# Health endpoint
# We have specified schemas.Health response model
@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """
    Root Get
    """

    # We have defined a response schema
    health = schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    )

    # We are returning that as dictionary
    # Under the hood FAST API will do the conversion to json for a json response
    return health.dict()

# Predict endpoint
# The FAST API can capture inputs and response models of our different endpoints 
@api_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
# Expected input make use of this schema
async def predict(input_data: schemas.MultipleHouseDataInputs) -> Any:
    """
    Make house price predictions with the TID regression model
    """

    # We load the input into pandas dataframe
    # jsonable_encoder handles loading the pydantic data into json that is expected by pandas
    input_df = pd.DataFrame(jsonable_encoder(input_data.inputs))

    # Advanced: You can improve performance of your API by rewriting the
    # `make prediction` function to be async and using await here.
    logger.info(f"Making prediction on inputs: {input_data.inputs}")

    # Replacing numpy nan with None so that pydantic can work with them correctly
    results = make_prediction(input_data=input_df.replace({np.nan: None}))

    if results["errors"] is not None:
        logger.warning(f"Prediction validation error: {results.get('errors')}")
        raise HTTPException(status_code=400, detail=json.loads(results["errors"]))

    logger.info(f"Prediction results: {results.get('predictions')}")

    # If the result does not contain any error then the result will be returned in the format specified in our response model
    # This is FAST API and pydantic working together  
    return results

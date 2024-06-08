from typing import Generator

import pandas as pd
import pytest
from fastapi.testclient import TestClient

# Imports from our deployed model as package
from regression_model.config.core import config
from regression_model.processing.data_manager import load_dataset

from app.main import app

# We have two fixtures

@pytest.fixture(scope="module")
def test_data() -> pd.DataFrame:
    # test_data_file from out deployed package
    return load_dataset(file_name=config.app_config.test_data_file)


@pytest.fixture()
def client() -> Generator:
    # Standard pattern of setting up a FAST API test client 
    with TestClient(app) as _client:
        yield _client
        app.dependency_overrides = {}

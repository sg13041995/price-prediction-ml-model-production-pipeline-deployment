from pydantic import BaseModel

# We have defined the Health schema
# Just like Health class also inherits from the pydantic BaseModel
class Health(BaseModel):
    name: str
    api_version: str
    model_version: str

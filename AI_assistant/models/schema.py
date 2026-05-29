from pydantic import BaseModel
from typing import List

class CookingRequest(BaseModel):
    prompt: str

class RecipeResponse(BaseModel):
    dish: str
    ingredients: List[str]
    steps: List[str]
    cook_time: str
    difficulty: str
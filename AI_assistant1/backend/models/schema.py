from pydantic import BaseModel, Field
from typing import List, Optional


class ChatMessage(BaseModel):
    role: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)


class CookingRequest(BaseModel):
    messages: List[ChatMessage] = Field(
        default_factory=list
    )

    prompt: Optional[str] = None


class RecipeResponse(BaseModel):
    dish: str
    ingredients: List[str]
    steps: List[str]
    cook_time: str
    difficulty: str
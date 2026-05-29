from fastapi import APIRouter
from models.schema import CookingRequest
from services.ollama_services import generate_recipe
from services.ingredients import detect_ingredients
from services.recoomendation_services import recommend_recipe
from services.memory_services import save_recipe, get_history

router = APIRouter()

@router.post("/ask")
def ask_ai(data: CookingRequest):

    recipe = generate_recipe(data.prompt)

    save_recipe(
        recipe["dish"],
        recipe["ingredients"]
    )

    return recipe

@router.post("/ingredients")
def ingredients(data: CookingRequest):

    detected = detect_ingredients(data.prompt)

    recommendations = recommend_recipe(detected)

    return {
        "ingredients": detected,
        "recoomendations": recommendations
    }

@router.get("/history")
def history():

    history = get_history()

    return history
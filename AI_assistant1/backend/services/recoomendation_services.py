from services.memory_services import get_all_recipes
from services.ollama_services import query_ollama


def recommend_recipe(user_ingredients):

    recipes = get_all_recipes()

    results = []

    for recipe in recipes:

        recipe_ingredients = [
            ingredient.strip().lower()
            for ingredient in recipe.ingredients.split(",")
        ]

        score = len(
            set(user_ingredients) &
            set(recipe_ingredients)
        )

        results.append({
            "recipe": recipe.recipe_name,
            "score": score
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # Top 3 matches
    top_matches = results[:3]

    # If database has no useful match
    if not top_matches or top_matches[0]["score"] == 0:

        prompt = f"""
        The user has these ingredients:

        {', '.join(user_ingredients)}

        Recommend 3 recipes.

        For each recipe provide:
        - Recipe Name
        - Short Description

        Return in JSON format.
        """

        return query_ollama(prompt)

    # Database matches found
    prompt = f"""
    User ingredients:

    {', '.join(user_ingredients)}

    Top matching recipes:

    {top_matches}

    Explain why these recipes are suitable.

    Return JSON format.
    """

    explanation = query_ollama(prompt)

    return {
        "database_matches": top_matches,
        "ai_explanation": explanation
    }
    
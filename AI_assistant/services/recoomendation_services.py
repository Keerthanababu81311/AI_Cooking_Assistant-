recipes = {
    "Omelette": ["egg", "onion"],
    "Veg Sandwich": ["bread", "tomato", "onion"],
    "Pasta": ["pasta", "tomato", "cheese"]
}

def recommend_recipe(user_ingredients):

    results = []

    for recipe, ingredients in recipes.items():

        score = len(
            set(user_ingredients) &
            set(ingredients)
        )

        results.append({
            "recipe": recipe,
            "score": score
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results
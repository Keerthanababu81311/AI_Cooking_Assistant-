from database.db import SessionLocal, RecipeHistory

def save_recipe(recipe_name, ingredients):

    db = SessionLocal()

    recipe = RecipeHistory(
        recipe_name=recipe_name,
        ingredients = ", ".join(ingredients))

    db.add(recipe)
    db.commit()
    db.close()

def get_history():

    db = SessionLocal()

    history = db.query(RecipeHistory).all()

    db.close()

    return history
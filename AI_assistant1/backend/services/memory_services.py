from database.db import SessionLocal, RecipeHistory


def save_recipe(recipe_name, ingredients):

    db = SessionLocal()

    try:

        recipe = RecipeHistory(
            recipe_name=recipe_name,
            ingredients=", ".join(ingredients)
        )

        db.add(recipe)
        db.commit()
        db.refresh(recipe)

        return recipe

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


def get_history():

    db = SessionLocal()

    try:

        return (
            db.query(RecipeHistory)
            .order_by(RecipeHistory.id.desc())
            .all()
        )

    finally:

        db.close()


def get_all_recipes():

    return get_history()


def delete_recipe(recipe_id):

    db = SessionLocal()

    try:

        recipe = (
            db.query(RecipeHistory)
            .filter(
                RecipeHistory.id == recipe_id
            )
            .first()
        )

        if recipe:

            db.delete(recipe)
            db.commit()

            return True

        return False

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


def clear_history():

    db = SessionLocal()

    try:

        db.query(
            RecipeHistory
        ).delete()

        db.commit()

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()
from mcp.server.fastmcp import FastMCP
import requests
import re
import time  
mcp = FastMCP("Health-Service")

storage = {
    "steps": 0
}


@mcp.tool()
def get_calories(food: str) -> str:
    """Fetch calorie data from Open Food Facts."""
    food_name = food.lower().strip()

    KCAL_KEYS = ["energy-kcal_100g", "energy-kcal", "energy-kcal_value"]

    def extract_kcal(nutriments: dict):
        for key in KCAL_KEYS:
            val = nutriments.get(key)
            if val is not None:
                try:
                    f = float(val)
                    if f > 0:
                        return round(f)
                except (ValueError, TypeError):
                    continue
        return None

    headers = {"User-Agent": "HealthFoodAgent/1.0 (test@test.com)"}

    for attempt in range(3):  # retry up to 3 times
        try:
            response = requests.get(
                "https://world.openfoodfacts.org/cgi/search.pl",
                headers=headers,
                params={
                    "search_terms": food_name,
                    "search_simple": 1,
                    "action": "process",
                    "json": 1,
                    "page_size": 50,
                    "fields": "product_name,generic_name,nutriments",
                    "sort_by": "unique_scans_n",
                },
                timeout=15,
            )

            if response.status_code == 503:
                time.sleep(2 ** attempt)  # wait 1s, 2s, 4s between retries
                continue

            data = response.json()
            products = data.get("products", [])

            if not products:
                return f"No products found for '{food}'."

            checked = []
            for product in products:
                product_name = (product.get("product_name") or "").strip()
                generic_name = (product.get("generic_name") or "").strip()
                name = product_name or generic_name or food
                nutriments = product.get("nutriments") or {}
                kcal = extract_kcal(nutriments)
                checked.append(name)
                if kcal is not None:
                    return f"{name} contains approximately {kcal} kcal per 100g."

            return f"Found products for '{food}' but none had calorie data. Checked: {', '.join(checked[:5])}"

        except Exception as error:
            return f"Could not fetch calorie data: {error}"

    return f"Open Food Facts is temporarily unavailable (503). Try again in a moment."

@mcp.tool()
def get_recipe(ingredient: str, cuisine: str = "") -> str:
    """Fetch a full recipe from TheMealDB. Returns ingredients and instructions."""

    ingredient = ingredient.lower().strip()
    cuisine = cuisine.strip()

    def fetch_details(meal_id: str) -> str:
        try:
            detail_res = requests.get(
                "https://www.themealdb.com/api/json/v1/1/lookup.php",
                params={"i": meal_id},
                timeout=10,
            ).json()
            meal = detail_res.get("meals", [{}])[0]
            if not meal:
                return "Could not find recipe details."

            name = meal.get("strMeal", "Unknown Dish")
            raw_instructions = meal.get("strInstructions", "No instructions available.")
            
            # Clean up instructions: normalize newlines and strip whitespace
            instructions = raw_instructions.replace("\r\n", "\n").replace("\r", "\n").strip()
            
            # If instructions lack newlines but contain step numbers (e.g., "1 ... 2 ..."), 
            # insert newlines before those numbers to help the agent format them.
            if instructions.count('\n') < 2:
                instructions = re.sub(r'(?<!^)(\d+\.|\d+\s+)', r'\n\1', instructions)
            
            ingredients = []
            for i in range(1, 21):
                ing = meal.get(f"strIngredient{i}")
                meas = meal.get(f"strMeasure{i}")
                if ing and ing.strip():
                    ingredients.append(f"- {ing.strip()} ({meas.strip() if meas else ''})")
            
            ing_list = "\n".join(ingredients)
            return (
                f"### Recipe: {name}\n\n"
                f"**Ingredients:**\n{ing_list}\n\n"
                f"**Instructions:**\n{instructions}"
            )
        except Exception as e:
            return f"Error fetching details: {e}"

    try:
        # Try ingredient search first
        ingredient_response = requests.get(
            "https://www.themealdb.com/api/json/v1/1/filter.php",
            params={"i": ingredient},
            timeout=10,
        ).json()

        if ingredient_response.get("meals"):
            meal_id = ingredient_response["meals"][0]["idMeal"]
            return fetch_details(meal_id)

        # Try meal name search
        search_response = requests.get(
            "https://www.themealdb.com/api/json/v1/1/search.php",
            params={"s": ingredient},
            timeout=10,
        ).json()

        if search_response.get("meals"):
            meal_id = search_response["meals"][0]["idMeal"]
            return fetch_details(meal_id)

        # Try cuisine search if cuisine was given
        if cuisine:
            cuisine_response = requests.get(
                "https://www.themealdb.com/api/json/v1/1/filter.php",
                params={"a": cuisine},
                timeout=10,
            ).json()

            if cuisine_response.get("meals"):
                meal_id = cuisine_response["meals"][0]["idMeal"]
                return fetch_details(meal_id)

        return (
            f"TheMealDB could not find a recipe for {ingredient}. "
            f"Try chicken, egg, rice, beef, pasta, salmon, tomato, or cheese."
        )

    except Exception as error:
        return f"Could not fetch recipe data from TheMealDB: {error}"


@mcp.tool()
def manage_steps(action: str, value: int = 0) -> str:
    """Manage step count. action can be add, get, or reset."""

    action = action.lower().strip()

    if action == "add":
        if value <= 0:
            return "Please provide a positive number of steps."

        storage["steps"] += value
        return f"Added {value} steps. Current total: {storage['steps']} steps."

    if action == "get":
        return f"Current step total: {storage['steps']} steps."

    if action == "reset":
        storage["steps"] = 0
        return "Step count reset to 0."

    return "Invalid action. Use add, get, or reset."


if __name__ == "__main__":
    mcp.run()
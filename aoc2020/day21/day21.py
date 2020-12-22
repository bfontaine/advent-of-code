from collections import Counter
from typing import Dict, Set, Tuple, List


def read_food(filename):
    food = []

    with open(filename) as f:
        for line in f:
            parts = line.strip(")\n").split(" (contains ")
            ingredients = parts[0].split()
            allergens = parts[1].split(", ")
            food.append((set(ingredients), set(allergens)))

    return food


def run(food):
    # ingredient -> occurrences
    ingredients = Counter()
    # allergen -> possible ingredients
    allergens: Dict[str, Set[str]] = {}

    for food_ingredients, food_allergens in food:
        ingredients.update({ingredient: 1 for ingredient in food_ingredients})

        for allergen in food_allergens:
            if allergen in allergens:
                allergens[allergen].intersection_update(food_ingredients)
            else:
                allergens[allergen] = set(food_ingredients)

    matched_allergens_ingredients: List[Tuple[str, str]] = []

    while allergens:
        for allergen in list(allergens):
            allergen_ingredients = allergens[allergen]

            if len(allergen_ingredients) == 1:
                ingredient = list(allergen_ingredients)[0]
                matched_allergens_ingredients.append((allergen, ingredient))
                del ingredients[ingredient]
                del allergens[allergen]

                for allergen2 in allergens:
                    if ingredient in allergens[allergen2]:
                        allergens[allergen2].remove(ingredient)

    print("Problem #1:", sum(ingredients.values()))

    matched_allergens_ingredients.sort()
    print("Problem #2:", ",".join([ingredient for _, ingredient in matched_allergens_ingredients]))


if __name__ == '__main__':
    run(read_food("input.txt"))

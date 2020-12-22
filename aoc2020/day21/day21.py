from collections import Counter
from typing import Dict, Set


def read_food(filename):
    food = []

    with open(filename) as f:
        for line in f:
            parts = line.strip(")\n").split(" (contains ")
            ingredients = parts[0].split()
            allergens = parts[1].split(", ")
            food.append((set(ingredients), set(allergens)))

    return food


def problem1(food):
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

    while allergens:
        for allergen in list(allergens):
            allergen_ingredients = allergens[allergen]

            if len(allergen_ingredients) == 1:
                ingredient = list(allergen_ingredients)[0]
                print(ingredient, "contains", allergen)
                del ingredients[ingredient]
                del allergens[allergen]

                for allergen2 in allergens:
                    if ingredient in allergens[allergen2]:
                        allergens[allergen2].remove(ingredient)

    print(ingredients.keys(), sum(ingredients.values()))


if __name__ == '__main__':
    problem1(read_food("input.txt"))

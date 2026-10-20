import json
import os
import random
from faker import Faker

# Number of lines
NUM_LINES = 200
# File name
FILE_NAME = "products.json"

fake = Faker()

CATEGORIES = ["airbag", "boot", "helmet", "jacket", "glove", "pants", "full suit"]
BRANDS = [
    "Alpinestars", "Dainese", "Rukka", "Roviron", "Klim", "Spidi", "Icon", "Shoei", "AGV", "HJC",
    "Arai", "Scorpion", "Shark", "Bell", "LS2", "Nolan", "X-Lite", "Schuberth", "Held", "RST",
    "IXS", "Macna", "Modeka", "Bering", "Furygan", "TCX", "Forma", "Sidi", "Gaerne", "Revit"
]
COLORS = ["black", "white", "red", "blue", "green", "yellow", "orange", "gray"]

def generate_product():
    category = random.choice(CATEGORIES)
    brand = random.choice(BRANDS)
    color = random.sample(COLORS, k=random.randint(1, 3))
    product_name = f"{category.capitalize()} {brand} {fake.word().capitalize()}"
    price = round(random.uniform(50, 1000), 2)
    description = fake.sentence(random.randint(30, 100))
    # [3XS, XXS, XS, S, M, L, XL, XXL, 3XL]
    size_availability = []
    for i in range(0,9):
        if random.randint(0,5):
            size_availability.append(random.randint(1,25))
        else:
            size_availability.append(0)

    return {
        "nombre": product_name,
        "precio": price,
        "descripcion": description,
        "categoria": category,
        "marca": brand,
        "colores": color,
        "dispo_tallas": size_availability
    }


def generate_dataset(num_products:int):
    return [generate_product() for _ in range(num_products)]


def save_to_json(filename:str, num_products:int):
    data = generate_dataset(num_products)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Dataset saved to {filename}")


if __name__ == "__main__":
    if not os.path.exists("datasets"):
        os.makedirs("datasets")
    save_to_json("datasets/" + FILE_NAME, NUM_LINES)
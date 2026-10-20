import random

class Availability:
    def __init__(self, products):
        self.availability = True
        self.products = products
        self.category_translation = {
            "guante": "glove", "guantes": "glove",
            "pantalon": "pant", "pantalones": "pant",
            "chaqueta": "jacket", "chaquetas": "jacket",
            "bota": "boot", "botas": "boot",
            "mono": "full suit", "monos": "full suit",
            "casco": "helmet", "cascos": "helmet",
            "airbag": "airbag", "airbags": "airbag"
        }
        self.color_translation = {
            "rojo": "red", "azul": "blue", "verde": "green", "negro": "black",
            "blanco": "white", "amarillo": "yellow", "naranja": "orange",
            "morado": "purple", "rosa": "pink", "gris": "gray", "marron": "brown"
        }
        self.yes_responses = [
            "Sí, tenemos {available_items} producto(s) que cumplen tus criterios.",
            "Claro, hay {available_items} producto(s) disponibles que coinciden con tus criterios.",
            "Por supuesto, tenemos {available_items} producto(s) que cumplen con lo que buscas.",
            "Sí, hay {available_items} producto(s) que coinciden con tus criterios."
        ]
        self.no_responses = [
            "Lo siento, no tenemos productos que cumplan esos criterios en este momento.",
            "Desafortunadamente, no hay productos disponibles que coincidan con tus criterios.",
            "No contamos con productos que cumplan con lo que buscas en este momento.",
            "Lamentablemente, no hay productos disponibles que coincidan con lo que buscas."
        ]

    def get_availability(self, name, brand, category, size, color, tokens) -> int:

        final_products = self.products.copy()

        remove_products = []

        for product in final_products:
            if not (name is None):
                if not(product.name in tokens):
                    remove_products.append(product)

        for product in remove_products:
            final_products.remove(product)
            
        remove_products = []

        for product in final_products:
            if brand is not None:
                if product.brand.lower() != brand.lower():
                    remove_products.append(product)

        for product in remove_products:
            final_products.remove(product)
        
        remove_products = []

        for product in final_products:
            if not (category is None):
                if not(product.category in tokens):
                    remove_products.append(product)

        for product in remove_products:
            final_products.remove(product)

        remove_products = []

        for product in remove_products:
            final_products.remove(product)

        for product in final_products:            
            if not (size is None):
                if product.size_availability[size] == 0:
                    remove_products.append(product)

        for product in remove_products:
            final_products.remove(product)

        remove_products = []

        for product in final_products:
            if not (color is None):
                appears = 0
                for color in product.colors:
                    if color in tokens:
                        appears = 1
                        break
                if appears == 0:
                    remove_products.append(product)

        for product in remove_products:
            final_products.remove(product)

        quantity = len(final_products)  

        return quantity
    
    def answer_availability(self, tokens):
        categories = {"airbag", "airbags", "glove", "gloves", "guante", "guantes", "pant", "pants", "pantalon", "pantalones", "jacket", "jackets", "chaqueta", "chaquetas", "boot", "boots", "bota", "botas", "full suit", "full suits", "mono", "monos", "helmet", "helmets", "casco", "cascos"}
        brands = {"scorpion", "sidi", "spidi", "ixs", "bell", "schuberth", "gaerne", "held", "dainese", "modeka", "tcx", "rukka", "nolan", "alpinestars", "shoei", "rst", "furygan", "shark", "x-lite", "ls2", "klim", "forma", "macna", "agv", "revit", "roviron", "bering", "icon", "arai", "hjc"}
        colors = {"red", "rojo", "blue", "azul", "green", "verde", "black", "negro", "white", "blanco", "yellow", "marillo", "orange", "naranja", "purple", "morado", "pink", "rosa", "gray", "gris", "brown", "marron"}
        sizes = ["xxxs", "xxs", "xs", "s", "m", "l", "xl", "xxl", "xxxl"]

        name = None
        brand = None
        category = None
        size = None
        color = None
        
        # Traduce tokens de español a inglés si es necesario
        translated_tokens = []
        for token in tokens:
            t = token.lower()
            # Traducción de categorías
            if t in self.category_translation:
                translated_tokens.append(self.category_translation[t])
            # Traducción de colores
            elif t in self.color_translation:
                translated_tokens.append(self.color_translation[t])
            else:
                translated_tokens.append(t)

        for token in translated_tokens:
            t = token.lower()
            if t in brands:
                brand = t
            elif t in categories:
                category = t
            elif t in colors:
                color = t
            elif t in sizes:
                size = sizes.index(t)

        for product in self.products:
            if product.name.lower() in [tok.lower() for tok in tokens]:
                name = product.name
                break

        available_items = self.get_availability(name, brand, category, size, color, translated_tokens)

        if available_items > 0:
            # Devolver una respuesta aleatoria de las respuestas afirmativas
            response = random.choice(self.yes_responses).format(available_items=available_items)
            return response
        else:
            response = random.choice(self.no_responses)
            return response

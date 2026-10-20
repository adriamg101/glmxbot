from token_extractor import tokenize

class Replacement:
    def __init__(self, products: list, token_list: list):
        self.products = products
        self.token_list = token_list
        self.category_translation = {
            "guante": "glove", "guantes": "glove",
            "pantalon": "pants", "pantalones": "pants",
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

    def extract_filters(self):
        categories = {"airbag", "glove", "pants", "jacket", "boot", "full suit", "helmet"}
        brands = {"scorpion", "sidi", "spidi", "ixs", "bell", "schuberth", "gaerne", "held", "dainese", "modeka", "tcx", "rukka", "nolan", "alpinestars", "shoei", "rst", "furygan", "shark", "x-lite", "ls2", "klim", "forma", "macna", "agv", "revit", "roviron", "bering", "icon", "arai", "hjc"}
        colors = {"red", "blue", "green", "black", "white", "yellow", "orange", "purple", "pink", "gray", "brown"}

        # Traducir tokens al inglés si es necesario
        translated_tokens = []
        for token in self.token_list:
            t = token.lower()
            if t in self.category_translation:
                translated_tokens.append(self.category_translation[t])
            elif t in self.color_translation:
                translated_tokens.append(self.color_translation[t])
            else:
                translated_tokens.append(t)

        # Usar tokens traducidos
        category = next((word for word in translated_tokens if word in categories), None)
        brand = next((word for word in translated_tokens if word in brands), None)
        max_price = None
        color = next((word for word in translated_tokens if word in colors), None)

        for i in range(len(translated_tokens) - 1):
            if translated_tokens[i].isdigit() and translated_tokens[i + 1].lower() in {"€", "euro", "euros"}:
                max_price = float(translated_tokens[i])
                break

        if category is None:
            category = self.ask_user("¿Qué tipo de artículo quieres para tu reemplazo?", categories)
        if brand is None:
            brand = self.ask_user("¿Cuál es tu marca favorita?", brands)
        if max_price is None:
            max_price = self.ask_price()
        if color is None:
            color = self.ask_user("¿Lo quieres de algún color específico?", colors)

        return category, brand, max_price, color

    def ask_user(self, question, valid_options):
        response = input(question + " ")
        tokens = tokenize(response)
        # Traducir los tokens
        translated = []
        for token in tokens:
            t = token.lower()
            if t in self.category_translation:
                translated.append(self.category_translation[t])
            elif t in self.color_translation:
                translated.append(self.color_translation[t])
            else:
                translated.append(t)
        return next((word for word in translated if word in valid_options), None)

    def ask_price(self):
        response = input("¿Tienes en mente algún precio máximo? ")
        tokens = tokenize(response)
        for i in range(len(tokens) - 1):
            if tokens[i].isdigit() and tokens[i + 1].lower() in {"€", "euro", "euros"}:
                return float(tokens[i])
        return float('inf')

    def find_replacement(self):
        category, brand, max_price, color = self.extract_filters()

        filtered_products = [p for p in self.products
                             if (category is None or p.category.lower() == category.lower())
                             and (brand is None or p.brand.lower() == brand.lower())
                             and p.price <= max_price
                             and (color is None or color.lower() in map(str.lower, p.colors))]

        if filtered_products:
            print("Productos encontrados:")
            for p in filtered_products:
                print(f"{p.name} - {p.price}€ - {p.colors} - {p.brand}")
        else:
            print("No hay productos que coincidan con tus criterios.")

import re

class Budget:
    # Regex
    CATEGORIES = [r"(airbag)\w*", r"(bota)\w*", r"(casco)\w*", r"(chaqueta)\w*", r"(guante)\w*", r"(pantalon)\w*", r"(traje)\w*"]
    CATEGORY_NAMES = ["airbag", "boot", "helmet", "jacket", "glove", "pants", "full suit"]
    CATEGORY_NAMES_SPANISH = ["airbag", "botas", "casco", "chaqueta", "guantes", "pantalones", "traje completo"]
    REGEX_CATEGORIES = rf"({'|'.join(CATEGORIES)})"

    non_new_categories = True
    wanted_categories = [False, True, True, True, True, True, False]  # Categorías por defecto
    category_products = {}

    def __init__(self, products: list):
        self.products = products.sort(key=lambda product: product.price)
        for product in products:
            if product.category not in self.category_products:
                self.category_products[product.category] = []
            self.category_products[product.category].append(product)

    def budgetWithoutCategory(self):
        print("Presupuestos propuestos:")
        # Presupuesto gama alta
        total_sum = 0
        print("\n\tGama alta:")
        for i in range(0, len(self.CATEGORIES)):
            if self.wanted_categories[i]:
                index = len(self.category_products[self.CATEGORY_NAMES[i]]) - 1
                total_sum += self.category_products[self.CATEGORY_NAMES[i]][index].price
                print(f" - {self.CATEGORY_NAMES_SPANISH[i].upper()}: {self.category_products[self.CATEGORY_NAMES[i]][index].name} ({self.category_products[self.CATEGORY_NAMES[i]][index].price}€)")
        print(f"\nPrecio total: {round(total_sum, 2)}")

        # Presupuesto gama media
        total_sum = 0
        print("\n\tGama media:")
        for i in range(0, len(self.CATEGORIES)):
            if self.wanted_categories[i]:
                index = (len(self.category_products[self.CATEGORY_NAMES[i]]) - 1) // 2
                total_sum += self.category_products[self.CATEGORY_NAMES[i]][index].price
                print(f" - {self.CATEGORY_NAMES_SPANISH[i].upper()}: {self.category_products[self.CATEGORY_NAMES[i]][index].name} ({self.category_products[self.CATEGORY_NAMES[i]][index].price}€)")
        print(f"\nPrecio total: {round(total_sum, 2)}")

        # Presupuesto gama baja
        total_sum = 0
        print("\n\tGama baja:")
        for i in range(0, len(self.CATEGORIES)):
            if self.wanted_categories[i]:
                total_sum += self.category_products[self.CATEGORY_NAMES[i]][0].price
                print(f" - {self.CATEGORY_NAMES_SPANISH[i].upper()}: {self.category_products[self.CATEGORY_NAMES[i]][0].name} ({self.category_products[self.CATEGORY_NAMES[i]][0].price}€)")
        print(f"\nPrecio total: {round(total_sum, 2)}")

    def budgetWithCategories(self, budget: float):
        # Calcular el presupuesto mínimo posible
        min_budget = 0
        for i in range(0, len(self.CATEGORIES)):
            if self.wanted_categories[i]:
                min_budget += self.category_products[self.CATEGORY_NAMES[i]][0].price

        if budget < min_budget:
            print("El presupuesto es muy bajo para los productos que quieres, esta es la combinación más económica:")
            total_sum = 0
            for i in range(0, len(self.CATEGORIES)):
                if self.wanted_categories[i]:
                    total_sum += self.category_products[self.CATEGORY_NAMES[i]][0].price
                    print(f" - {self.CATEGORY_NAMES_SPANISH[i].upper()}: {self.category_products[self.CATEGORY_NAMES[i]][0].name} ({self.category_products[self.CATEGORY_NAMES[i]][0].price}€)")
            print(f"\nPrecio total: {round(total_sum, 2)}")
            return

        # Calcular el presupuesto máximo posible
        max_budget = 0
        for i in range(0, len(self.CATEGORIES)):
            if self.wanted_categories[i]:
                max_budget += self.category_products[self.CATEGORY_NAMES[i]][-1].price

        # Búsqueda binaria para ajustar al presupuesto
        total_sum = max_budget + 1
        por = 100
        while total_sum > budget and por >= 0:
            total_sum = 0
            for i in range(0, len(self.CATEGORIES)):
                if self.wanted_categories[i]:
                    index = ((len(self.category_products[self.CATEGORY_NAMES[i]]) - 1) * por) // 100
                    total_sum += self.category_products[self.CATEGORY_NAMES[i]][index].price
            if total_sum > budget:
                por -= 10

        total_sum = 0
        for i in range(0, len(self.CATEGORIES)):
            if self.wanted_categories[i]:
                index = ((len(self.category_products[self.CATEGORY_NAMES[i]]) - 1) * por) // 100
                total_sum += self.category_products[self.CATEGORY_NAMES[i]][index].price
                print(f" - {self.CATEGORY_NAMES_SPANISH[i].upper()}: {self.category_products[self.CATEGORY_NAMES[i]][index].name} ({self.category_products[self.CATEGORY_NAMES[i]][index].price}€)")
        print(f"\nPrecio total: {round(total_sum, 2)}")

    def checkInputForBudget(self, tokens: list):
        budget = -1
        for token in tokens:
            if self.non_new_categories and re.match(self.REGEX_CATEGORIES, token):
                self.non_new_categories = False
                for i in range(0, len(self.wanted_categories)):
                    self.wanted_categories[i] = False
            for i in range(0, len(self.CATEGORIES)):
                if re.match(self.CATEGORIES[i], token):
                    self.wanted_categories[i] = True
            # Si hay un número, es el presupuesto
            if re.match(r"^\d+([.,]\d+)?", token):
                # Borrem els caracters que no siguin ni digits ni nombres
                token = re.sub(r'[^.,\d]', '', token)
                # Pasem la quantitat com a budgeet
                budget = float(token.replace(',', '.'))

        # Dependiendo de los datos introducidos
        if self.non_new_categories and budget < 0:
            self.budgetWithoutCategory()
        else:
            if budget < 0:
                self.budgetWithoutCategory()
            else:
                self.budgetWithCategories(budget)

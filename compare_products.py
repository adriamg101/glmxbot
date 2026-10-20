from product import Product
import json
from transformers import pipeline


class CompareProducts:
    def __init__(self, products: list):
        self.products = products
        self.qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")
        self.context = "\n".join([
            f"Nombre: {p.name}. Precio: {p.price} euros. Categoría: {p.category}. Marca: {p.brand}. "
            f"Colores: {', '.join(p.colors)}. Tallas: {', '.join([str(t) for t in p.size_availability])}."
            for p in self.products
        ])

    def compare_products(self) -> None:
        while True:
            pregunta = input("Haz una pregunta sobre los productos (o 'salir'): ")
            if pregunta.lower() in ["salir", "exit"]:
                break

            respuesta = self.qa_pipeline({
                'question': pregunta,
                'context': self.context
            })

            print(f"Bot: {respuesta['answer']}")


if __name__ == '__main__':
    products = list()
    with open("datasets/products.json") as json_file:
        data = json.load(json_file)
        for data_product in data:
            product = Product(data_product['nombre'], data_product['precio'], data_product['descripcion'],
                              data_product['categoria'], data_product['marca'], data_product['colores'],
                              data_product['dispo_tallas'])
            products.append(product)
    compareProducts = CompareProducts(products)
    compareProducts.compare_products()

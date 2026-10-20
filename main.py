import json
import re

import spacy
import language_tool_python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

import Promotions
import paymentMethods
from budget import Budget
from compare_products import CompareProducts
from product import Product
from replacement import Replacement
from token_extractor import tokenize
import FrequentlyAskQuestions
from availability import Availability

SIMILARITY_THRESHOLD = 0.6

COLOR_RESET = '\033[0m'
COLOR_BLUE = '\033[94m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'

def read_dataset(filename: str) -> list:
    products = list()
    with open(filename) as json_file:
        data = json.load(json_file)
        for data_product in data:
            product = Product(data_product['nombre'], data_product['precio'], data_product['descripcion'],
                              data_product['categoria'], data_product['marca'], data_product['colores'],
                              data_product['dispo_tallas'])
            products.append(product)
    return products


def fix_mistakes(texto):
    matches = tool.check(texto)
    return language_tool_python.utils.correct(texto, matches)


def lemmatize(texto):
    doc = nlp(texto.lower())
    lemmas = []
    for token in doc:
        if not token.is_stop and not token.is_punct:
            lemmas.append(token.lemma_)
    lemmatized_text = " ".join(lemmas)
    return lemmatized_text


def load_training_data(ruta_json, nlp):
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    sentences = []
    intentions = []
    lemmatized_sentences = []

    for intention, examples in data.items():
        for sentence in examples:
            sentences.append(sentence)
            intentions.append(intention)
            # Lematizar aquí directamente
            doc = nlp(sentence.lower())
            lemmas = " ".join([t.lemma_ for t in doc if not t.is_stop and not t.is_punct])
            lemmatized_sentences.append(lemmas)

    return sentences, intentions, lemmatized_sentences


def process_user_input(user_text):
    if (user_text == ""): return "none_question"

    fixed_text = fix_mistakes(user_text)
    lemma_text = lemmatize(fixed_text)
    X_user = vectorizer.transform([lemma_text])
    intention = modelo.predict(X_user)[0]

    # Verificar similitud
    doc_usuario = nlp(user_text.lower())

    frases_de_intencion = [
        s for s, i in zip(sentences, intentions) if i == intention
    ]

    similitudes = [
        (nlp(frase.lower()).similarity(doc_usuario), frase)
        for frase in frases_de_intencion
    ]

    best_similarity, best_phrase = max(similitudes, key=lambda x: x[0])

    # TODO: Per testing
    # print(f"{COLOR_YELLOW}Similitud con mejor frase de intención: {best_similarity:.2f} - \"{best_phrase}\"")

    if best_similarity < SIMILARITY_THRESHOLD:
        # Si la similitud es molt baixa retornem que no s'ha entes la pregunta
        return "no_entiendo"

    return intention


if __name__ == '__main__':
    logo = f"""{COLOR_GREEN}
╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                    ║
║   ██████╗ ██████╗ ███████╗███████╗███╗   ██╗██╗      █████╗ ███╗   ██╗██████╗ ███╗   ███╗██╗  ██╗  ║
║  ██╔════╝ ██╔══██╗██╔════╝██╔════╝████╗  ██║██║     ██╔══██╗████╗  ██║██╔══██╗████╗ ████║╚██╗██╔╝  ║
║  ██║  ███╗██████╔╝█████╗  █████╗  ██╔██╗ ██║██║     ███████║██╔██╗ ██║██║  ██║██╔████╔██║ ╚███╔╝   ║
║  ██║   ██║██╔══██╗██╔══╝  ██╔══╝  ██║╚██╗██║██║     ██╔══██║██║╚██╗██║██║  ██║██║╚██╔╝██║ ██╔██╗   ║
║  ╚██████╔╝██║  ██║███████╗███████╗██║ ╚████║███████╗██║  ██║██║ ╚████║██████╔╝██║ ╚═╝ ██║██╔╝ ██╗  ║
║   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝  ║
║                                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""
    print(logo)

    filename = "datasets/products.json"
    products = read_dataset(filename)

    nlp = spacy.load("es_core_news_md")
    tool = language_tool_python.LanguageTool('es')

    sentences, intentions, lemmatized_sentences = load_training_data("datasets/intentions.json", nlp)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(lemmatized_sentences)

    modelo = MultinomialNB()
    modelo.fit(X, intentions)
    budget = Budget(products)

    print(COLOR_RESET, end="")
    text = input("Soy GreenLandMXBot en que puedo ayudarte?\n")

    while True:
        intention = process_user_input(text)
        filtered_tokens = tokenize(text)        

        print(COLOR_BLUE, end="")
  
        if intention == "comparar_productos":
            cp = CompareProducts(products)
            cp.compare_products(text)
        elif intention == "hacer_presupuesto":
            budget.checkInputForBudget(filtered_tokens)
        elif intention == "consultar_disponibilidad":
            availability = Availability(products)
            respuesta = availability.answer_availability(filtered_tokens)
            print(respuesta)
        elif intention == "informacion_producto":
            print("Intention: " + intention)
        elif intention == "seguimiento_pedido":
            print("Intention: " + intention)
        elif intention == "devolucion_producto":
            replacement_finder = Replacement(products, filtered_tokens)
            replacement_finder.find_replacement()
        elif intention == "recomendar_talla":
            print("Intention: " + intention)
        elif (re.match(r"\b(payment|shipping)_\w+\b", intention)):
            pm = paymentMethods.PaymentMethod()
            pm.answerQuestion(intention)
        elif re.match(r"^promo_", intention):
            promo = Promotions.Promotions()
            promo.answerQuestion(intention)
        elif (re.match(r"\baccount_\w+\b", intention)
              or re.match(r"\bcontact_\w+\b", intention)
              or re.match(r"\bgift_card_\w+\b", intention)):
            faq = FrequentlyAskQuestions.FrequentlyAskQuestions()
            faq.answerQuestion(intention)
        elif intention == "despedida":
            print("¡Hasta la próxima!")
            break

        # Mirem si la pregunta no era bona
        print(COLOR_RESET, end="")
        if intention == "no_entiendo":
            text = input("No he entendido la pregunta. ¿Podrías reformularla? ")
        elif intention == "saludo":
            text = input("Hola! ¿En que te puedo ayudar? ")
        elif intention == "none_question":
            text = input("> ")
        else:
            text = input("¿Necesitas algo más? ")


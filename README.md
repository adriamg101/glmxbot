# GreenLandMXBot

A Spanish-language customer-service chatbot for a motorcycle gear shop. It answers questions about stock, budgets, product comparisons, replacements, payment, shipping, promotions and account help, using a classic NLP pipeline instead of an LLM.

## How it works

Each message goes through four steps:

1. **Spelling correction.** LanguageTool fixes typos in the user's text.
2. **Lemmatization.** spaCy (`es_core_news_md`) lowercases the text, drops stop words and punctuation, and reduces words to their lemmas.
3. **Intent classification.** A TF-IDF vectorizer feeds a Multinomial Naive Bayes classifier trained on the example sentences in `datasets/intentions.json`.
4. **Confidence check.** The message is compared with the training sentences of the predicted intent using spaCy vector similarity. If the best match scores below 0.6, the bot asks the user to rephrase instead of guessing.

`main.py` then routes the intent to a handler module and loops until the user says goodbye.

## Features

| Intent | Module | What it does |
| --- | --- | --- |
| Product replacement | `replacement.py` | Asks for brand, maximum price and colour, then lists matching products |
| Budget | `budget.py` | Recommends products that fit a given maximum budget |
| Availability | `availability.py` | Checks stock for a product or category |
| Comparison | `compare_products.py` | Compares products from the catalogue |
| Payment and shipping | `paymentMethods.py` | Answers from `datasets/payment.json` |
| Promotions | `Promotions.py` | Answers from `datasets/promotions.json` |
| FAQ (account, contact, gift cards) | `FrequentlyAskQuestions.py` | Answers from the matching JSON files in `datasets/` |

Product information, order tracking and size recommendation are recognised as intents but not implemented yet. The bot only prints the detected intent for them.

The product catalogue is generated with Faker by `datasetGenerator.py`, so the data is synthetic.

## Stack

Python 3.8, spaCy, scikit-learn, language_tool_python, Faker, pandas.

## Setup

1. Install Python 3.8.
2. Create and activate a virtual environment:
   ```
   py -3.8 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
   On Windows you may need Microsoft Visual C++ 14.0 or later for some packages to build.

## Running it

1. Generate the product dataset. Run `datasetGenerator.py`, and edit `NUM_LINES` and `FILE_NAME` in the script to change the number of products or the output file. Re-running it overwrites the existing file.
2. Start the chatbot with `python main.py`.

## Example questions

**Replacement**

```
User: Quiero cambiar mis guantes por otros de otra marca
Bot:  ¿Cuál es tu marca favorita?
User: LS2
Bot:  ¿Tienes en mente algún precio máximo?
User: 900
Bot:  ¿Lo quieres de algún color específico?
User:
Bot:  Productos encontrados:
```

**Budget**

- `Tengo 1000 euros como maximo presupuesto, que recomiendas comprar?`

**Availability**

- `¿Hay stock de guantes de invierno?`
- `¿Teneis disponible el mono Alpinestars?`

**FAQ**

- `¿Dónde solicito la eliminación de mi cuenta?`
- `¿Puedo revisar las órdenes que he hecho antes?`

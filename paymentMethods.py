import json
import re

class PaymentMethod:
    PAYMENT_JSON = "datasets/payment.json"

    def loadAnswers(self, ruta_json: str):
        with open(ruta_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def answerQuestion(self, intention: str):
        if re.match(r"\b(payment|shipping)_\w+\b", intention):
            answers = self.loadAnswers(self.PAYMENT_JSON)
            print("\n" + answers[intention] + "\n")
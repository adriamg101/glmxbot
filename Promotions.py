import json
import re

class Promotions:
    PROMOTIONS_JSON = "datasets/promotions.json"

    def loadAnswers(self, ruta_json: str):
        with open(ruta_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def answerQuestion(self, intention: str):
        if re.match(r"\bpromo_\w+\b", intention):
            answers = self.loadAnswers(self.PROMOTIONS_JSON)
            print("\n" + answers[intention] + "\n")

import json
import re


class FrequentlyAskQuestions:
    ACCOUNT_JSON = "datasets/accountAnswers.json"
    CONTACT_JSON = "datasets/contactAnswers.json"
    GIFT_CARD_JSON = "datasets/giftCardAnswers.json"

    def loadAnswers(self, ruta_json: str):
        with open(ruta_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    def answerQuestion(self, intention: str):
        if re.match(r"\baccount_\w+\b", intention):
            answers = self.loadAnswers(self.ACCOUNT_JSON)
        elif re.match(r"\bcontact_\w+\b", intention):
            answers = self.loadAnswers(self.CONTACT_JSON)
        else: # r"\bgift_card_\w+\b"
            answers = self.loadAnswers(self.GIFT_CARD_JSON)

        print("\n" + answers[intention] + "\n")
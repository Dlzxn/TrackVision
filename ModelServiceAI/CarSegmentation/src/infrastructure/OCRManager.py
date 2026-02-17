import easyocr

from src.domain.OCRcontract import OCRAbstract

class OCRManager(OCRAbstract):
    def __init__(self):
        self.reader = easyocr.Reader(['ru', 'en'])

    def _get_number(self, frame):
        return self.reader.readtext(frame)

    def _get_result(self, result):
        if len(result) > 1:
            max_prob = max(result, key = lambda x: x[2])
            for (bbox, text, prob) in result:
                if prob == max_prob:
                    return text
            return ""

        elif len(result) == 1:
            return result[0][1]

        else:
            return ""


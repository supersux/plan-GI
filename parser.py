# OCR解耦在这里，基于BaseOperator进行扩展
import easyocr


class BaseOCRParser:
    def parse(self, file):
        pass


# 基于EasyOCR的实现
class EasyOCRParser(BaseOCRParser):
    def __init__(self):
        self.reader = easyocr.Reader(['en', 'ch_sim'])

    def parse(self, file):
        return self.reader.readtext(file)

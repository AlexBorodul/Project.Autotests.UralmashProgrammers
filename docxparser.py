from docx_parser import DocumentParser


class DocxParser:
    def __init__(self, path):
        self.path = path
        self.doc = {}

    def parse(self):
        infile = self.path
        self.doc = DocumentParser(infile)
        return self.doc

    def print_doc(self):
        for _type, item in self.doc:
            print(_type, item)


doc = DocxParser('test_fsd.docx').parse()
doc.print_doc()
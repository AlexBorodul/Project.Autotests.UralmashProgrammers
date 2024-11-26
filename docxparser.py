# from docx_parser import DocumentParser
#
# infile = 'test_fsd.docx'
# doc = DocumentParser(infile)
# for _type, item in doc.parse():
#     print(_type, item)

from docx_parser_converter.docx_to_txt.docx_to_txt_converter import DocxToTxtConverter
from docx_parser_converter.docx_parsers.utils import read_binary_from_file_path


class ParserToTxt:
    def __init__(self, entrance_path):
        self.docx_path = entrance_path
        self.docx_file_content = read_binary_from_file_path(self.docx_path)
        self.converter = DocxToTxtConverter(self.docx_file_content, use_default_values=True)
        self.txt_output = ''

    def convert(self):
        self.txt_output = self.converter.convert_to_txt(indent=True)
        return self.txt_output

    def save_file(self, exit_path):
        self.converter.save_txt_to_file(self.txt_output, exit_path)

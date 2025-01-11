import fitz
from docx import Document


def pdf_to_docx(pdf_path, docx_path):
    pdf_document = fitz.open(pdf_path)
    doc = Document()
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text()
        doc.add_paragraph(text)
    doc.save(docx_path)

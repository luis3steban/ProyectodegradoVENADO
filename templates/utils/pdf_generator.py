import pdfkit

def generar_pdf(html_content, file_path):
    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
    }
    pdfkit.from_string(html_content, file_path, options=options)

import logging
import pathlib

import os
import jinja2
import pdfkit

import app.src.config as settings

logger = logging.getLogger(__name__)

def render_html(values:list[dict], name:str, abstract:str) -> pathlib.Path: 

    template_loader = jinja2.FileSystemLoader(searchpath=settings.JINJA_SEARCH_PATH)
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "dictionary.html"
    template = template_env.get_template(template_file)

    context:dict = {
                        "headers": values[0].keys(),
                        "records": values,
                        "tittle": name,
                        "caption": abstract
                    }
                  
    output_text = template.render(context=context)

    html_path = pathlib.Path(settings.TEMP_FILES, f'{name}.html')
    html_file = open(html_path, 'w')
    html_file.write(output_text)
    html_file.close()

    return html_path

def html2pdf(html_path:str) -> str:
    options = {
        'page-size': 'Letter',
        'margin-top': '0.35in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }

    pdf_path:str = f"{html_path}.pdf"
    final_html_path:str = f"{html_path}.html"
    with open(final_html_path) as f:
        pdfkit.from_file(f, pdf_path, options=options)

    return final_html_path


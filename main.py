import logging
import json

import argparse
import markdown
import jinja2
import weasyprint


def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as file:
        return json.load(file)


def setup_logging() -> logging.Logger:
    logging.config.dictConfig(load_config('config.json'))
    return logging.getLogger(__name__)


logger = setup_logging()


def markdown_to_html(md_content: str) -> str:
    logger.debug('Converting Markdown to HTML')
    return markdown.markdown(md_content)


def read_file(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            logger.debug(f'Reading file: {file_path}')
            return file.read()
    except FileNotFoundError:
        logger.error(f'File not found: {file_path}')
        return ''


def html_to_pdf(
    html_content: str, 
    output_pdf_path: str,
    css_file_path: str
) -> None:
    logger.debug('Applying HTML to template')
    template = jinja2.Template(html_content)
    rendered_html = template.render()
    stylesheets = []
    if css_file_path:
        logger.debug(f'Adding CSS file: {css_file_path}')
        stylesheet = weasyprint.CSS(string=read_file(css_file_path))
        stylesheets.append(stylesheet)
    logger.debug('Converting HTML to PDF')
    pdf_document = weasyprint.HTML(string=rendered_html)
    logger.debug(f'Writing PDF to: {output_pdf_path}')
    pdf_document.write_pdf(output_pdf_path, stylesheets=stylesheets)


def process_files(
    input_md_path: str, 
    output_pdf_path: str, 
    css_file_path: str, 
    template_path: str = None
) -> None:
    markdown_content = read_file(input_md_path)
    html_content = markdown_to_html(markdown_content)

    if template_path:
        html_content = jinja2.Template(read_file(template_path)).render(
            content=html_content)

    html_to_pdf(html_content, output_pdf_path, css_file_path)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to PDF with optional CSS and template styling.')
    parser.add_argument('-i', '--input', type=str,
                        help='Path to the input Markdown file', required=True)
    parser.add_argument('-o', '--output', type=str,
                        help='Path to the output PDF file', required=True)
    parser.add_argument('-t', '--template', type=str,
                        help='Path to the template HTML file', required=False)
    parser.add_argument('-c', '--css', type=str, help='Path to the CSS file',
                        required=False)
    return parser.parse_args()


def main():
    args = parse_arguments()
    process_files(args.input, args.output, args.css, args.template)


if __name__ == '__main__':
    main()
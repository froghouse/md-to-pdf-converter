import argparse
import json
import logging
import logging.config

import jinja2
import markdown
import weasyprint


def load_config(config_path: str) -> dict:
    """Load a JSON configuration file."""
    with open(config_path, 'r') as file:
        return json.load(file)


def setup_logging(config_path: str = 'config.json') -> logging.Logger:
    """Set up logging configuration from a JSON file."""
    logging.config.dictConfig(load_config(config_path))
    return logging.getLogger(__name__)


logger = setup_logging()


def read_file(file_path: str) -> str:
    """Read the contents of a file and return it as a string."""
    logger.debug(f'Reading file: {file_path}')
    with open(file_path, 'r') as file:
        return file.read()


def markdown_to_html(md_content: str) -> str:
    """Convert Markdown content to HTML."""
    logger.debug('Converting Markdown to HTML')
    return markdown.markdown(md_content)


def html_to_pdf(
    html_content: str,
    output_pdf_path: str,
    css_file_path: str | None = None
) -> None:
    """Convert HTML content to a PDF file, applying optional CSS styles."""
    logger.debug('Converting HTML to PDF')
    stylesheets = []

    if css_file_path:
        logger.debug(f'Adding CSS file: {css_file_path}')
        css_content = read_file(css_file_path)
        stylesheet = weasyprint.CSS(string=css_content)
        stylesheets.append(stylesheet)

    pdf_document = weasyprint.HTML(string=html_content)
    logger.debug(f'Writing PDF to: {output_pdf_path}')
    pdf_document.write_pdf(output_pdf_path, stylesheets=stylesheets)


def process_files(
    input_md_path: str,
    output_pdf_path: str,
    css_file_path: str | None = None,
    template_path: str | None = None
) -> None:
    """Process the Markdown file and generate a PDF with optional styling."""
    try:
        markdown_content = read_file(input_md_path)
        html_content = markdown_to_html(markdown_content)

        if template_path:
            logger.debug(f'Applying template from: {template_path}')
            template_content = read_file(template_path)
            template = jinja2.Template(template_content)
            html_content = template.render(content=html_content)

        html_to_pdf(html_content, output_pdf_path, css_file_path)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to PDF with optional CSS and template styling.'
    )
    parser.add_argument(
        '-i', '--input', type=str, required=True,
        help='Path to the input Markdown file'
    )
    parser.add_argument(
        '-o', '--output', type=str, required=True,
        help='Path to the output PDF file'
    )
    parser.add_argument(
        '-t', '--template', type=str,
        help='Path to the template HTML file'
    )
    parser.add_argument(
        '-c', '--css', type=str,
        help='Path to the CSS file'
    )
    return parser.parse_args()


def main():
    """Main function to execute the script."""
    args = parse_arguments()
    process_files(args.input, args.output, args.css, args.template)


if __name__ == '__main__':
    main()

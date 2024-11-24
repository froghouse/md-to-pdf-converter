import argparse
import json
import logging
import logging.config
import sys

import jinja2
import markdown
import weasyprint
from weasyprint import CSS, HTML


def load_config(config_path: str) -> dict:
    """Load a JSON configuration file."""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Configuration file not found: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON configuration file: {e}")
        sys.exit(1)


def setup_logging(config_path: str = 'config.json') -> logging.Logger:
    """Set up logging configuration from a JSON file."""
    config = load_config(config_path)
    try:
        logging.config.dictConfig(config)
    except (ValueError, TypeError, AttributeError) as e:
        print(f"Error in logging configuration: {e}")
        sys.exit(1)
    return logging.getLogger(__name__)


logger = setup_logging()


def read_file(file_path: str) -> str:
    """Read the contents of a file and return it as a string."""
    logger.debug(f'Reading file: {file_path}')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f'File not found: {file_path}')
        raise
    except IOError as e:
        logger.error(f'Error reading file {file_path}: {e}')
        raise


def markdown_to_html(md_content: str) -> str:
    """Convert Markdown content to HTML."""
    logger.debug('Converting Markdown to HTML')
    try:
        return markdown.markdown(md_content)
    except Exception as e:
        logger.error(f'Error converting Markdown to HTML: {e}')
        raise


def render_template(html_content: str, template_path: str) -> str:
    """Render HTML content using a Jinja2 template."""
    try:
        template_content = read_file(template_path)
        template = jinja2.Template(template_content)
        logger.debug(f'Applying template from: {template_path}')
        return template.render(content=html_content)
    except jinja2.TemplateError as e:
        logger.error(f'Error rendering template: {e}')
        raise


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
        try:
            stylesheet = CSS(filename=css_file_path)
            stylesheets.append(stylesheet)
        except FileNotFoundError:
            logger.error(f'CSS file not found: {css_file_path}')
            raise
        except Exception as e:
            logger.error(f'Error loading CSS file {css_file_path}: {e}')
            raise

    try:
        pdf_document = HTML(string=html_content)
        logger.debug(f'Writing PDF to: {output_pdf_path}')
        pdf_document.write_pdf(target=output_pdf_path, stylesheets=stylesheets)
    except weasyprint.WeasyPrintError as e:
        logger.error(f'Error generating PDF: {e}')
        raise
    except Exception as e:
        logger.error(f'Unexpected error generating PDF: {e}')
        raise


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
            html_content = render_template(html_content, template_path)

        html_to_pdf(html_content, output_pdf_path, css_file_path)

    except FileNotFoundError as e:
        logger.error(f'File not found: {e}')
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred during file processing: {e}")
        sys.exit(1)


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

    # Validate input file
    if not args.input.endswith('.md'):
        logger.error('Input file must be a Markdown (.md) file.')
        sys.exit(1)

    # Validate output file
    if not args.output.endswith('.pdf'):
        logger.error('Output file must be a PDF (.pdf) file.')
        sys.exit(1)

    process_files(args.input, args.output, args.css, args.template)


if __name__ == '__main__':
    main()

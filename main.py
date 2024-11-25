import argparse
import json
import logging
import logging.config
import sys
import os

import jinja2
import markdown
import weasyprint
from pygments.formatters import HtmlFormatter
from weasyprint import CSS, HTML


class MarkdownPDFConverter:
    """Class to handle the conversion of Markdown files to PDF."""

    def __init__(self, config_path: str = "config.json") -> None:
        self.logger = self.setup_logging(config_path)

    def load_config(self, config_path: str) -> dict:
        """Load a JSON configuration file."""
        try:
            with open(config_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Configuration file not found: {config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON configuration file: {e}")
            sys.exit(1)

    def setup_logging(self, config_path: str) -> logging.Logger:
        """Set up logging configuration from a JSON file."""
        config = self.load_config(config_path)
        try:
            logging.config.dictConfig(config)
        except (ValueError, TypeError, AttributeError) as e:
            print(f"Error in logging configuration: {e}")
            sys.exit(1)
        return logging.getLogger(__name__)

    def read_file(self, file_path: str) -> str:
        """Read the contents of a file and return it as a string."""
        self.logger.debug(f"Reading file: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            raise
        except IOError as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            raise

    def markdown_to_html(self, md_content: str) -> str:
        """Convert Markdown content to HTML with syntax highlighting."""
        self.logger.debug("Converting Markdown to HTML with syntax highlighting")
        try:
            html_content = markdown.markdown(
                md_content,
                extensions=["codehilite", "extra"],
                extension_configs={"codehilite": {"linenums": True}},
                output_format="html5",
            )
            pygments_css = HtmlFormatter(style="sas").get_style_defs(".codehilite")
            full_html = f"<style>{pygments_css}</style>\n{html_content}"
            return full_html
        except Exception as e:
            self.logger.error(
                f"Error converting Markdown to HTML. Content: {md_content[:30]}... Error: {e}"
            )
            raise

    def render_template(self, html_content: str, template_path: str) -> str:
        """Render HTML content using a Jinja2 template."""
        self.logger.debug(f"Reading template from: {template_path}")
        try:
            template_content = self.read_file(template_path)
        except FileNotFoundError:
            self.logger.error(f"Template file not found: {template_path}")
            raise
        except Exception as e:
            self.logger.error(f"Error reading template file at {template_path}: {e}")
            raise

        try:
            # Configure the Jinja2 environment to raise an exception on undefined variables
            env = jinja2.Environment(
                loader=jinja2.BaseLoader(), undefined=jinja2.StrictUndefined
            )
            template = env.from_string(template_content)
            self.logger.debug(f"Applying template from: {template_path}")
            return template.render(content=html_content)
        except jinja2.TemplateSyntaxError as e:
            self.logger.error(
                f"Syntax error in template at {template_path}: Line {e.lineno} - {e.message}"
            )
            raise
        except jinja2.UndefinedError as e:
            self.logger.error(f"Undefined variable in template at {template_path}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error rendering template at {template_path}: {e}")
            raise

    def html_to_pdf(
        self, html_content: str, output_pdf_path: str, css_file_path: str | None = None
    ) -> None:
        """Convert HTML content to a PDF file, applying optional CSS styles."""
        self.logger.debug("Converting HTML to PDF")
        stylesheets = []

        if css_file_path:
            self.logger.debug(f"Adding CSS file: {css_file_path}")
            try:
                stylesheet = CSS(filename=css_file_path)
                stylesheets.append(stylesheet)
            except FileNotFoundError:
                self.logger.error(f"CSS file not found: {css_file_path}")
                raise
            except Exception as e:
                self.logger.error(f"Error loading CSS file at {css_file_path}: {e}")
                raise

        try:
            pdf_document = HTML(string=html_content)
            self.logger.debug(f"Writing PDF to: {output_pdf_path}")
            pdf_document.write_pdf(target=output_pdf_path, stylesheets=stylesheets)
        except OSError as e:
            self.logger.error(f"Error writing PDF file {output_pdf_path}: {e}")
            raise
        except weasyprint.WeasyPrintError as e:
            self.logger.error(f"Error generating PDF: {e}")
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error generating PDF while writing to {output_pdf_path}: {e}"
            )
            raise

    def process_files(
        self,
        input_md_path: str,
        output_pdf_path: str,
        css_file_path: str | None = None,
        template_path: str | None = None,
        force_overwrite: bool = False,
    ) -> None:
        """Process the Markdown file and generate a PDF with optional styling."""
        try:
            output_dir = os.path.dirname(output_pdf_path) or "."

            if not os.path.exists(output_dir):
                self.logger.error(f"Output directory does not exist: {output_dir}")
                sys.exit(1)

            if not os.access(output_dir, os.W_OK):
                self.logger.error(
                    f"No write permission to the output directory: {output_dir}"
                )
                sys.exit(1)

            if not force_overwrite and os.path.exists(output_pdf_path):
                self.logger.error(
                    f"Output file {output_pdf_path} already exists. Use --force to overwrite."
                )
                sys.exit(1)

            markdown_content = self.read_file(input_md_path)
            html_content = self.markdown_to_html(markdown_content)

            if template_path:
                html_content = self.render_template(html_content, template_path)

            self.html_to_pdf(html_content, output_pdf_path, css_file_path)

        except FileNotFoundError as e:
            self.logger.error(f"File not found: {e}")
            sys.exit(1)
        except PermissionError as e:
            self.logger.error(f"Permission error: {e}")
            sys.exit(1)
        except Exception as e:
            self.logger.error(
                f"An error occurred during file processing. Input file: {input_md_path}, "
                f"Output file: {output_pdf_path}. Error: {e}"
            )
            sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to PDF with optional CSS and template styling."
    )
    parser.add_argument(
        "-i", "--input", type=str, required=True, help="Path to the input Markdown file"
    )
    parser.add_argument(
        "-o", "--output", type=str, required=True, help="Path to the output PDF file"
    )
    parser.add_argument(
        "-t", "--template", type=str, help="Path to the template HTML file"
    )
    parser.add_argument("-c", "--css", type=str, help="Path to the CSS file")
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force overwriting of the output file if it exists",
    )
    return parser.parse_args()


def main() -> None:
    """Main function to execute the script."""
    args = parse_arguments()

    # Validate input file
    if not args.input.endswith(".md"):
        print(f"Input file must be a Markdown (.md) file. Provided: {args.input}")
        sys.exit(1)

    # Validate output file
    if not args.output.endswith(".pdf"):
        print(f"Output file must be a PDF (.pdf) file. Provided: {args.output}")
        sys.exit(1)

    converter = MarkdownPDFConverter()
    converter.process_files(
        args.input, args.output, args.css, args.template, force_overwrite=args.force
    )


if __name__ == "__main__":
    main()

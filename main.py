import argparse
import markdown
import jinja2
import weasyprint


def markdown_to_html(md_content: str) -> str:
    return markdown.markdown(md_content)


def read_file(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ''


def html_to_pdf(html_content: str, output_pdf_path: str,
                css_file_path: str) -> None:
    template = jinja2.Template(html_content)
    rendered_html = template.render()
    stylesheet = weasyprint.CSS(string=read_file(css_file_path))
    pdf_document = weasyprint.HTML(string=rendered_html)
    pdf_document.write_pdf(output_pdf_path, stylesheets=[stylesheet])


def process_files(input_md_path: str, output_pdf_path: str, css_file_path: str,
                  template_path: str = None) -> None:
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


if __name__ == '__main__':
    args = parse_arguments()
    process_files(args.input, args.output, args.css, args.template)
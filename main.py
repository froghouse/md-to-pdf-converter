import argparse
import markdown
import jinja2
import weasyprint


def markdown_to_html(markdown_text: str) -> str:
    return markdown.markdown(markdown_text)


def html_to_pdf(html_text: str, output_file: str) -> None:
    weasyprint.HTML(string=html_text).write_pdf(output_file)


def process_files(input_file: str, output_file: str) -> None:
    with open(input_file, 'r') as f:
        markdown_text = f.read()
    html_text = markdown_to_html(markdown_text)
    html_to_pdf(html_text, output_file)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('-i', '--input', type=str, help='Input file path',
                        required=True)
    parser.add_argument('-o', '--output', type=str, help='Output file path',
                        required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    process_files(args.input, args.output)
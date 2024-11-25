# test_main.py

import os
import pytest
import jinja2
from main import MarkdownPDFConverter

def test_markdown_to_html():
    converter = MarkdownPDFConverter()
    md_content = "# Hello World\nThis is a test."
    html_content = converter.markdown_to_html(md_content)
    assert "<h1>Hello World</h1>" in html_content

def test_render_template(tmp_path):
    converter = MarkdownPDFConverter()
    html_content = "<p>This is content</p>"
    template_content = "<html><body>{{ content }}</body></html>"
    template_path = tmp_path / "template.html"
    template_path.write_text(template_content)
    rendered_html = converter.render_template(html_content, str(template_path))
    assert "<body><p>This is content</p></body>" in rendered_html

def test_html_to_pdf(tmp_path):
    converter = MarkdownPDFConverter()
    html_content = "<h1>PDF Test</h1><p>Testing PDF generation.</p>"
    output_pdf_path = tmp_path / "output.pdf"
    converter.html_to_pdf(html_content, str(output_pdf_path))
    assert output_pdf_path.exists()

def test_process_files(tmp_path):
    converter = MarkdownPDFConverter()
    md_content = "# Test Markdown\nContent for testing."
    input_md_path = tmp_path / "input.md"
    input_md_path.write_text(md_content)
    output_pdf_path = tmp_path / "output.pdf"
    converter.process_files(str(input_md_path), str(output_pdf_path), force_overwrite=True)
    assert output_pdf_path.exists()

def test_missing_input_file():
    converter = MarkdownPDFConverter()
    with pytest.raises(FileNotFoundError):
        converter.read_file("nonexistent.md")

def test_invalid_template(tmp_path):
    converter = MarkdownPDFConverter()
    html_content = "<p>Test Content</p>"
    invalid_template = "<html><body>{{ undefined_variable }}</body></html>"
    template_path = tmp_path / "template.html"
    template_path.write_text(invalid_template)
    with pytest.raises(jinja2.UndefinedError):
        converter.render_template(html_content, str(template_path))

def test_output_directory_permissions(tmp_path):
    converter = MarkdownPDFConverter()
    md_content = "# Test"
    input_md_path = tmp_path / "input.md"
    input_md_path.write_text(md_content)
    output_dir = tmp_path / "no_write_permission"
    output_dir.mkdir(mode=0o400)
    output_pdf_path = output_dir / "output.pdf"
    with pytest.raises(SystemExit):
        converter.process_files(str(input_md_path), str(output_pdf_path))
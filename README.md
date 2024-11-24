# Markdown to PDF Converter

A lightweight tool for converting Markdown files into styled PDF documents using customizable templates. This project aims to provide an easy-to-use, less comprehensive alternative to LaTeX, with the simplicity of Markdown and the flexibility of CSS-based styling.

---

## Features (Planned for Version 1.0)
- Convert Markdown files into PDF documents.
- Support for user-specified templates to customize the look and feel of the output.
- Syntax highlighting for code blocks.
- Embedded image and hyperlink support.
- Command-line interface for ease of use.
- Cross-platform compatibility (Windows, macOS, Linux).

---

## Getting Started

### Prerequisites
To run the tool, you'll need:
- Python 3.9 or later
- Pip for managing Python dependencies

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/md-to-pdf-converter.git
   cd md-to-pdf-converter
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage
Once installed, you can convert a Markdown file to PDF with:
```bash
python mdtopdf.py input.md --template template.html --output output.pdf
```

### Options:
- `--template`: Specify a custom HTML template for styling.
- `--output`: Set the name and path of the output PDF file.

---

## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. See `CONTRIBUTING.md` for more details.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## TODO (Version 1.0 Progress)
- [ ] Markdown to PDF conversion
- [ ] Template support
- [ ] CLI interface
- [ ] Basic error handling
- [ ] Documentation and examples

---

## Acknowledgments
- [Markdown](https://daringfireball.net/projects/markdown/)
- [WeasyPrint](https://weasyprint.org/)
- [Jinja2](https://palletsprojects.com/p/jinja/)

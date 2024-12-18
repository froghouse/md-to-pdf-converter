# Markdown to PDF Converter

A lightweight tool for converting Markdown files into styled PDF documents using customizable templates. This project aims to provide an easy-to-use, less comprehensive alternative to LaTeX, with the simplicity of Markdown and the flexibility of CSS-based styling.

---

## Features
- Convert Markdown files into PDF documents.
- Support for user-specified templates to customize the look and feel of the output.
- Syntax highlighting for code blocks.
- Embedded image and hyperlink support.
- Command-line interface for ease of use.

---

## Getting Started

### Prerequisites
To run the tool, you'll need:
- Python 3.10 or later
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
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install poetry
   poetry install
   ```

---

## Usage
Once installed, you can convert a Markdown file to PDF with:
```bash
python mdtopdf.py --input input.md --template template.html --output output.pdf --css style.css --force
```

### Options:
- `--input`: Specify the markdown file to convert.
- `--template`: Specify a custom HTML template for styling.
- `--output`: Set the name and path of the output PDF file.
- `--css`: Specify a CSS file for styling the document.
- `--force`: Force overwriting of the output file if it exists.

---

## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. See `CONTRIBUTING.md` for more details.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## TODO (Version 1.0 Progress)
- [x] Markdown to PDF conversion
- [x] Template support
- [x] CLI interface
- [x] Basic error handling
- [x] Syntax highlighting for codeblocks
- [x] Embedded image and hyperlink support
- [x] Documentation and examples

---

## Acknowledgments
- [Markdown](https://daringfireball.net/projects/markdown/)
- [WeasyPrint](https://weasyprint.org/)
- [Jinja2](https://palletsprojects.com/p/jinja/)

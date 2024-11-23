# Contributing to Markdown to PDF Converter

We’re excited that you’re interested in contributing to this project! By participating, you’re helping to build a user-friendly tool for converting Markdown files into customizable PDF documents. This guide outlines the process for contributing effectively.

---

## How Can You Contribute?

### Reporting Bugs
If you encounter a bug:
1. Search the [issues](https://github.com/froghouse/md-to-pdf-converter/issues) to see if it’s already reported.
2. If not, create a new issue with:
   - A clear title describing the problem.
   - Steps to reproduce the issue.
   - Expected and actual results.
   - Any relevant logs or screenshots.

### Suggesting Features
Have an idea to improve the project? Suggest it by:
1. Checking the [issues](https://github.com/froghouse/md-to-pdf-converter/issues) to avoid duplicates.
2. Opening a feature request with:
   - A description of the feature and its benefits.
   - Any technical suggestions for implementation.

### Code Contributions
Want to add a new feature or fix a bug? Follow these steps:

1. **Fork the Repository**  
   Fork the project to your GitHub account and clone it locally:
   ```bash
   git clone https://github.com/your-username/md-to-pdf-converter.git
   cd md-to-pdf-converter
   ```

2. **Set Up the Development Environment**  
   Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create a Branch**  
   Use descriptive names for branches:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes**  
   - Follow PEP 8 coding standards.
   - Write clear and concise code with comments when necessary.
   - Add or update unit tests as needed.

5. **Run Tests**  
   Ensure all tests pass before submitting:
   ```bash
   pytest
   ```

6. **Commit Your Changes**  
   Use meaningful commit messages:
   ```bash
   git commit -m "Add feature: your-feature-name"
   ```

7. **Push Your Branch**  
   Push the changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Submit a Pull Request**  
   Open a pull request to the `main` branch in the original repository. Include:
   - A clear description of your changes.
   - Any additional context or screenshots.

---

## Coding Standards
- **Code Style**: Adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/).
- **Commit Messages**: Write descriptive, imperative-style messages (e.g., “Add feature: support for custom templates”).
- **Testing**: Write unit tests for new features or bug fixes.

---

## Feedback and Review
Pull requests are reviewed by maintainers. We may request changes or ask questions about your contribution. Once approved, your changes will be merged into the main branch.

---

## Community Guidelines
- Be respectful and collaborative.
- Provide constructive feedback in discussions and reviews.
- Aim for clear and concise communication.

---

## Thank You!
Your contributions make this project better! Whether you’re reporting a bug, suggesting a feature, or writing code, we’re grateful for your help.

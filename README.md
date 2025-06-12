# Fax Intelligence Pipeline

A modular pipeline for processing medical faxes using OCR, natural language processing, and deep learning classification. This tool extracts structured information from scanned PDF faxes and classifies the content using a fine-tuned BERT model.

## Features

- **PDF Input Handling**: Converts multi-page PDFs to images using `pdf2image`.
- **OCR**: Extracts text from images using Tesseract.
- **RDNF Classification**: Automatically detects and filters RDNF forms.
- **Information Extraction**: Identifies medically relevant lines (e.g. lab results).
- **Text Classification**: Classifies content using a fine-tuned BERT model (Positive / Negative / Neutral).
- **Modular Design**: Each step is encapsulated in its own function for easy reuse or debugging.

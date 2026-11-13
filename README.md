# DocChat

DocChat is a command-line assistant that answers questions about local documents and repositories using intelligent RAG and tool-calling execution.

## Example Sessions

# Markdown Compiler
```bash
cd test_projects/markdown-compiler
chat
chat> /ls .
markdown-compiler.py
README.md
chat> how are headings converted?
Headings are parsed using regular expressions matching markdown hashes.

# Homepage
cd test_projects/lab-homepage
chat
chat> /ls .
index.html
styles.css
chat> what styles are applied?
Styles use custom CSS variables for layout padding and typography.

# eBay Scraper
cd test_projects/ebay-scraper
chat
chat> /ls .
ebay-dl.py
output.json
chat> how is data exported?
Data is serialized directly to formatted JSON files.
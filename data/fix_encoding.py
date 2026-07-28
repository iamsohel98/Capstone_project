"""Fix encoding issues in generate_sample_pdfs.py"""
import re

path = "data/generate_sample_pdfs.py"
with open(path, encoding="utf-8") as f:
    content = f.read()

replacements = {
    "\u2014": "-",
    "\u2013": "-",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u0393\u00c7\u00ac": "-",
    "\u0393\u00c7\u00b3": "'",
}
for bad, good in replacements.items():
    content = content.replace(bad, good)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed encoding. Running generator...")

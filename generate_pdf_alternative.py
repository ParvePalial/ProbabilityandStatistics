#!/usr/bin/env python3
"""
Alternative script to convert markdown to PDF using Python-Markdown and WeasyPrint.
This approach doesn't require external tools like pandoc.
"""

import os
import sys
import markdown
import argparse
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def convert_markdown_to_pdf(input_file, output_file):
    """Convert Markdown to PDF using python-markdown and WeasyPrint."""
    print(f"Converting {input_file} to {output_file}...")
    
    # Read the markdown file
    with open(input_file, 'r') as f:
        markdown_text = f.read()
    
    # Convert markdown to HTML
    html = markdown.markdown(
        markdown_text,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.tables',
            'markdown.extensions.toc'
        ]
    )
    
    # Add some CSS for better styling
    css = CSS(string='''
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #333;
            font-weight: bold;
        }
        h1 {
            font-size: 24pt;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }
        h2 {
            font-size: 18pt;
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }
        h3 {
            font-size: 14pt;
        }
        pre {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 3px;
            overflow-x: auto;
        }
        code {
            font-family: Consolas, Monaco, "Andale Mono", monospace;
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
        }
        blockquote {
            border-left: 4px solid #ddd;
            padding-left: 10px;
            color: #555;
            margin-left: 20px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        img {
            max-width: 100%;
            height: auto;
        }
    ''')
    
    # Create a complete HTML document
    complete_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Probability Puzzles Report</title>
    </head>
    <body>
    {html}
    </body>
    </html>
    '''
    
    # Save the HTML file for inspection (optional)
    with open(input_file.replace('.md', '.html'), 'w') as f:
        f.write(complete_html)
    
    # Render the HTML to PDF
    font_config = FontConfiguration()
    HTML(string=complete_html).write_pdf(
        output_file,
        stylesheets=[css],
        font_config=font_config
    )
    
    print(f"Successfully created {output_file}")
    print(f"Note: The images referenced in the markdown need to be in the same directory.")

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown report to PDF using Python-Markdown and WeasyPrint")
    parser.add_argument('-i', '--input', default='probability_puzzles_report.md', 
                      help='Input markdown file (default: probability_puzzles_report.md)')
    parser.add_argument('-o', '--output', default='probability_puzzles_report.pdf',
                      help='Output PDF file (default: probability_puzzles_report.pdf)')
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found.")
        return
    
    try:
        convert_markdown_to_pdf(args.input, args.output)
    except ImportError:
        print("\nRequired dependencies not installed. Please install them with:")
        print("\npip install markdown weasyprint")
        print("\nNote: WeasyPrint has additional system dependencies.")
        print("See https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation for details.")

if __name__ == "__main__":
    main() 
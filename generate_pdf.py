#!/usr/bin/env python3
"""
Script to convert the markdown report to PDF using pdfkit or other libraries.
"""

import os
import subprocess
import argparse

def check_pandoc_installed():
    """Check if pandoc is installed."""
    try:
        subprocess.run(['pandoc', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def convert_with_pandoc(input_file, output_file):
    """Convert Markdown to PDF using pandoc."""
    print(f"Converting {input_file} to {output_file} using pandoc...")
    try:
        subprocess.run([
            'pandoc',
            input_file,
            '-o', output_file,
            '--pdf-engine=xelatex',
            '--variable', 'geometry=margin=1in',
            '--variable', 'fontsize=11pt',
            '--standalone',
            '--toc'
        ], check=True)
        print(f"Successfully created {output_file}")
        return True
    except subprocess.SubprocessError as e:
        print(f"Error converting to PDF: {e}")
        return False

def install_dependencies():
    """Print instructions for installing dependencies."""
    print("\nDependencies not installed. Please install the required dependencies:")
    print("\n1. Pandoc - https://pandoc.org/installing.html")
    print("   - On macOS: brew install pandoc")
    print("   - On Ubuntu/Debian: sudo apt-get install pandoc")
    print("   - On Windows: Download from https://pandoc.org/installing.html")
    
    print("\n2. LaTeX (for PDF generation)")
    print("   - On macOS: brew install --cask mactex")
    print("   - On Ubuntu/Debian: sudo apt-get install texlive-xetex")
    print("   - On Windows: Install MiKTeX or TeX Live")
    
    print("\nAfter installing dependencies, run this script again.")

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown report to PDF")
    parser.add_argument('-i', '--input', default='probability_puzzles_report.md', 
                        help='Input markdown file (default: probability_puzzles_report.md)')
    parser.add_argument('-o', '--output', default='probability_puzzles_report.pdf',
                        help='Output PDF file (default: probability_puzzles_report.pdf)')
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found.")
        return
    
    if check_pandoc_installed():
        success = convert_with_pandoc(args.input, args.output)
        if success:
            print("\nTo generate the full report with images:")
            print("1. Open the PDF in your preferred PDF editor")
            print("2. Ensure the image files (monty_hall_results.png, monty_hall_visualization.png, etc.) are in the same directory")
            print("3. You may need to run the simulation scripts first to generate these images:")
            print("   - python monty_hall_simulator.py")
            print("   - python bertrands_box_simulator.py")
    else:
        install_dependencies()

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Compile translation JSON files to PDF using XeLaTeX.

Usage:
    python3 compile_chapters.py translations/chapter_001.json output/
    python3 compile_chapters.py translations/ output/

Requirements:
    - XeLaTeX (texlive-xetex)
    - xeCJK package
    - Noto CJK fonts
"""

import json
import sys
import os
import subprocess
import tempfile
from pathlib import Path

# LaTeX template
LATEX_TEMPLATE = r"""
\documentclass[11pt,a4paper]{article}
\usepackage{xeCJK}
\usepackage{xcolor}
\usepackage{geometry}
\usepackage{setspace}
\usepackage{titlesec}
\usepackage{fancyhdr}

% Page geometry
\geometry{margin=2.5cm}

% Font setup
\setCJKmainfont{Noto Serif CJK SC}
\setCJKsansfont{Noto Sans CJK SC}
\setmainfont{Noto Serif}

% Russian support
\usepackage{polyglossia}
\setdefaultlanguage{english}
\setotherlanguage{russian}

% Color definitions
\definecolor{original}{HTML}{000000}
\definecolor{modernzh}{HTML}{333333}
\definecolor{english}{HTML}{00008B}
\definecolor{russian}{HTML}{8B0000}
\definecolor{japanese}{HTML}{006400}
\definecolor{commentary}{HTML}{666666}

% Custom commands
\newcommand{\originaltext}[1]{\textcolor{original}{\textbf{【原文】} #1}}
\newcommand{\modernzh}[1]{\textcolor{modernzh}{\textbf{【现代汉语】} #1}}
\newcommand{\english}[1]{\textcolor{english}{\textbf{[English]} #1}}
\newcommand{\russian}[1]{\textcolor{russian}{\textbf{[Русский]} #1}}
\newcommand{\japanese}[1]{\textcolor{japanese}{\textbf{【日本語】} #1}}

% Spacing
\setstretch{1.3}
\setlength{\parskip}{0.5em}

% Header/Footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{红楼梦 · Dream of the Red Chamber}
\fancyhead[R]{<<CHAPTER_HEADER>>}
\fancyfoot[C]{\thepage}

\begin{document}

% Title
\begin{center}
{\Large\bfseries 第<<CHAPTER_NUM>>回}\\[0.5em]
{\large <<CHAPTER_TITLE_ORIGINAL>>}\\[0.3em]
{\small\textcolor{modernzh}{<<CHAPTER_TITLE_ZH>>}}\\
{\small\textcolor{english}{<<CHAPTER_TITLE_EN>>}}\\
{\small\textcolor{russian}{<<CHAPTER_TITLE_RU>>}}\\
{\small\textcolor{japanese}{<<CHAPTER_TITLE_JA>>}}
\end{center}

\vspace{1em}
\hrule
\vspace{1em}

<<CONTENT>>

\end{document}
"""

SEGMENT_TEMPLATE = r"""
\subsection*{段落 <<SEGMENT_ID>><<SEGMENT_TYPE>>}

\originaltext{<<ORIGINAL>>}

\modernzh{<<ZH_MODERN>>}

\english{<<ENGLISH>>}

\russian{<<RUSSIAN>>}

\japanese{<<JAPANESE>>}

<<POEM_NOTES>>
<<TRANSLATOR_NOTES>>

\vspace{0.5em}
\hrule
\vspace{0.5em}
"""


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    replacements = [
        ('\\', r'\textbackslash{}'),
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('^', r'\textasciicircum{}'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def format_segment(segment: dict, segment_id: int) -> str:
    """Format a single segment for LaTeX."""
    segment_type = segment.get("type", "prose")
    type_label = f" ({segment_type})" if segment_type != "prose" else ""
    
    content = SEGMENT_TEMPLATE
    content = content.replace("<<SEGMENT_ID>>", str(segment_id))
    content = content.replace("<<SEGMENT_TYPE>>", type_label)
    content = content.replace("<<ORIGINAL>>", escape_latex(segment.get("original", "")))
    content = content.replace("<<ZH_MODERN>>", escape_latex(segment.get("zh_modern", "")))
    content = content.replace("<<ENGLISH>>", escape_latex(segment.get("en", "")))
    content = content.replace("<<RUSSIAN>>", escape_latex(segment.get("ru", "")))
    content = content.replace("<<JAPANESE>>", escape_latex(segment.get("ja", "")))
    
    # Poem notes
    poem_notes = ""
    if segment_type == "poem" and "poem_notes" in segment:
        notes = segment["poem_notes"]
        poem_notes = r"\textcolor{commentary}{\textit{Poetry Notes: "
        if isinstance(notes, dict):
            for key, value in notes.items():
                if isinstance(value, list):
                    value = ", ".join(value)
                poem_notes += f"{key}: {escape_latex(str(value))}; "
        poem_notes += r"}}"
    content = content.replace("<<POEM_NOTES>>", poem_notes)
    
    # Translator notes
    trans_notes = ""
    if "translator_notes" in segment and segment["translator_notes"]:
        notes = segment["translator_notes"]
        if isinstance(notes, list):
            trans_notes = r"\textcolor{commentary}{\textit{Notes: "
            trans_notes += "; ".join(escape_latex(n) for n in notes)
            trans_notes += r"}}"
    content = content.replace("<<TRANSLATOR_NOTES>>", trans_notes)
    
    return content


def compile_chapter(json_path: str, output_dir: str) -> bool:
    """
    Compile a single chapter JSON to PDF.
    
    Returns True on success, False on failure.
    """
    # Load JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chapter_num = data.get("chapter", 0)
    title = data.get("chapter_title", {})
    segments = data.get("segments", [])
    
    # Build content
    content_parts = []
    for i, segment in enumerate(segments):
        content_parts.append(format_segment(segment, i + 1))
    content = "\n".join(content_parts)
    
    # Build LaTeX document
    latex = LATEX_TEMPLATE
    latex = latex.replace("<<CHAPTER_NUM>>", str(chapter_num))
    latex = latex.replace("<<CHAPTER_HEADER>>", f"第{chapter_num}回")
    latex = latex.replace("<<CHAPTER_TITLE_ORIGINAL>>", escape_latex(title.get("original", "")))
    latex = latex.replace("<<CHAPTER_TITLE_ZH>>", escape_latex(title.get("zh_modern", "")))
    latex = latex.replace("<<CHAPTER_TITLE_EN>>", escape_latex(title.get("en", "")))
    latex = latex.replace("<<CHAPTER_TITLE_RU>>", escape_latex(title.get("ru", "")))
    latex = latex.replace("<<CHAPTER_TITLE_JA>>", escape_latex(title.get("ja", "")))
    latex = latex.replace("<<CONTENT>>", content)
    
    # Write to temp file and compile
    output_name = f"chapter_{chapter_num:03d}"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, f"{output_name}.tex")
        
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(latex)
        
        # Run XeLaTeX
        try:
            result = subprocess.run(
                ['xelatex', '-interaction=nonstopmode', tex_path],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                print(f"XeLaTeX error for chapter {chapter_num}:")
                print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
                return False
            
            # Copy PDF to output
            pdf_path = os.path.join(tmpdir, f"{output_name}.pdf")
            if os.path.exists(pdf_path):
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"{output_name}.pdf")
                
                import shutil
                shutil.copy(pdf_path, output_path)
                print(f"✓ Created: {output_path}")
                return True
            else:
                print(f"✗ PDF not generated for chapter {chapter_num}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"✗ Timeout compiling chapter {chapter_num}")
            return False
        except FileNotFoundError:
            print("✗ XeLaTeX not found. Please install texlive-xetex.")
            return False


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 compile_chapters.py <json_file_or_dir> <output_dir>")
        print("\nExamples:")
        print("  python3 compile_chapters.py translations/chapter_001.json output/")
        print("  python3 compile_chapters.py translations/ output/")
        sys.exit(1)
    
    source = sys.argv[1]
    output_dir = sys.argv[2]
    
    if os.path.isfile(source):
        # Single file
        success = compile_chapter(source, output_dir)
        sys.exit(0 if success else 1)
    
    elif os.path.isdir(source):
        # Directory
        path = Path(source)
        json_files = sorted(path.glob("chapter_*.json"))
        
        if not json_files:
            print(f"No chapter_*.json files found in {source}")
            sys.exit(1)
        
        success_count = 0
        fail_count = 0
        
        for filepath in json_files:
            if compile_chapter(str(filepath), output_dir):
                success_count += 1
            else:
                fail_count += 1
        
        print(f"\nSummary: {success_count} compiled, {fail_count} failed")
        sys.exit(0 if fail_count == 0 else 1)
    
    else:
        print(f"Error: {source} is not a file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()

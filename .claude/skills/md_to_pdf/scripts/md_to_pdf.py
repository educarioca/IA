#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MD to PDF converter - Tema Thomson Reuters
Usa fpdf2 (puro Python, sem dependencias nativas)
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from fpdf import FPDF


def parse_args():
    parser = argparse.ArgumentParser(description="Converte Markdown para PDF estilizado")
    parser.add_argument("--file", help="Arquivo .md a converter")
    parser.add_argument("--output", help="Caminho do PDF de saida")
    parser.add_argument("--dir", default=".", help="Diretorio para buscar .md (modo --list)")
    parser.add_argument("--list", action="store_true", help="Listar arquivos .md disponiveis")
    parser.add_argument("--color", default="E87722", help="Cor de destaque em hex sem # (default: E87722)")
    return parser.parse_args()


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def sanitize_text(text):
    """Sanitiza caracteres Unicode para compatibilidade latin-1"""
    replacements = {
        "—": "-",    # em dash
        "–": "-",    # en dash
        "‘": "'",    # left single quote
        "’": "'",    # right single quote
        "“": '"',    # left double quote
        "”": '"',    # right double quote
        "…": "...",  # ellipsis
        "→": "->",   # arrow right
        "←": "<-",   # arrow left
        "•": "-",    # bullet
        " ": " ",    # non-breaking space
        " ": " ",    # line separator
        " ": " ",    # paragraph separator
        "​": "",     # zero-width space
        "·": "-",    # middle dot
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Fallback: remove any remaining non-latin1 chars
    try:
        text.encode("latin-1")
    except UnicodeEncodeError:
        text = text.encode("latin-1", errors="replace").decode("latin-1")
    return text


def list_md_files(directory):
    """Lista arquivos .md no diretorio com tamanho e data"""
    md_files = []
    for f in sorted(Path(directory).glob("*.md")):
        stat = f.stat()
        size_kb = stat.st_size / 1024
        mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%d/%m/%Y %H:%M")
        if size_kb >= 1024:
            size_str = f"{size_kb/1024:.1f} MB"
        else:
            size_str = f"{size_kb:.1f} KB"
        md_files.append(f"{f.name}|{size_str}|{mod_time}")
    return md_files


class MdToPdfConverter(FPDF):
    def __init__(self, accent_color=(232, 119, 34)):
        super().__init__()
        self.accent = accent_color
        self.black = (26, 26, 26)
        self.white = (255, 255, 255)
        self.gray_bg = (249, 249, 249)
        self.gray_line = (220, 220, 220)
        self.quote_bg = (255, 248, 240)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")

    def render_h1(self, text):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*self.accent)
        self.cell(0, 12, text, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.accent)
        self.set_line_width(0.8)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(6)

    def render_h2(self, text):
        if self.get_y() > 250:
            self.add_page()
        self.ln(4)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*self.accent)
        self.cell(0, 9, text, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.gray_line)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def render_h3(self, text):
        if self.get_y() > 260:
            self.add_page()
        self.ln(3)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*self.accent)
        self.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def render_blockquote(self, text):
        self.set_fill_color(*self.quote_bg)
        self.set_draw_color(*self.accent)
        x = self.get_x()
        y = self.get_y()
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 100, 100)
        self.set_line_width(1)
        # Calculate height first
        w = self.w - self.l_margin - self.r_margin - 4
        lines_count = len(text.split("\n"))
        block_h = max(lines_count * 5, 10)
        self.line(x, y, x, y + block_h)
        self.set_x(x + 4)
        self.multi_cell(w, 5, text, fill=True)
        self.ln(3)

    def render_table(self, headers, rows):
        if self.get_y() > 220:
            self.add_page()

        col_count = len(headers)
        avail_w = self.w - self.l_margin - self.r_margin

        # Calculate column widths proportional to content
        col_widths = []
        for i in range(col_count):
            max_len = len(headers[i])
            for row in rows:
                if i < len(row):
                    max_len = max(max_len, len(row[i]))
            col_widths.append(max(max_len, 3))

        total = sum(col_widths)
        col_widths = [(w / total) * avail_w for w in col_widths]

        # Enforce minimum width
        for i in range(len(col_widths)):
            col_widths[i] = max(col_widths[i], 12)
        total = sum(col_widths)
        col_widths = [(w / total) * avail_w for w in col_widths]

        # Header row
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(*self.accent)
        self.set_text_color(*self.white)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, re.sub(r"\*\*(.*?)\*\*", r"\1", h.strip()), border=0, fill=True)
        self.ln()

        # Data rows
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.black)
        for row_idx, row in enumerate(rows):
            # Page break with header repeat
            if self.get_y() > 270:
                self.add_page()
                self.set_font("Helvetica", "B", 8)
                self.set_fill_color(*self.accent)
                self.set_text_color(*self.white)
                for i, h in enumerate(headers):
                    self.cell(col_widths[i], 7, re.sub(r"\*\*(.*?)\*\*", r"\1", h.strip()), border=0, fill=True)
                self.ln()
                self.set_font("Helvetica", "", 8)
                self.set_text_color(*self.black)

            # Zebra striping
            if row_idx % 2 == 1:
                self.set_fill_color(*self.gray_bg)
            else:
                self.set_fill_color(*self.white)

            # Row height based on content
            max_lines = 1
            for i, cell_text in enumerate(row):
                if i < len(col_widths):
                    clean = re.sub(r"\*\*(.*?)\*\*", r"\1", cell_text.strip())
                    char_per_line = max(1, int(col_widths[i] / 2))
                    lines_needed = max(1, (len(clean) // char_per_line) + 1)
                    max_lines = max(max_lines, lines_needed)
            row_h = 6 * min(max_lines, 3)

            for i in range(col_count):
                cell_text = row[i].strip() if i < len(row) else ""
                cell_text = re.sub(r"\*\*(.*?)\*\*", r"\1", cell_text)
                self.cell(col_widths[i], row_h, cell_text, border=0, fill=True)
            self.ln()

            # Bottom border
            self.set_draw_color(*self.gray_line)
            self.set_line_width(0.1)
            self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())

        self.ln(4)

    def _write_rich(self, text, size=10):
        """Escreve texto com suporte a **negrito** e `code` inline"""
        text = text.replace("`", "")
        parts = re.split(r"(\*\*.*?\*\*)", text)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                self.set_font("Helvetica", "B", size)
                self.write(5.5, part[2:-2])
                self.set_font("Helvetica", "", size)
            else:
                self.write(5.5, part)

    def render_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.black)
        self._write_rich(text, 10)
        self.ln(5.5)
        self.ln(1)

    def render_code_block(self, lines):
        if self.get_y() > 250:
            self.add_page()
        self.set_fill_color(240, 240, 240)
        self.set_font("Courier", "", 8)
        self.set_text_color(50, 50, 50)
        for line in lines:
            if self.get_y() > 275:
                self.add_page()
                self.set_fill_color(240, 240, 240)
                self.set_font("Courier", "", 8)
                self.set_text_color(50, 50, 50)
            self.cell(0, 5, "  " + line, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def render_hr(self):
        self.ln(3)
        self.set_draw_color(*self.gray_line)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(5)

    def render_bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.black)
        self.cell(6, 5.5, "-")
        self._write_rich(text, 10)
        self.ln(5.5)
        self.ln(1)

    def render_image(self, img_path, alt_text=""):
        if not os.path.isfile(img_path):
            self.render_text(f"[Imagem nao encontrada: {img_path}]")
            return
        usable_w = self.w - self.l_margin - self.r_margin
        try:
            from PIL import Image
            with Image.open(img_path) as img:
                img_w, img_h = img.size
        except Exception:
            img_w, img_h = 800, 600
        aspect = img_h / img_w
        display_w = usable_w
        display_h = display_w * aspect
        max_h = 220
        if display_h > max_h:
            display_h = max_h
            display_w = display_h / aspect
        if self.get_y() + display_h + 10 > self.h - 20:
            self.add_page()
        x = self.l_margin + (usable_w - display_w) / 2
        self.image(img_path, x=x, y=self.get_y(), w=display_w, h=display_h)
        self.set_y(self.get_y() + display_h + 3)
        if alt_text:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 5, alt_text, align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(3)


def convert_md_to_pdf(md_path, pdf_path, accent_color):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = sanitize_text(content)
    lines = content.split("\n")

    pdf = MdToPdfConverter(accent_color=accent_color)
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    i = 0
    in_table = False
    table_headers = []
    table_rows = []
    in_code_block = False
    code_lines = []

    while i < len(lines):
        line = lines[i]

        # Code blocks (fenced)
        if line.strip().startswith("```"):
            if in_code_block:
                pdf.render_code_block(code_lines)
                code_lines = []
                in_code_block = False
            else:
                if in_table:
                    pdf.render_table(table_headers, table_rows)
                    in_table = False
                    table_headers = []
                    table_rows = []
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # H1
        if line.startswith("# ") and not line.startswith("##"):
            if in_table:
                pdf.render_table(table_headers, table_rows)
                in_table = False
                table_headers = []
                table_rows = []
            pdf.render_h1(line[2:])
            i += 1
            continue

        # H2
        if line.startswith("## ") and not line.startswith("###"):
            if in_table:
                pdf.render_table(table_headers, table_rows)
                in_table = False
                table_headers = []
                table_rows = []
            pdf.render_h2(line[3:])
            i += 1
            continue

        # H3
        if line.startswith("### "):
            if in_table:
                pdf.render_table(table_headers, table_rows)
                in_table = False
                table_headers = []
                table_rows = []
            pdf.render_h3(line[4:])
            i += 1
            continue

        # HR
        if line.strip() == "---":
            if in_table:
                pdf.render_table(table_headers, table_rows)
                in_table = False
                table_headers = []
                table_rows = []
            pdf.render_hr()
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            if in_table:
                pdf.render_table(table_headers, table_rows)
                in_table = False
                table_headers = []
                table_rows = []
            bq_text = line.lstrip("> ").strip() + "\n"
            i += 1
            while i < len(lines) and lines[i].strip().startswith(">"):
                bq_text += lines[i].strip().lstrip("> ").strip() + "\n"
                i += 1
            pdf.render_blockquote(bq_text.strip())
            continue

        # Table
        if "|" in line and line.strip().startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if all(re.match(r"^[-:]+$", c.strip()) for c in cells):
                i += 1
                continue
            if not in_table:
                in_table = True
                table_headers = cells
            else:
                table_rows.append(cells)
            i += 1
            continue
        else:
            if in_table:
                pdf.render_table(table_headers, table_rows)
                in_table = False
                table_headers = []
                table_rows = []

        # Image ![alt](path)
        img_match = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)", line.strip())
        if img_match:
            alt_text = img_match.group(1)
            img_file = img_match.group(2)
            if not os.path.isabs(img_file):
                img_file = os.path.join(os.path.dirname(md_path), img_file)
            pdf.render_image(img_file, alt_text)
            i += 1
            continue

        # Empty line
        if line.strip() == "":
            i += 1
            continue

        # Bullet list
        if line.strip().startswith("- "):
            pdf.render_bullet(line.strip()[2:])
            i += 1
            continue

        # Normal text
        pdf.render_text(line)
        i += 1

    # Flush remaining
    if in_table:
        pdf.render_table(table_headers, table_rows)
    if in_code_block and code_lines:
        pdf.render_code_block(code_lines)

    pdf.output(pdf_path)
    return pdf_path


def main():
    args = parse_args()

    if args.list:
        files = list_md_files(args.dir)
        if not files:
            print(f"Nenhum arquivo .md encontrado em: {os.path.abspath(args.dir)}")
            sys.exit(1)
        for f in files:
            print(f)
        sys.exit(0)

    if not args.file:
        print("Erro: --file obrigatorio (ou use --list para listar)")
        sys.exit(1)

    md_path = os.path.abspath(args.file)
    if not os.path.exists(md_path):
        print(f"Erro: arquivo nao encontrado: {md_path}")
        sys.exit(1)

    if args.output:
        pdf_path = os.path.abspath(args.output)
    else:
        pdf_path = os.path.splitext(md_path)[0] + ".pdf"

    accent = hex_to_rgb(args.color)
    result = convert_md_to_pdf(md_path, pdf_path, accent)
    print(f"PDF gerado: {result}")


if __name__ == "__main__":
    main()

---
name: md_to_pdf
description: Converte arquivos Markdown (.md) em PDF estilizado com tema Thomson Reuters (laranja #E87722), tabelas formatadas, blockquotes e paginacao. Usa fpdf2 (puro Python, sem dependencias externas).
version: 1.0.0
---

# MD to PDF

Converte arquivos `.md` em `.pdf` com visual profissional usando o tema TR (laranja #E87722, Helvetica, tabelas zebradas).

## When to Use

Use this skill when the user:
- Pedir para **converter um .md em pdf**
- Pedir para **gerar pdf** de um arquivo markdown
- Mencionar **md to pdf**, **markdown para pdf**, **pdf do md**

### Examples that SHOULD trigger this skill

- "gera um pdf desse md"
- "converte o dicas.md pra pdf"
- "md_to_pdf"
- "gere um pdf com esse markdown"
- "transforma esse .md em .pdf"

### Examples that should NOT trigger this skill

- "me mostra o md" (apenas leitura)
- "abre o pdf" (arquivo ja existe)
- "converte pdf pra md" (direcao inversa)

## How to Execute

### Caso 1: Arquivo especificado nos argumentos

Converter diretamente:
```bash
python "${SKILL_DIR}/scripts/md_to_pdf.py" --file "/path/to/arquivo.md"
```

### Caso 2: Sem arquivo especificado

1. Listar os .md disponiveis no diretorio atual:
```bash
python "${SKILL_DIR}/scripts/md_to_pdf.py" --list --dir "."
```
2. Apresentar a lista ao usuario usando **AskUserQuestion** para que ele escolha qual arquivo converter. O output do `--list` usa formato `nome|tamanho|dd/mm/aaaa HH:MM` — incluir tamanho e data/hora na description de cada opcao
3. Rodar o script com `--file` passando o arquivo escolhido:
```bash
python "${SKILL_DIR}/scripts/md_to_pdf.py" --file "/path/to/escolhido.md"
```

### Opcoes adicionais

```bash
# Especificar nome do PDF de saida
python "${SKILL_DIR}/scripts/md_to_pdf.py" --file "input.md" --output "output.pdf"

# Especificar cor de destaque (hex sem #)
python "${SKILL_DIR}/scripts/md_to_pdf.py" --file "input.md" --color "E87722"
```

Apos gerar o PDF, abre automaticamente com `start ""`.

## Input Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| file      | No       | Caminho do arquivo .md a converter |
| dir       | No       | Diretorio para buscar .md (default: atual) |
| output    | No       | Caminho do PDF de saida (default: mesmo nome do .md com .pdf) |
| color     | No       | Cor de destaque em hex sem # (default: E87722 laranja TR) |

## Output

- Arquivo `.pdf` no mesmo diretorio do `.md` original (ou no path especificado em --output)
- Estilo: tema TR (laranja #E87722), Helvetica, tabelas zebradas com header colorido
- Suporta: H1, H2, tabelas, blockquotes, horizontal rules, code inline, texto normal
- Paginacao automatica com "Pagina X/Y" no rodape

## Dependencias

- `fpdf2` (puro Python, sem dependencias nativas)
- **NAO** usar weasyprint (requer GTK) ou xhtml2pdf (requer freetype 64-bit)

## Limitacoes

- Nao suporta imagens embutidas no markdown
- Caracteres Unicode fora de latin-1 sao sanitizados automaticamente (em dash -> -, smart quotes -> aspas simples)
- Fontes limitadas a Helvetica/Courier (built-in do fpdf2)

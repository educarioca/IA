# Global Instructions

## Idioma
- Sempre responder em **portugues brasileiro** (pt-BR)
- Codigo em **ingles**
- Commits e PRs em **portugues brasileiro**
- Comentarios em codigo em ingles

## Comunicacao
- Respostas curtas e diretas, sem enrolacao
- Sem emojis (a menos que eu peca)
- Usar tabelas e listas quando facilitar a leitura
- Ao referenciar codigo, usar formato `arquivo:linha`

## Raciocinio
- Para decisoes de arquitetura, depuracao complexa ou analise de impacto em cascata: usar **ultrathink** no prompt
- Para tarefas triviais (fix simples, rename, consulta direta): manter esforco padrao
- `/effort` para ajustar nivel de esforco da sessao inteira

## Coding
- Nao over-engineer: resolver o que foi pedido, nada mais
- Nao adicionar docstrings/comments desnecessarios
- Nao criar arquivos novos se puder editar existentes
- Preferir solucoes simples sobre abstratas
- Seguranca: nunca commitar .env, credenciais ou tokens
- **`.claude.json` contem tokens em plaintext** (`env.ADO_PAT`, `env.ZENDESK_TOKEN`) — `bkp` copia para OneDrive. Ver memoria `security_tokens_claude_json.md`
- **ZIP pacote de entrega** (`MFS{WI_ID}_V2R010.zip`): NUNCA recriar/sobrescrever — e curado manualmente. So recriar `TESTES_{WI_ID}.zip`
- **Atalhos Desktop**: NUNCA criar .lnk no Desktop — nenhum projeto, instalador ou agente deve gerar atalhos

## Git
- Formato de branch: `MFS{WI_ID}` ou `MFS{WI_ID}a` (letra sufixo para branches adicionais do mesmo WI) — sem espacos (git nao aceita)
- Branch base: `RC` (taxone_dw), `rc` (ReportServer, conteudo)
- Nunca fazer commit sem eu pedir explicitamente
- Nunca fazer push sem eu pedir explicitamente
- Nunca usar --force ou --no-verify
- **Worktrees**: para WIs paralelos, usar `claude --worktree MFS{WI_ID}-descricao` (2-3 simultaneos max)
- **Titulo de PR**: SEMPRE prefixar com `[DEV]` ou `[RC]`. Se branch tem sufixo (a/b/c), incluir no titulo. Ex: `[DEV] MFS1121183a — fix X`
- **Ordem de PR (REGRA ABSOLUTA)**: 1o PR sempre para `DEV` (`base = DEV`). SOMENTE depois do PR-DEV ser **mergeado** e que pode abrir o PR para `RC`. Nunca abrir PR para RC enquanto DEV nao estiver mergeado, mesmo que a branch tenha sido criada a partir de RC. Ver memoria `feedback_pr_dev_first.md`
- **Titulo de commit**: NUNCA usar `[DEV]`/`[RC]`. Se branch tem sufixo (a/b/c), incluir no identificador. Ex: `MFS1121183a — fix X`
- **Trailer `Co-Authored-By`**: NUNCA incluir em commits IA. AITracker contabiliza autoria via SQLite (hook PostToolUse), nao via trailer Git. Ver memoria `feedback_no_coauthored_by.md`
- **Comando "commit"**: quando o usuario escrever `commit` (ou variantes "fazer commit", "pode commitar"), SEMPRE mostrar antes: (1) titulo proposto + body, (2) lista de objetos alterados com diff stat. Aguardar autorizacao explicita antes de rodar `git commit`. Ver memoria `feedback_commit_preview.md`

## Bancos de Dados

**Ver memoria completa:** `memory/db_rules.md`

**Hierarquia:**
- LOCAL (1521) — padrão R/W
- QA (10.226.81.223) — SELECT estrutura
- AC (10.226.81.116) — **READ-ONLY ABSOLUTO**
- PROD/UAT — via `/query-executor-prod-uat` SELECT apenas

**Regra ouro:** NUNCA UPDATE/DELETE/DROP em PROD sem autorização explícita

## Encodings padrao
- Regras por linguagem em `~/.claude/rules/` (plsql.md, powerbuilder.md, java.md, angular.md)
- **XML SuiteAutomation / SAFX flat-files**: ISO-8859-1 + CRLF — suite_runner.py / Write com encoding explicito
- **Nunca** converter ISO-8859-1 para UTF-8 (corrompe acentos)


## Ferramentas & Integrações

**Ver memoria completa:** `memory/tools_reference.md`

**APIs principais:**
- **ADO**: `tr-ggo` org, `ADO_PAT` env var
- **GitHub**: `gh` CLI, `GITHUB_TOKEN` env var
- **Zendesk**: `atendimentotr.zendesk.com`, API token
- **Datadog**: DD_API_KEY + DD_APP_KEY + DD_SITE
- **Docker**: `MSYS_NO_PATHCONV=1` no Git Bash (Windows)
- **OAuth**: `claude login` (console.anthropic.com bloqueado em rede corporativa)
- **CronCreate**: max 7 dias, sempre session-only
- **Compaction**: 1M beta (header `context-1m-2025-08-07`)

## Comentarios ADO (Discussion)
- Formato HTML: `<h3>`, `<table border=1 cellpadding=4>`, `<p><b>`, `<code>`, `<ol>/<ul>`
- **Nunca** fonte custom ou `style` de font-family
- **Nunca** mencionar nomes internos de pipelines/skills nos comentarios publicos


## @imports — Referencia sob demanda
- Estudos de modulos: `PROJETO/TR/RAIOX_MODULOS/ESTUDO_{MODULO}.md` — consultar antes de alterar objetos do modulo (path completo: `C:\Users\6107692\OneDrive - Thomson Reuters Incorporated\PROJETO\TR\RAIOX_MODULOS\`)
- Modulos disponiveis: EFD-REINF, SAFIL, EFD PIS/COFINS, SPED ECD, PARAMETROS, SAFUFIC (ICMS), EFD-ICMS/IPI, Ferramentas, Report Fiscal, SAFFDIR, SAFMUNPAR, SAFMUNIC
- Tabelas SAFX: colunas **nao** seguem padrao obvio — sempre validar na base local (x07=X07_DOCTO_FISCAL, x08=X08_ITENS_MERC/BASE/TRIB, x09=X09_ITENS_SERV/BASE/TRIB)
- Tabelas DWT_: Ferramentas > Tabelas Internas — exportadas via TACES##.TXT (TACES14=DWT_COD_RECEITA, TACES16=DWT_TRIBUTO). Campo `IND_DEB_SCPINC_R10` em DWT_COD_RECEITA indica tipo SCP/INC por Codigo de Receita (CHAR 1, exclusivo grp_tributo=10)
- 50 dicas Claude Code: `@_SANDBOX/50_dicas_claude_code.md`

## Projetos Pessoais
- BigDog, TheGate, ROBOCOP, PAPO — detalhes em memorias `project_bigdog.md`, `project_thegate.md`, `project_robocop_rewrite.md`, `project_papo.md`
- **ConsultaExpressa**: projeto independente em `PROJETO\ConsultaExpressa\` — **NUNCA** gerar artefatos no TheGate. Lucine/Allana/qualquer agente deve manter builds, RELEASE e instalador dentro do workspace ConsultaExpressa
- **DeleteFK**: projeto independente em `PROJETO\DeleteFK\` — mesma regra: builds e RELEASE no workspace, nunca no TheGate. Lucine roda no CWD
- **Logo TR**: `TheGate/PR_Assist/images/logo.png` | **Icone TR**: `TheGate/TR_Version_Viewer/TR_icon.ico`

## Agentes Customizados
- **Gigio**: Oracle INSERT/MERGE de CSV | **Kadu**: investiga WIs ADO+Zendesk+Datadog (read-only) | **qa-analise-demanda**: QA 10 passos | **Eduardoc** (Sonnet): ESTUDO_*.md
- "WI local" = numero da ultima pasta do diretorio atual (`MFS\{WI_ID}\`)

## Execucao de Comandos e Skills
- Ao executar QUALQUER comando ou skill, seguir **TODOS** os passos rigorosamente
- **Nao pular** nenhum passo, mesmo que pareca redundante
- **Nao resumir** ou simplificar — executar fielmente
- **Nao criar atalhos** — cada passo existe por um motivo
- Se um passo for condicional, avaliar a condicao mas nunca ignorar
- Ler instrucoes inteiras antes de comecar
- Isso vale para TUDO: skills, pipelines, agentes, scripts, comandos do usuario, qualquer instrucao
- **Agentes**: ao lancar qualquer agente (Agent tool), passar instrucoes completas e exigir execucao integral. Nao deixar o agente pular etapas

## Hooks Ativos

**Ver memoria completa:** `memory/hooks_setup.md`

**PreToolUse (Bash):** Bloqueia rm -rf, DROP, TRUNCATE, --force, --no-verify, DELETE sem WHERE, escrita em AC, --amend. Avisos em git push/commit.

**PreToolUse (Edit|MultiEdit):** Detecta ISO-8859-1 em .pck/.fon/.fnc/.trg/.vw/.prc/.typ.

**PostToolUse:** AITracker checkpoint + Prettier (TS/JS/HTML/CSS/JSON).

**AITracker:** Contabiliza Edit/Write apenas. Portal: `https://aitracker.cloudportal.thomsonreuters.com/`


## Atalhos de resposta
- `s` = sim
- `n` = nao

## Comandos Rapidos
- Ver `~/.claude/rules/comandos_rapidos.md` (oi, xau, linhas, taxonepipeline, equalize, assine, empacote, bkp, md, etc.)
- **`/oi`** — skill novo: startup completo (9 passos + lê IA.md). Ver memoria `skill_oi_startup.md`
- **`bkp` sempre executa `mg` antes** — salvar contexto completo antes de fazer backup
- **`equalize` — NUNCA recompilar nada em AC**, sem excecao. AC e read-only absoluto.

## Status Line
- Replicada exatamente como na TR
- Mostra: `cwd | branch | model | ctx:percentage% | $cost | compacts`
- Cores ANSI: verde (<50%), amarelo (50-80%), vermelho (>80%)
- Ver memoria `statusline_setup.md`

---

**Última atualização:** 2026-06-12 00:20 (mg executado)  
**Origem:** Backup Thomson Reuters (28/05/2026)  
**Versão:** TR Production (com regras de segurança críticas)  
**Contexto:** Sessão local sincronizada em C:\Users\educa\.claude\projects\C--Users-educa\memory\

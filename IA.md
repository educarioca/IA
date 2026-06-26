# Workspace IA — Meu Drive

**Diretório:** `G:\Meu Drive\IA\`  
**Status:** Production-Ready & Secured  
**Última atualização:** 2026-06-25 (mg executado)

---

## Visão Geral

Workspace pessoal para projetos IA, automação e experimentação. Baseado em padrões Thomson Reuters validados em produção.

---

## Estrutura Principal

```
IA/
├── .claude/
│   ├── rules/
│   │   └── comandos_rapidos.md          # Comandos pessoais
│   ├── skills/
│   │   ├── md_to_pdf/                   # MD→PDF com tema TR
│   │   └── oi/                          # Startup completo (8 passos)
│   ├── statusline.sh                    # Status line: cwd | branch | model | ctx | custo
│   ├── statusline-command.sh            # Script status line (replica TR)
│   ├── settings.json                    # Config: modelo Sonnet 4.6, status line
│   ├── settings.local.json
│   └── projects/G--Meu-Drive-IA/memory/
│       ├── MEMORY.md                    # Index de memórias
│       ├── session_2026-06-25_workspace_setup.md
│       ├── session_2026-06-25_oi_otimizado.md
│       ├── skill_oi_startup.md
│       ├── statusline_setup.md
│       ├── session_2026-06-12_statusline.md
│       ├── session_context.md
│       ├── backup_tr_explored.md
│       ├── db_rules.md
│       ├── hooks_setup.md
│       ├── tools_reference.md
│       └── feedback_git_direto.md
├── CLAUDE.md                             # Instruções globais
├── IA.md                                 # Este arquivo
└── .git/
```

---

## Git

| Item | Valor |
|------|-------|
| Branch ativa | `varsao_1.1` |
| Branches | `versao_1.0`, `varsao_1.1`, `master` |
| Commits | `639fc82` Primeira Versao / `4787a67` Initial commit |

---

## Status

| Item | Status | Detalhes |
|------|--------|----------|
| CLAUDE.md global | OK | ~142 linhas |
| Memórias ativas | OK | 6 arquivos indexados em MEMORY.md |
| StatusLine | OK | cwd \| branch \| model \| ctx:% \| $cost \| compacts |
| Skill /oi | OK | 8 passos otimizados |
| Skills | OK | md_to_pdf, oi |
| Modelo padrão | OK | Sonnet 4.6 |
| Dependências | OK | Python 3.12.5, Git 2.50.0, Node 20.16.0, npm 10.8.2 |

---

## Memórias Ativas

| Memória | Responsabilidade |
|---------|-----------------|
| session_2026-06-25_workspace_setup | Inicialização do workspace + branch varsao_1.1 |
| session_2026-06-25_oi_otimizado | Otimização da skill /oi (8 passos) |
| skill_oi_startup | Descrição da skill /oi |
| statusline_setup | Configuração da status line |
| backup_tr_explored | Exploração do backup TR |
| feedback_git_direto | Preferência: git commit/push direto sem aviso |

---

## Segurança

### Hooks Bloqueadores
- `rm -rf`, `DROP TABLE`, `TRUNCATE`
- `DELETE` sem WHERE
- `git --force`, `--no-verify`, `--amend`
- Escrita em AC (read-only absoluto)

### Credenciais
- Nunca commitar `.env`, tokens ou credenciais
- `CLAUDE.md` pode citar variáveis de ambiente — validar `.gitignore`

---

**Use `/oi` para startup automático em cada sessão.**

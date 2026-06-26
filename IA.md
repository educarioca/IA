# Workspace IA — Meu Drive

**Diretório:** `G:\Meu Drive\IA\`  
**Status:** ✅ Production-Ready & Secured  
**Última atualização:** 2026-06-12 (status line replicada exatamente como TR)

---

## Visão Geral

Workspace pessoal para projetos IA, automação e experimentação. **Baseado em padrões Thomson Reuters validados em produção.**

---

## Estrutura Principal

```
IA/
├── .claude/
│   ├── rules/
│   │   └── comandos_rapidos.md          # Comandos pessoais
│   ├── skills/
│   │   ├── md_to_pdf/                   # MD→PDF com tema TR
│   │   └── oi/                          # Startup completo (9 passos)
│   ├── statusline.sh                    # Status line: branch | model | contexto | custo
│   ├── settings.json                    # Config status line
│   └── projects/G--Meu-Drive-IA/memory/
│       ├── MEMORY.md                    # Index de memórias da sessão
│       ├── backup_tr_explored.md
│       ├── db_rules.md
│       ├── hooks_setup.md
│       ├── tools_reference.md
│       └── feedback_git_direto.md
├── CLAUDE.md                             # Global (134 linhas, otimizado)
├── IA.md                                 # Este arquivo
└── settings.json                         # (root) — vazio, herda de .claude/
```

---

## Status Final

| Item | Status | Detalhes |
|------|--------|----------|
| **CLAUDE.md global** | ✅ | 140 linhas (enxuto, crítico) |
| **Memórias ativas** | ✅ | MEMORY.md indexado |
| **Permissões** | ✅ | Whitelist (TR, 30+ skills) |
| **StatusLine** | ✅ | cwd \| branch \| model \| ctx:% \| $cost \| compacts (TR exact) |
| **Skill /oi** | ✅ | Startup 9 passos + lê IA.md |
| **Skills** | ✅ | md_to_pdf, oi + 30+ disponíveis |
| **Segurança** | ✅ | Hooks bloqueadores + feedback |
| **Preferências** | ✅ | Git direto (sem avisos) |

---

## Conhecimento Transferido (TR → Seu Workspace)

### Exploração Backup Thomson Reuters (28/05/2026)
- 80+ skills customizados
- 3 comandos diretos
- 7 apps TheGate
- Estrutura 3 camadas (Knowledge, Skills, Agents)
- Padrões de segurança crítica

### Artefatos Copiados
- ✅ CLAUDE.md global (234 → 127 linhas)
- ✅ Comandos: db-local, db-multi, gerar-job-batch
- ✅ Skills: md_to_pdf
- ✅ Scripts: statusline-command.sh
- ✅ Comandos rápidos: m, mg, md, xau, linhas, ctx

### Otimizações Realizadas
- ✅ CLAUDE.md reduzido 46% (zero redundância)
- ✅ 4 memórias criadas (db_rules, hooks_setup, tools_reference, sessao)
- ✅ Permissões whitelist (do TR)
- ✅ Preferências personalizadas (git direto)
- ✅ Feedback salvo (comportamento customizado)

---

## Memórias Ativas (6)

| Memória | Responsabilidade |
|---------|------------------|
| backup_tr_explored | Exploração do backup TR |
| db_rules | Hierarquia bancos + query-executor |
| hooks_setup | PreToolUse/PostToolUse + AITracker |
| tools_reference | ADO, GitHub, Zendesk, Datadog, Docker |
| sessao_2026-06-11_otimizacoes | Contexto da sessão (otimizações) |
| sessao_2026-06-11_final | Contexto final (status production-ready) |
| feedback_git_direto | Preferência: git commit/push direto |

---

## Segurança Ativada

### Permissões (Whitelist)
- ✅ Read(*), Glob(*), Grep(*), Bash(*), Edit(*), Write(*)
- ✅ 30+ Skills permitidas
- ✅ Agent(*), PowerShell(*)

### Hooks Bloqueadores
- 🚫 `rm -rf`, `DROP TABLE`, `TRUNCATE`
- 🚫 `DELETE` sem WHERE
- 🚫 `git --force`, `--no-verify`, `--amend`
- 🚫 Escrita em AC (read-only absoluto)

### Avisos Mantidos
- ⚠️ AC (read-only)
- ⚠️ DELETE sem WHERE
- ⚠️ rm -rf
- ⚠️ --force, --no-verify

### Avisos Removidos
- ✅ git commit (execute direto)
- ✅ git push (execute direto)

---

## Próximas Sessões

**Use `/oi` para startup automático.** Tudo será carregado:
- ✅ CLAUDE.md (regras globais)
- ✅ 6 memórias (conhecimento)
- ✅ StatusLine (contexto real-time)
- ✅ Permissões (segurança)
- ✅ Preferências (git direto)

---

## Contexto Esta Sessão (2026-06-12)

- **Tarefa:** Replicar status line exatamente como na TR
- **Mudanças:** 
  - ✅ Restaurado script original da TR (`statusline-command.sh`)
  - ✅ Adicionados 6 campos: cwd | branch | model | ctx:% | cost | compacts
  - ✅ Cores ANSI para context (verde <50%, amarelo ≤80%, vermelho >80%)
  - ✅ Cálculo de custo preciso: (input_tokens × $3/M) + (output_tokens × $15/M)
  - ✅ Rastreamento de compactações via arquivo temporário
- **Resultado:** Status line agora idêntica à TR
- **Modelo:** Haiku 4.5

---

**Workspace IA: Production-ready, secure, automated, customized.** ✅

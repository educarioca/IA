---
name: oi
description: Startup completo — sincroniza git, carrega memória, valida ambiente, mostra resumo e status do projeto
version: 1.0.0
---

# OI — Startup Completo

Executa 9 passos de inicialização sensata para começar a trabalhar no projeto.

## When to Use

Use this skill quando:
- Iniciar uma nova sessão no projeto
- Retornar após pausa
- Sincronizar estado local com remoto
- Verificar saúde do ambiente

### Examples that SHOULD trigger this skill

- `oi`
- `startup`
- `iniciar`

## How to Execute

```bash
python "${SKILL_DIR}/scripts/oi.py"
```

## O que faz (9 passos)

1. **Git Status** — mostra branch atual, arquivos modificados, commits pendentes
2. **Git Sync** — faz pull se houver atualizações remotas (sem force)
3. **Memória do Projeto** — carrega MEMORY.md e mostra resumo
4. **CLAUDE.md** — valida instruções e mostra avisos críticos
5. **Dependências** — checa python, npm, docker (se aplicável)
6. **Skills & Agentes** — lista skills disponiveis e status
7. **Hooks** — valida hooks git configurados
8. **Resumo do Projeto** — mostra estrutura, arquivos críticos, últimos commits
9. **Status Line** — atualiza contexto da sessão

## Output

Relatório estruturado com:
- Status git (branch, commits, conflitos)
- Warnings se houver situações anormais
- Lista de dependências e suas versões
- Próximas ações sugeridas

## Dependencias

- Python 3.8+
- Git
- (Outras validadas dinamicamente)

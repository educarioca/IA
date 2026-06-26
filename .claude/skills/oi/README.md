# OI — Startup Otimizado

Inicializa o workspace pessoal, atualiza ferramentas e valida ambiente.

## O que faz (8 passos)

1. **Git Status** — Branch, arquivos modificados, últimos commits
2. **Sincronizar com Remoto** — `git fetch` e atualizar branch (se repo git)
3. **Memória do Projeto** — Carrega MEMORY.md e contexto salvo
4. **CLAUDE.md** — Valida instruções do projeto
5. **Validar Dependências** — Checa Python, Git, Node, npm
6. **Atualizar Python** — `pip upgrade` + `pip install -r requirements.txt`
7. **Atualizar Node** — `npm install` (se package.json existir)
8. **Resumo Final** — Status de todas as ferramentas

## Uso

```bash
/oi
```

ou

```bash
python "g:\Meu Drive\IA\.claude\skills\oi\scripts\oi.py"
```

## O que foi removido vs. versão TR

| Item | Razão |
|------|-------|
| Hooks Git | Não é um repo git funcional |
| Skills corporativas | Gigio, Kadu, qa-analise não existem aqui |
| Validação de módulos | Sem acesso a SAFX/Oracle corporativo |
| Status line TR | Específico do ambiente TR |

## O que foi adicionado

✅ Atualização automática de `pip`  
✅ Instalação de `requirements.txt`  
✅ Instalação de `package.json` (npm install)  
✅ Tracking de atualizações aplicadas  
✅ Melhor resumo de ferramentas disponíveis  

## Output esperado

```
======================================================================
  OI — STARTUP OTIMIZADO
======================================================================

[1/8] Git Status
...

[6/8] Atualizar Python Packages
Atualizando pip...
Instalando requirements.txt...

[7/8] Atualizar Node Packages
Instalando/atualizando node_modules...

[8/8] Resumo do Projeto
...

======================================================================
  STATUS FINAL
======================================================================

✅ ATUALIZAÇÕES APLICADAS:
  ✓ Python packages atualizados
  ✓ Node packages instalados

Pronto para trabalhar! 🚀
```

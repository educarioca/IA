# Comandos Rapidos

Comandos com passos detalhados: ler `reference_comandos_detalhes.md` da memoria ANTES de executar.

## Comandos simples (ficam como comandos)
- `memoria` ou `m` = salvar contexto na memoria do projeto atual
- `memoria global` ou `mg` = executar `m` + `md` + salvar contexto no CLAUDE.md global. Os tres em sequencia.
- `xau` = executar `memoria` e sugerir `/exit`.
- `linhas` = contar linhas CLAUDE.md global, listar memorias, sugerir reducoes. Executar direto.
- `meus filhos` = listar skills/agentes pessoais + comandos rapidos + tabela `meus projetos`. Executar direto.
- `custo mes` = `python ~/bin/custo.py --mes` (ultimos 3 meses). Aceita `custo mes N`.
- `md` = criar/atualizar `{NOME_DA_PASTA}.md` do workspace. Maximo de detalhes. Nunca README.md. Executar direto.
- `meus projetos` = 4 tabelas (TheGate, BigDog, TaxonePipeline, ROBOCOP). **Ler detalhes na memoria.** Executar direto.
- `ctx` = reportar uso de contexto + atualizar status line. Executar direto.

## Comandos que agora sao skills (usar /skill ou alias)
- `finalize` = `/finalize` — cenario + plano de testes + empacote + md (4 passos sequenciais)
- `cenario local/qa` = `/cenario local` ou `/cenario qa` — massa de teste SAFX (7 passos). Aliases: `massa local`, `massa qa`
- `equalize X Y` = `/equalize X Y` — equalizar objetos Oracle entre bases. NUNCA recompilar em AC
- `validar commit {WI_ID}` = `/validar-commit {WI_ID}` — panorama git completo do WI
- `bkp` = `/bkp` — mg + FULL zip + MIN zip para OneDrive\MeusFilhos
- `empacote {assunto}` = `/empacote {assunto}` — pasta TESTES_{WI_ID} distribuivel + ZIP
- `taxonepipeline {PIPELINE} {WI_ID}` = `/taxonepipeline {PIPELINE} {WI_ID}` — GUI + skill correspondente
- `tenants` = busca tenants.json mais recente em Downloads, confirma e distribui para 5 destinos (sem regenerar — usa o arquivo do portal)
- `tenants-refresh` = `/tenants-refresh` — regenera tenants.json via tenant-export e distribui (descarta Ansible Report). Requer secrets.json CIAM

## Comandos com skill equivalente (alias — rodam a skill)
- `oi` = `/oi` (startup completo, 9 passos)
- `assine {arquivo}` = `/assine {arquivo}` — assinatura IA + AITracker
- `atualizar` = `/atualize-tudo` — git pull + sync agentes/skills

## Comandos de teste (tres niveis)
- `tester` = gerar `TESTES_{WI_ID}.md` (11 secoes: resumo, causa raiz, fix, objetos, diff OLD/NEW, dados teste, pre-condicoes, roteiro passo-a-passo, SQLs validacao, criterios aceite, regressao) + `{WI_ID}_tester.zip` com todos os artefatos (MD + SQLs + OBJETOS OLD/NEW). Pasta: `MFS/{WI_ID}/`. **Ler detalhes na memoria global `feedback_tester_command.md`.**
- `plano de testes` = `plano_teste_{WI_ID}.md` com 10 secoes + TCs. Leve, sem ADO. **Ler detalhes na memoria.** Executar direto.
- `/task-revisao-tdd` = versao completa: plano + enriquecimento schema/git + massa SAFX + scripts SQL + relatorio HTML + Task no ADO

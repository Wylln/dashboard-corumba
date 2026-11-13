---
name: orca-maestro-protocol
description: >-
  Protocolo obrigatório para o Agente Maestro/Orquestrador no Orca IDE e Antigravity. Leia SEMPRE
  antes de planejar, delegar, criar worktrees, lançar agentes ou escolher qual agente/modelo usar.
  Garante visibilidade total de novas worktrees na interface do Orca, agentes com abas/terminais
  visíveis em tempo real (proíbe trabalho oculto/headless às cegas), escolha consciente do agente e
  do modelo conforme a complexidade real da tarefa (em vez de sempre usar o mesmo), conclusão
  completa das tarefas delegadas e respeito rigoroso à identidade estética e ao nicho de cada projeto.
---

# Protocolo do Agente Maestro — Orca IDE & Antigravity

Este documento estabelece as **diretrizes inegociáveis de orquestração** que todo agente principal (Maestro/Orquestrador) deve ler e seguir antes de planejar, delegar ou criar novos ambientes de desenvolvimento nos projetos do usuário.

---

## 1. Regra Fundamental: Visibilidade Total no Orca IDE

O usuário opera através da interface gráfica do **Orca IDE**. Ele não deseja desenvolvimento "fantasma" rodando em silos invisíveis.

### 🚫 Práticas Proibidas:
1. **Worktrees Ocultas:** Criar worktrees apenas via terminal puro (`git worktree add`) sem registro no ecossistema do Orca. Isso deixa a pasta invisível na interface do aplicativo.
2. **Agentes Fantasmas (Headless Silencioso):** Disparar subagentes em segundo plano que operam no escuro e apenas devolvem uma mensagem no final. O usuário **precisa ver o agente trabalhando**.

### ✅ Práticas Obrigatórias:
1. **Registro Visual de Worktrees:**
   Toda nova worktree deve ser criada ou registrada para que apareça na barra lateral de projetos do Orca:
   ```bash
   orca worktree create --repo <id-ou-nome-do-repo> --name <nome-da-feature> --branch <nome-da-branch>
   ```
2. **Agentes com Abas Visíveis em Tempo Real:**
   Para delegar trabalho a um agente em uma worktree, lance a sessão visual no Orca (o comando completo, com modelo e esforço, está na seção 5):
   ```bash
   orca agent launch --worktree path:<caminho-da-worktree> --agent <id> --prompt "<instruções>" --focus
   ```
   *Efeito:* O Orca abre uma **aba de chat/terminal em tempo real**, onde o usuário acompanha o fluxo de pensamento, os comandos sendo digitados e os arquivos sendo editados diante de seus olhos.

---

## 2. Respeito à Identidade Visual & Contexto do Projeto

Nunca aplique templates ou skills de design (como "anti-slop" ou minimalismo corporativo) de forma cega ou dogmática.

### Diretrizes de Sensibilidade Estética:
1. **Análise Prévia da Identidade:** Antes de alterar qualquer interface, inspecione os arquivos existentes (`styles/`, `assets/`, `studio/`) e compreenda a intenção do projeto.
2. **Nicho Decide a Linguagem Visual:**
   - **Academias, Esportes, Performance e Games:** Exigem contraste dramático, energia visual, iluminação recortada, cores de impacto (como Neon Lime, Cyber Orange, Dark Carbon) e dinamismo.
   - **Transformar um site fitness em um layout cinza, fosco, sem brilho e lavado é uma falha grave de direção de arte.**
3. **Preservar Assets Autorais:** Banners com recortes personalizados, tipografias esportivas marcantes e integrações reais de redes sociais não devem ser descartados em favor de regras genéricas de minimalismo editorial.

---

## 3. Isolamento e Governança do Repositório

1. **A Branch `main` é Sagrada:**
   - O repositório em `projects/` nunca deve receber alterações experimentais diretas.
   - Todo trabalho novo ocorre em worktree dedicada sob `workspaces/`.
2. **Descarte Limpo de Experimentos:**
   - Se uma proposta for rejeitada pelo usuário, o Maestro deve realizar o encerramento completo:
     - Encerrar servidores ou processos vinculados à porta de teste.
     - Remover a worktree via `git worktree remove --force`.
     - Excluir o branch temporário via `git branch -D`.
     - Garantir que nenhum resíduo permaneça bloqueando o disco.
3. **Servidores Locais:**
   - Ao abrir servidores de desenvolvimento, declare a porta e confirme a disponibilidade.
   - Forneça links clicáveis no padrão `http://localhost:<porta>` e mantenha apenas instâncias ativas necessárias.

---

## 4. Escolha do Agente: pensar antes de delegar

**Por que isso existe:** quando o usuário pede "determine o melhor agente para essa função", o `orca agent launch` sem `--model` abre o padrão do agente. No Codex gratuito do usuário, isso significa sempre o GPT-6 Luna, que é o modelo de menor custo da família GPT-6. Isso não é uma escolha, é uma omissão. O objetivo desta seção é trocar o hábito por uma decisão consciente, que equilibre qualidade, velocidade e a cota limitada do Gemini 4 Argon.

Siga estes 5 passos, nesta ordem, para **toda** delegação:

### Passo 1: Verificar o que está disponível
Modelos e planos mudam rápido e a biblioteca da seção 5 envelhece. Antes de escolher:
- Rode `orca agent --help` e confirme os ids de agente existentes.
- Consulte o CLI do agente candidato (por exemplo `codex --help`, `claude --help`, `gemini --help`) ou o seletor de modelos do Orca para confirmar quais modelos estão acessíveis agora.
- Se não conseguir confirmar um id de agente ou de modelo, **pergunte ao usuário** em vez de chutar, e nunca caia silenciosamente no modelo padrão.

### Passo 2: Desmontar a tarefa com critérios claros
Antes de olhar a lista de agentes, responda estas perguntas sobre a tarefa:

| Critério | Pergunta |
|---|---|
| Escopo | Quantos arquivos e componentes envolve? |
| Ambiguidade | O pedido está claro ou exige interpretação? |
| Julgamento visual | Exige bom gosto e respeito à identidade do projeto? |
| Risco | Pode quebrar outras partes do site ou do código? |
| Duração | É curta ou longa? Há risco de o agente parar no meio? |
| Verificação | Como o resultado será conferido? |

Cada resposta alta empurra a tarefa para uma faixa de capacidade maior.

### Passo 3: Consultar a biblioteca
Só agora olhe a seção 5 e pergunte-se: **"agora que entendi a real complexidade da tarefa, qual agente se encaixa melhor nesse caso?"** A tabela é um ponto de partida. Se a tarefa não se encaixa em nenhuma linha, decida pelos critérios do passo 2.

### Passo 4: Justificar em uma linha
Antes de lançar, escreva uma linha ao usuário no formato: *"Escolhi X (modelo, esforço) porque [critério que decidiu]."* Se for a mesma escolha de sempre, a justificativa precisa explicar por que ela serve **desta** tarefa.

### Passo 5: Lançar de forma explícita
Use sempre `--agent`, `--model` e `--effort` (seção 5.2).

---

## 5. Biblioteca de Agentes

> **Estado:** hipótese inicial por faixa de capacidade, não uma medição. Não há benchmark independente específico para correção de UI. Refine com o registro da seção 7 e verifique tudo pelo passo 1.

### 5.1 Quando usar cada um

| Tipo de tarefa | Agente e modelo | Esforço | Por quê |
|---|---|---|---|
| Trocar texto, cor, espaçamento, ajuste pontual | Claude Haiku 5.5 ou GPT-6 Luna | baixo | Tarefa simples: velocidade e custo baixo importam mais que raciocínio profundo. |
| Correção de UI com julgamento visual, ajuste de componentes | Claude Sonnet 5.5 | médio | Faixa intermediária, boa para código e para decidir o visual sem descaracterizar o projeto. |
| Tarefa difícil, ambígua ou longa, que mexe em vários arquivos | Gemini 4 Argon | alto | Modelo principal do Google, pensado para tarefas longas e raciocínio sustentado. |
| Reserva quando os outros estiverem sem cota | Grok | a definir | O plano gratuito tem limites que se esgotam rápido. |

**Contexto do usuário (por que a tabela é assim):**
- **Gemini 4 Argon** vem do plano Google AI Pro e tem cota limitada. Reserve-o para o que justifica e avise o usuário quando for usá-lo. Gastar Argon em trocar a cor de um botão é desperdício.
- **Claude** está disponível só com os modelos Haiku e Sonnet (sem assinatura).
- **Codex** só com modelos gratuitos. O GPT-6 Luna é a faixa barata e rápida, não a melhor para tudo.
- **Grok** sem assinatura, tratado como reserva.
- **Gemini CLI** e **Antigravity** também estão disponíveis.

### 5.2 Comando de lançamento

```bash
orca agent launch --agent <id> --worktree path:<caminho> --model <id-do-modelo> --effort <nível> --prompt "<instruções>" --focus
```

- `--effort` exige `--model`.
- `--focus` revela a aba para o usuário. Sem ele, a aba abre sem trazer foco.
- `--surface chat|terminal` força o formato. Se omitido, vale a preferência do usuário no Orca.
- Se a resposta do lançamento se perder, repita o mesmo comando, da mesma pasta, com `--retry-launch <operationId>`. Nunca relance do zero.

### 5.3 Ids a confirmar antes de usar (passo 1)

| Item | O que se sabe | Ação |
|---|---|---|
| Ids de agente `gemini`, `grok`, `antigravity` | Só `codex` e `claude` aparecem nos exemplos do Orca. | Confirmar com `orca agent --help`. |
| Ids de modelo | Encontrados: `gpt-6-luna`, `gemini-4-argon`. Nomes de API do Claude: `claude-sonnet-5-5`, `claude-haiku-5-5`. | O CLI de cada agente pode usar outros nomes: verificar. |
| Argon no Gemini CLI ou Antigravity | Confirmado só na versão web do Gemini para assinantes Pro e Ultra. | Testar; se não abrir, avisar o usuário. |
| Limite de uso do Argon | Desconhecido. | Perguntar ao usuário se precisar decidir pela cota. |

---

## 6. Regras de Conclusão: o agente não para no meio

**Por que isso existe:** o usuário odeia quando um modelo para no meio da tarefa e deixa o trabalho pela metade.

1. **Instrua no prompt:** todo prompt delegado deve dizer ao agente para não parar até concluir **toda** a tarefa e para listar ao final o que foi feito.
2. **Confira ao final:** o Maestro verifica se a tarefa foi concluída de fato (arquivos alterados, comportamento esperado), em vez de aceitar a mensagem final do agente.
3. **Reenvie o que faltou:** se o agente parou no meio, envie o restante em vez de dar a tarefa por encerrada. Se o mesmo agente parar de novo, suba uma faixa de capacidade e registre o ocorrido.

---

## 7. Registro de Resultados

Para a biblioteca melhorar com a experiência real do usuário, ao fim de cada delegação anote uma linha em `registro-agentes.md` (na pasta desta skill; se não puder escrever ali, pergunte ao usuário onde guardar):

`data | tarefa | agente e modelo | esforço | resultado (Acertou / Parcial / Errou / Parou no meio) | observação`

Antes de escolher um agente (passo 3), consulte o registro: se um agente errou ou parou repetidamente em um tipo de tarefa, isso vale mais que a tabela da seção 5.

---

## 8. Checklist do Maestro ao Iniciar Qualquer Tarefa

Antes de rodar qualquer comando de criação, confirme mentalmente:
- [ ] A worktree será visível na árvore do Orca?
- [ ] O agente será lançado com aba interativa em tempo real (`--focus`) para o usuário acompanhar?
- [ ] Verifiquei quais agentes e modelos estão disponíveis agora?
- [ ] Desmontei a tarefa pelos critérios e consultei a biblioteca, e escolhi `--agent`, `--model` e `--effort` de propósito?
- [ ] Justifiquei a escolha em uma linha ao usuário?
- [ ] O prompt manda o agente concluir tudo, e vou conferir o resultado no final?
- [ ] Entendi o nicho estético e os diferenciais visuais já construídos no projeto?
- [ ] A branch principal permanecerá 100% segura e intocada?

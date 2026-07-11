# TabNews pitch (PT-BR) — technical "how it's built" story

**STATUS: DRAFT — needs native review before posting.** Machine-assisted
Brazilian Portuguese; a native speaker must review before publishing.
Venue: https://www.tabnews.com.br — TabNews norms explicitly welcome
pitches that share technical knowledge; this is written as a technical
architecture story with the pitch disclosed, not an ad. Disclosed-maker
voice. Plan ref: `plan-q3-distribution.md` Phase 2, language wave 1 (PT).

---

**Título:** Pitch: construí um editor de workflows de IA que é um único
arquivo HTML — sem servidor, sem conta, sem analytics

Olá, TabNews! Sou o autor do projeto, então isto é um pitch — mas o que
quero compartilhar de verdade é a arquitetura, porque as restrições que
escolhi produziram os problemas de engenharia mais interessantes que já
enfrentei num projeto solo.

O projeto: **nanoodle** (https://nanoodle.com, interface em português:
https://nanoodle.com/pt/) é um editor de grafos de nós — estilo ComfyUI —
para encadear modelos de IA (texto, imagem, vídeo, áudio) no navegador.
Código aberto, MIT: https://github.com/nanoodlecom/nanoodle

A restrição central: **o produto inteiro é uma página HTML estática**. Sem
backend, sem build, sem bundler, zero analytics. Disso caem quatro
histórias técnicas:

## 1. Exportar um app como um único arquivo .html

Qualquer grafo pode ser exportado como um aplicativo autônomo de **um
arquivo só**, com o runtime embutido. Isso significa que o runtime
JavaScript vive dentro da página, num template `String.raw` — e um único
backtick perdido em qualquer lugar desse bloco quebra TODOS os exports.
Existe um hook de pré-commit cujo único trabalho é caçar backticks.

Consequência maior: o editor e o app exportado são **dois motores de
execução gêmeos** que precisam se comportar de forma idêntica. A "deriva"
entre os dois virou a principal classe de bugs do projeto, então a paridade
também é imposta por hooks (o repositório tem cerca de 40 guardas de
pré-commit no total).

## 2. Sandbox via iframe srcdoc

Apps rodam dentro de um iframe `srcdoc` com sandbox. Detalhe que dói
aprender na prática: um iframe `srcdoc` não tem storage próprio — então
persistência de resultados exigiu uma ponte com o IndexedDB da página
hospedeira, com consentimento explícito.

## 3. URLs de compartilhamento compactas

Compartilhar um grafo é gerar uma URL onde o grafo inteiro vai codificado
no **fragmento** (depois do `#`). O navegador nunca envia o fragmento ao
servidor, então o link é ilegível para qualquer hospedeiro — por
construção. O problema virou engenharia de orçamento de bytes: encurtadores
e intermediários impõem tetos práticos de tamanho de URL, então o formato
de compartilhamento aprendeu a despachar apps não-customizados **sem** os
arquivos default (o decodificador os reconstrói do outro lado) para caber
no teto. Depurar por que um link "pendurava" num encurtador acabou virando
uma investigação de HTTP/3 à parte.

## 4. Executores com zero dependências

Um grafo salvo é JSON. Para rodar fora do navegador existem duas
bibliotecas **sem nenhuma dependência**:

- JavaScript: `npm install nanoodle` — https://github.com/nanoodlecom/nanoodle-js
- Python: `pip install nanoodle` — https://github.com/nanoodlecom/nanoodle-py

As duas são testadas para produzir payloads idênticos byte a byte — o mesmo
grafo dá o mesmo resultado no navegador, no Node e no Python.

## O trade-off honesto

Não existe almoço grátis: sem servidor significa **traga sua própria
chave**. Os modelos rodam pela API da nano-gpt.com com a SUA chave, paga
por chamada (uma estimativa de custo aparece antes de cada execução; o
nanoodle não cobra markup — a receita é um programa de indicação do
provedor, declarado abertamente). Editar, compartilhar e exportar não
precisam de chave nem de conta. E privacidade aqui é verificável, não
prometida: a Content-Security-Policy não permite nenhuma origem de
terceiros — a aba Network do DevTools é o recibo.

## Perguntas para a comunidade

- Alguém já levou o modelo "produto = um arquivo estático" a sério em
  produção? Onde ele quebrou para vocês?
- Há interesse num detalhamento maior de alguma das quatro partes acima
  (posso escrever um post técnico dedicado)?

Crítica dura é bem-vinda — de arquitetura ou de produto.

---

**Submission notes (EN, not part of the post):**
- TabNews rewards substance and punishes drive-by promo: stay in the
  thread and answer every technical question same-day.
- If a dedicated deep-dive is requested, the da.gd/HTTP3 header-stall
  investigation is the strongest candidate (also earmarked as the October
  war-story launch in `launch-runbook.md`).
- Log in `growth/shares.md`.

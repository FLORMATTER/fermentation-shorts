# Como ganhar dinheiro com esses vídeos

**23/09/2026** · Todo número aqui foi checado hoje, com fonte. Nada de "ouvi dizer".

---

## 1. O diagnóstico em uma linha

Você tem uma **fábrica de conteúdo** e **zero distribuição**.

26 vídeos prontos, 25 com `.mp4` renderizado, roteiros, títulos, descrições, hashtags,
plano de 16 semanas — e **nada publicado**, porque o canal não existe e o nome não foi
escolhido.

> **Nada publicado = R$ 0.** Todo o resto deste documento é sobre qual é o caminho mais
> curto de zero até o primeiro dinheiro.

O gargalo **nunca foi produzir**. Você resolveu isso. O gargalo é **publicar** — e escolher
o **formato certo** para monetizar, que não é o que você construiu.

---

## 2. 🔴 A descoberta que muda o plano: Shorts não monetizam

Este é o ponto mais importante do documento e ele contraria o senso comum.

O YouTube publicou em **12/08/2026** (blog oficial, Rene Ritchie) a definição de "horas
qualificadas". A lista do que **não** conta:

> Watch hours that do not count as qualified include: Private videos, Unlisted videos,
> Deleted videos, Videos watched as an ad, **Shorts watch hours**, Live streams that aren't
> archived.

**Hora assistida de Short NÃO conta para as 4.000 horas.** Não existe meio-termo. Para
entrar no Programa de Parceiros com Shorts existe **um caminho só**:

> **10.000.000 de *engaged views* em 90 dias.**

E "engaged" é restritivo: exclui **loop** e exclui quem saiu nos primeiros segundos.

### O que isso quer dizer na prática

| Caminho | A barra | Traduzindo |
|---|---|---|
| **Só Shorts** | 10 mi de engaged views / 90 dias | **~111 mil views por dia, todo dia, sem falhar** |
| **Vídeo longo** | 4.000 horas assistidas / 365 dias | ~45 mil views de um vídeo de 12 min (45% de retenção) |

O segundo é **muito** mais alcançável. E paga mais:

| Formato | RPM | Por 1 milhão de views |
|---|---|---|
| **Shorts** (nicho comida) | US$ 0,06 – 0,12 | **US$ 60 – 120** |
| **Vídeo longo** | US$ 3 – 8 bruto · 1,35 – 3,60 líquido | **US$ 1.350 – 3.600** |

**10 a 50 vezes mais por view.**

> **O Short traz gente. O vídeo longo é onde o dinheiro está.** O seu próprio roteiro
> (`video-longo/roteiro-video-longo-7-legumes.md`) já dizia exatamente isso — e o plano de
> postagem colocou o único vídeo longo na **Semana 7**, como se fosse um item da lista.
> Ele não é um item da lista. **Ele é o objetivo.**

---

## 3. ⏰ O prazo: 131 dias

Em **10/08/2026** o YouTube anunciou que, a partir de **1º de fevereiro de 2027**, a barra
de entrada **dobra**:

| | Até 31/01/2027 | De 01/02/2027 |
|---|---|---|
| Horas assistidas (365 d) | 4.000 | **8.000** |
| Views de Shorts (90 d) | 10 milhões | **20 milhões** |

E tem uma pegadinha para quem entra agora: quem já está no programa mas **cai abaixo de
10 milhões de views de Shorts em 90 dias** tem o **dinheiro de Shorts pausado** (o
long-form, Fan Funding, Memberships e Shopping continuam).

Hoje é 23/09/2026 → **131 dias** para entrar na regra velha.

Isso não é motivo para pânico. É motivo para **publicar esta semana** em vez de em janeiro.
Quatro meses de postagem consistente é exatamente a diferença entre pegar a barra de 4.000
e a de 8.000.

---

## 4. ✅ A decisão que você já tomou certo (sem saber)

Seu canal é **em inglês**. Isso não é detalhe de estilo — é dinheiro, e a diferença é grande:

| Público | RPM (Shorts) |
|---|---|
| EUA, nicho geral | US$ 0,08 – 0,15 |
| EUA, alto CPM (finanças, tech, saúde) | US$ 0,15 – 0,25 |
| Reino Unido / Canadá / Austrália | US$ 0,06 – 0,12 |
| **América Latina** | **US$ 0,02 – 0,05** |

O mesmo vídeo, com o mesmo número de views, rende **3 a 5 vezes mais** com público
americano. **Não traduza os vídeos para português.** Se algum dia quiser público BR, faça
um **canal separado** — nunca o mesmo.

O nicho "comida" é o ponto fraco do seu projeto (US$ 0,06 – 0,12, contra 0,15 – 0,25 de
finanças). Mas você tem uma vantagem que a maioria dos canais de comida não tem: **o seu
conteúdo é ciência, não receita.** "A betalaina só é estável entre pH 3 e 6" é conteúdo de
educação, e educação paga **US$ 0,08 – 0,15** — melhor que comida. **Empurre o canal para
o lado "explicação", não para o lado "receita".** Isso já está na sua série; é só assumir.

---

## 5. As quatro rotas, em ordem de retorno

### 🥇 Rota 1 — Vídeo longo (a base: lenta, sólida, e é a única que monetiza)

**O que fazer:** virar o material dos Shorts em vídeos de 8 a 15 minutos, 16:9.

Você tem **duas** fontes de vídeo longo, e as duas já existem:

**(a) O player "7 legumes" — 45 cenas animadas, 16:9, já escritas e traduzidas.**
Está parado por um detalhe técnico. O que eu verifiquei no código:

- O `_gerar-mp4.js` **não** grava esse arquivo — mas o motivo é mais estreito do que
  parece. A linha `if (/player-video-longo/.test(f)) return false;` está no filtro do
  **lote** (`--todos`), e o comentário logo acima diz: *"argumento explícito não passa por
  este filtro"*. Ou seja: **o filtro não é o problema.**
- **O problema real é o motor.** O `_mp4/render.js` é específico de Short: ele faz
  `var S = W / 405` (o cartão 405×720), lê a estrutura `svg.scene` e **desenha a própria
  barra de legenda**. O player monta as cenas por JavaScript com outro formato (`CAPS`,
  `ci`, `si`, `elapsed`) e tem o **seu próprio** motor de tempo. O motor de mp4 não sabe
  conversar com ele.
- **A boa notícia:** o player **já foi projetado para isso.** Ele tem um modo `?rec` cujo
  comentário no código diz literalmente *"o quadro preenche 1080x1920 (**1920x1080 no
  vídeo longo**)"* — esconde capa e botões, escala o palco e dá play sozinho.

**O que falta, então, não é gravar: é software.** Um renderizador 16:9 que dirija a
linha de tempo do player e capture os quadros. É trabalho **bounded** — reaproveita a
técnica de MediaRecorder + CFR já provada no `render.js`, e a parte chata (o modo de
gravação limpo) o player já entrega pronta.

> ⚠️ **Correção de uma versão anterior deste documento:** eu havia escrito que bastava
> "passar o arquivo pelo nome". **Não basta** — o filtro do lote não é o bloqueio; o motor
> é. O trabalho continua sendo software e não gravação, mas é maior do que uma linha de
> comando.

**E o roteiro pede filmagem de celular** (o legume de verdade, 7 trechos). A versão 100%
animada **se sustenta sozinha** e não depende de você filmar nada — mas seja honesto
consigo: 12 minutos de animação pura, sem nenhuma imagem real, cansam mais que 12 minutos
com respiro. Se a versão animada performar, os 7 trechos de celular viram a **segunda**
versão do mesmo vídeo, não a primeira.


**(b) Compilações temáticas dos Shorts.** Você tem 26 assuntos que se agrupam:

| Tema | Shorts | Vira um vídeo de |
|---|---|---|
| Kombucha: 4 frutas, 4 lições | #23, #24, #25, #26 | ~12 min |
| Beterraba: o guia completo | #3, #4, #8, #14, #19, #25 | ~15 min |
| Os 3 erros que matam uma fermentação | #1, #11, #17, #20 | ~10 min |
| Repolho e couve: sal e tempo | #1, #2, #8, #20 | ~10 min |

⚠️ **Cuidado com a sua própria regra:** "conteúdo em massa / não autêntico". Empilhar 4
Shorts e chamar de vídeo longo é exatamente o padrão que derruba canal. A compilação só
vale se tiver **substância nova**: comparação, conclusão, o "o que eu faria diferente".
O Short #25 ensina que a cenoura salva o vermelho da beterraba; o #26 ensina a janela de
pH. **Juntos** eles ensinam algo que nenhum dos dois ensina: *como escolher a fruta certa
para manter a cor*. Isso é um vídeo longo. Quatro Shorts colados não são.

**Meta:** 4.000 horas assistidas.
**Receita:** US$ 1,35 – 3,60 por 1.000 views. Um vídeo de 12 min com 45 mil views ≈
**US$ 60 – 160**.
**Prazo honesto:** 3 a 9 meses de postagem consistente. É a rota mais lenta e a única que
constrói um ativo que continua rendendo.

### 🥈 Rota 2 — Afiliado e produto digital (mais rápida: não depende do algoritmo)

**Não espere o AdSense.** Estas duas linhas rendem antes de você ter 1.000 inscritos.

**Afiliado.** Seus vídeos mostram, em close: pote de vidro, airlock, peso de cerâmica, fita
de pH, sal sem iodo. Todo mundo que assiste quer comprar isso. **Link na descrição, sempre.**
Você já tem 26 vídeos prontos para receber o link — é editar a descrição, não o vídeo.
(Confira os percentuais atuais do programa de afiliados que escolher; eles mudam por
categoria e por país.)

**Produto digital.** Você já escreveu, sem perceber que era um produto:

| Arquivo que já existe | Vira |
|---|---|
| `guias/como-virar-video-de-verdade.md` | o método |
| `guias/guia-obs-passo-a-passo.md` | o setup |
| `guias/guia-capcut-pc.html` | a edição |
| `guias/guia-de-upload.md` | a publicação |
| `guias/plano-de-postagem.md` | o cronograma |

Isso é um **curso de canal sem rosto (faceless)**, escrito, testado e em português. O
público existe e paga por isso. **É a receita que não depende do algoritmo, do RPM nem de
inscrito** — depende só de você empacotar o que já está no disco.

### 🥉 Rota 3 — Vender o sistema (a alavanca escondida, e a mais subestimada)

Olhe o que você construiu de fato: um **pipeline em Python que transforma um tema em um
mp4 1080×1920 animado, em inglês, com design validado** — com validador de layout, testes
de idioma por comparação, prova de render A/B, galeria automática.

**Isso é raro.** A maioria das pessoas que quer um canal sem rosto paga US$ 20–50 por vídeo
a editores humanos, ou assina ferramentas que fazem vídeo genérico.

Três modelos, do mais rápido ao maior:

1. **Serviço:** você produz N vídeos/mês para um criador ou empresa. Receita imediata,
   não depende de view nenhuma.
2. **Produto:** vende o pacote de vídeos prontos (ou o template) para quem quer um canal.
3. **Ferramenta:** transforma o pipeline num produto. É o maior, e o mais distante.

**Esta rota é a única em que o dinheiro entra antes do primeiro milhão de views.** Se o
objetivo é "ganhar dinheiro com esses vídeos", e não "construir um canal", é aqui que eu
olharia primeiro.

### 🔁 Rota 4 — Multiplicador: o mesmo arquivo, outras plataformas

Um vídeo vertical pronto para Shorts **já está pronto** para TikTok, Reels e Facebook. Zero
trabalho extra, e algumas dessas plataformas pagam mais por view:

| Plataforma | Por 1 milhão de views | Portão |
|---|---|---|
| YouTube Shorts | US$ 60 – 120 | 10 mi de views / 90 d |
| **Facebook Reels** | **US$ 300 – 5.000** | 5.000 seguidores **+ 600.000 min / 60 dias** |
| **TikTok Creator Rewards** | **US$ 400 – 1.000** | 10.000 seguidores **+ 100.000 views / 30 d** + vídeo **> 1 min** + país elegível |
| Snapchat Spotlight | US$ 100 – 300 | — |

⚠️ **O portão do Facebook é brutal:** 600.000 minutos em 60 dias são ~10.000 horas em dois
meses — mais que o **dobro** da exigência anual do YouTube. Não é a primeira jogada; é a
jogada de quem já tem tração.

✅ **O Brasil ESTÁ na lista** — checado em 26/09/2026. O Creator Rewards roda em
**8 países**: Estados Unidos, Reino Unido, Alemanha, França, Japão, Coreia do Sul,
**Brasil** e México (este entrou em 01/10/2025).

⚠️ **Mas o dinheiro depende de onde está o ESPECTADOR, não de onde você está.** Uma view
só conta como *qualified view* se **todas** valerem: vídeo **acima de 1 minuto**,
assistido **5 s ou mais**, entregue na **For You**, e vista **de um dos 8 países**.
View de audiência brasileira em canal brasileiro paga **US$ 0**.

> 🔑 **Isso não é um problema — é um argumento a favor do canal em inglês.** Este guia já
> manda não traduzir (o RPM cai 3 a 5×). A mesma decisão é o que faz a view valer no
> TikTok: canal EN mirando EUA/Reino Unido acerta o público que paga nas duas plataformas.

⚠️ **O portão do TikTok é maior do que "vídeo de 60 s".** Além de vídeo > 1 min, exige
**10.000 seguidores** e **100.000 views nos últimos 30 dias**, conta **pessoal** (não
Business) e 18+. É o segundo portão mais duro da tabela — atrás só do Facebook.

⚠️ **Não existe RPM fixo publicado.** A própria TikTok diz que a fórmula pesa
originalidade, tempo assistido, valor de busca e engajamento. Estimativas de terceiros
ficam em **US$ 0,40–1,00 por 1.000 views qualificadas** (≈ US$ 400–1.000 por milhão) —
sempre por view **qualificada**, nunca por view total. Planeje pelo painel do TikTok Studio.

> ✅ **Um corte de 60 s já existe** (feito em 26/09/2026):
> `beterraba/shorts-beet-garlic-en-1080x1920-60s.html` (+ `.mp4`, **67,5 s**). É o #19 com
> duas cenas de substância nova, não esticado — **este é o modelo** para levar os outros
> para o TikTok. Feito por `_criar-beet-garlic-60s.py`, que parte do arquivo validado.
> Os **67,5 s** importam: o TikTok exige vídeo **acima de** 1 minuto, então **não corte
> em 60,0 s cravados** — deixe margem (65–70 s), senão o vídeo pode não contar como
> qualificado.

**A parte grátis e certa:** publique em TikTok, Instagram Reels e Facebook desde o primeiro
dia, mesmo sem monetizar. É onde o Shorts pega alcance, e alcance é o que você não tem.

---

## 6. O que NÃO fazer

- **Não poste os 26 de uma vez.** Sua própria regra: o formato pode repetir, a substância
  não. 26 vídeos em uma semana é o retrato do "conteúdo em massa".
- **Não traduza para português.** Cai o RPM de 3 a 5 vezes. Canal BR é outro canal.
- **Não compre inscritos nem views.** Derrota a única coisa que importa (retenção) e é
  motivo de expulsão.
- **Não use música do CapCut.** Isso você já sabe e já está no guia. Vale repetir porque
  bloqueia o vídeo *inteiro*.
- **Não deixe o link de afiliado para depois.** É a única receita que não depende de
  escala, e os 26 vídeos já estão prontos para receber.

---

## 7. As próximas 2 semanas (concreto, em ordem)

**Semana 1 — destravar a distribuição**
1. **Escolher o nome** (opções na seção 8). É o bloqueio real de tudo.
2. Criar o canal, criar o AdSense, ativar 2FA.
3. Publicar o **#1 (Sauerkraut — o pilar)** e o **#2 (Couve — os dois truques)**.
4. Colocar o **link de afiliado** na descrição dos 26 (mesmo os ainda não publicados).

**Semana 2 — construir a máquina de horas assistidas**
5. **Renderizar o player 16:9 em mp4.** É software, não gravação — e é o que transforma o
   ativo parado em motor de 4.000 horas.
6. Escrever o **primeiro vídeo longo de compilação** (Kombucha: #23–#26), com substância
   nova, não colagem.
7. Continuar 2 Shorts por semana, sem falhar.

---

## 8. Nome do canal — 6 opções

Critério: tem que funcionar em inglês, ser dito em voz alta, e **não** parecer "canal de
receita genérico" (isso atrai o filtro de conteúdo em massa).

| Nome | Por quê |
|---|---|
| **2% Salt** | É a regra que aparece em **toda** receita da sua série (2% de sal por peso). Quem fermenta entende na hora; quem não entende, pergunta. Curto, técnico, memorável. |
| **Brine & Numbers** | A sua série é obcecada por números (pH 3–6, 6,76 g, 3 dias). O nome assume isso. |
| **The Ferment Window** | Vem do #26 — a janela de pH. Soa a ciência, não a receita. Puxa o canal para o nicho de educação, que paga mais. |
| **Ferment by the Numbers** | Explica o diferencial em 4 palavras. |
| **Salt, Water, Time** | Os três ingredientes. Calmo, limpo, fácil de lembrar. |
| **The Jar Tells You** | Vem do #26 ("o pote é o relógio"). Bom para marca, fraco para busca. |

**Minha recomendação: `2% Salt`.** É curto, é verdadeiro, é técnico e é a assinatura da
série inteira — e é a única da lista que um fermentador ouve e pensa "esse cara sabe".

⚠️ **Antes de decidir:** confira a disponibilidade do `@handle` no YouTube, do domínio, e
do nome no Instagram/TikTok. Nome bom com handle tomado não serve.

---

## 9. A expectativa honesta

| Fonte | Primeiro dinheiro | Depende de |
|---|---|---|
| Vender o sistema/serviço (Rota 3) | **semanas** | você prospectar |
| Produto digital (Rota 2) | **semanas a 2 meses** | empacotar e divulgar |
| Afiliado (Rota 2) | **1 a 3 meses** | ter view |
| AdSense YouTube (Rota 1) | **3 a 9 meses** | 4.000 horas |

**Não existe dinheiro rápido em AdSense de Shorts.** Existe um ativo real, que leva meses
para ligar e depois rende sozinho — e existem duas receitas que não dependem do algoritmo e
podem começar antes.

A pergunta que decide o resto é uma só: **você quer construir um canal (lento, escala
grande) ou vender o que você sabe fazer (rápido, escala menor)?**

---

## Fontes

- YouTube, blog oficial (12/08/2026) — definição de horas e views qualificadas:
  `blog.youtube/news-and-events/youtube-monetization-qualified-watch-hours-shorts-views/`
- YouTube (10/08/2026) — anúncio da mudança do YPP para 01/02/2027
- ShortSync (12/08/2026) — RPM de Shorts por nicho e por país, fórmula do Creator Pool
- FluxNote (26/06/2026) — RPM e elegibilidade do Facebook Content Monetization
- TikTok Newsroom — anúncio do Creator Rewards e requisitos oficiais (10.000
  seguidores, 100.000 views/30 d, vídeo acima de 1 minuto)
- quasa.io (26/07/2026) e monetizednow (18/09/2026) — lista dos 8 países e a regra de
  que a view só paga se vier de um país elegível

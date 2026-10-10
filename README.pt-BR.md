# YouTube · Fermentação sem rosto

> 🌐 **English?** Read [`README.md`](README.md) — that is the
> standard README for this repository. This file is the Portuguese version.

Canal de fermentação caseira **sem mostrar o rosto** — só as mãos.
Todo o vídeo é feito em HTML+SVG animado, gravado no OBS e montado no CapCut PC.

---

## Como o projeto funciona

```
roteiro  →  animação HTML+SVG  →  grava a tela (OBS)  →  monta (CapCut PC)  →  publica
```

**O produto não gera vídeo.** Ele gera os **arquivos animados** que você grava.
Sempre foi assim e não muda.

---

## Mapa das pastas

| Pasta | O que tem | Quando usar |
|---|---|---|
| `repolho/` | 5 arquivos — chucrute em várias versões **+ o short EN no formato de upload** | O legume nº1 da série. Comece por aqui. |
| `cenoura/` | 1 short | |
| `rabanete/` | 1 short | O mais rápido de todos (5 dias) |
| `couve-flor/` | 1 short | O do 2,5% de sal |
| `beterraba/` | 6 arquivos | A beterraba em várias versões (camadas, couve, melancia, svg puro) **+ o short beterraba+alho, mãos brancas** |
| `cebola/` | 1 short | Cebola + beterraba em camadas |
| `alho/` | 1 short (em inglês) | Alho no mel — o clímax, é o mais bonito |
| `pepino/` | 2 shorts | Pepino (o mais rápido da série) e pepino + maçã — nº 17 |
| `cores/` | 1 short | Os 3 que mudam de cor (alho + cebola + beterraba) — nº 14 |
| `brocolis/` | 1 short | Brócolis + laranja — nº 15. O único que precisa de salmoura |
| `kombucha/` | 3 shorts | Kombuchas de fruta — nº 23, 24 e 26 |
| `pao/` | 1 short | Fermento natural (sourdough) — nº 21. O primeiro pão |
| `mosquito/` | 1 short | Armadilha de mosquito caseira — nº 16. Trilha paralela, não é fermentação |
| `video-longo/` | **O vídeo de 12 minutos** — player + roteiro + pacote de publicação | O projeto principal de agora |
| `guia-geral/` | **O vídeo PILAR** — o short "os 5 mais fáceis" (nº 11) | É o que abre a série. Postar na semana 1 |
| `guias/` | Como gravar, como editar, legendas, descrições | Manual de operação |
| `aulas/` | Aulas de HTML/CSS | Aprender a mexer nos arquivos |
| `_base/` | Desenho técnico dos legumes (SVG) | Referência de desenho |
| `_arquivo/` | Coisas antigas / de outros assuntos **+ `_arquivo/backups/` com os `*.antes*` arquivados** | Não é da série atual |
| `_mp4/` | Ferramentas e notas do renderizador de MP4 | Mexer só se o `_gerar-mp4.js` precisar |
| `_teste-rec/` | Perfis do Chrome dos testes de gravação | **Ignorado pelo git** — lixo de teste |
| `capas-canva/` | Capas prontas feitas no Canva | Subir no YouTube |
| `_revisao/` | PNGs de conferência gerados pelo `_revisar-cenas.py` | Olhar antes de entregar |
| `galeria-shorts.html` | **Galeria de todos os 27 shorts** — abrir e clicar para ver cada um | E o indice visual da serie |
| `_gerar-galeria.py` | Gera a galeria | Rodar depois de criar/consertar um short |

---

## O que fica de fora do git

O repositório **não** versiona:

| O quê | Por quê |
|---|---|
| `*.mp4` (~288 MB) | São regeneráveis a partir do `.html` com o `_gerar-mp4.js`. |
| `_teste-rec/`, `_revisao/*.png`, `_revisao/_tmpprof/` | Perfis do Chrome e folhas de contato geradas. |
| `*.antes*` | Backups manuais — arquivados em `_arquivo/backups/`. |
| `.workbuddy-ai/` | Estado interno da ferramenta, não é do projeto. |

A lista completa está no [`.gitignore`](.gitignore).

---

## O que fazer primeiro (os 3 passos)

1. **Gravar o vídeo longo.** Abra `video-longo/player-video-longo-7-legumes.html`,
   aperte play, grave a tela no OBS em **1920×1080, MP4, 30 fps**.
   São ~6 minutos de animação. Não mexa em nada enquanto grava.

2. **Gravar os 7 clipes curtos no celular.** A lista exata está em
   `video-longo/roteiro-video-longo-7-legumes.md`, seção "O QUE GRAVAR NO CELULAR".
   É 15 s por legume, menos de 2 minutos no total.

3. **Montar e publicar.** Use `guias/guia-capcut-pc.html` para editar e o
   `video-longo/titulo-descricao-video-longo.md` para o título e a descrição.

**Plano completo — 7 semanas, vídeo por vídeo, com o arquivo exato a abrir:**
`guias/plano-de-postagem.md`

**Publicar no YouTube — campo por campo, com o que colar em cada um:**
`guias/guia-de-upload.md`

**Instalar e configurar o OBS do zero (se você nunca gravou a tela):**
`guias/guia-obs-passo-a-passo.md`

---

## Regras que não mudam

| Regra | Por quê |
|---|---|
| **Sal sempre sem iodo** | O iodo mata o fermento. O legume apodrece em vez de fermentar. |
| **Mofo colorido com pelo = joga tudo fora** | Não tem conversa. Bolha e cheiro azedo, ao contrário, são normais. |
| **Alho pode ficar azul ou verde** | Reação natural do enxofre. **Não é mofo.** Não jogue fora. |
| **Sem rosto no quadro** | É a identidade do canal. Mãos podem aparecer — as duas juntas, melhor ainda. |
| **Só áudio da biblioteca do YouTube** | A do CapCut costuma dar direito autoral. |
| **Texto em inglês** | O público-alvo é internacional. Capas, legendas e CTAs em inglês. |
| **CapCut no PC** | Windows + OBS + CapCut PC. (O "cap coil" de mensagens antigas era "CapCut".) |

---

## Antes de entregar qualquer arquivo animado

### 1. Validar (keyframes, ids, hex)

```bash
python _validar-short.py                 # valida TODOS os shorts do projeto
python _validar-short.py guia-geral/shorts-5-easiest-en.html   # ou um só
```

Sai `TOTAL DE PROBLEMAS: 0` quando está limpo. Ele checa:

| Checagem | Por que |
|---|---|
| `animations: N \| keyframes: M` | **Nunca confie num resultado vazio sem olhar as contagens** — duas listas vazias dão "0 erros", mas podem significar *nenhum keyframe existe* e o vídeo fica parado |
| `url(#x)` sem `id` | cada `<svg>` é um documento separado; não herda `<defs>` de outro |
| `@keyframes` nunca usado | lixo morto, vale limpar |
| hex corrompido | o gerador às vezes escreve `#8b8köln` |
| `svg id` ≠ `scenes[].id` | se não bater, a cena nunca aparece e a tela fica preta |
| **`transform=` + `animation` no mesmo tag** | 🔴 a animação **substitui** o atributo `transform` e o elemento **pula para a origem (0,0)**. Ver a seção abaixo |
| **`<text>` dentro de `<rect>`** | 🔴 o `<rect>` **não é contentor** no SVG — o texto **nunca é desenhado**. O cartão aparece vazio, sem erro nenhum |
| **`transform-origin` com palavra-chave** | 🔴 em SVG ele é resolvido contra o **viewBox** (405×720), não contra o desenho. Ver a seção abaixo |
| texto abaixo de `y=645` | fica escondido atrás da barra de legenda |

**Para consertar o bug do `transform=` em lote** — envolve cada `<g>` num `<g>` de fora
que carrega o `transform`, preservando os fins de linha e sem tocar no resto do arquivo:

```bash
python _consertar-transform.py            # dry-run: só mostra o que faria
python _consertar-transform.py --apply    # grava
```

### 2. OLHAR as cenas (o passo que os greps não fazem)

```bash
python _revisar-cenas.py guia-geral/shorts-5-easiest-en.html
python _revisar-cenas.py alho/shorts-garlic-honey-en.html --no-anim
```

Monta uma folha de contato com todas as cenas em tamanho nativo e renderiza em PNG
(Chrome headless) em `_revisao/`. A faixa da legenda aparece **marcada em vermelho**
para você ver se algo entrou ali.

| Flag | O que faz | Quando usar |
|---|---|---|
| `--final` | prende cada animação no **estado final** | ✅ **é o modo para revisar layout** |
| `--no-anim` | remove as animações (estilo base) | só para provar o bug do `transform=` |
| `--cols N` | N cenas por linha | ver as 8 cenas de uma vez (`--cols 8`) |

> ⚠️ **Sem `--final` a folha sai em t=0** e todo elemento com `animation-fill-mode: both`
> aparece **invisível** — parece que o texto sumiu, mas é só o primeiro quadro.
> O `--virtual-time-budget` **não** avança a timeline de animação CSS no `--headless=new`;
> quem resolve é o `--final` (injetar `animation-delay:-1s` + `animation-play-state:paused`).

Para conferir o **quadro real 1080×1920** (com a barra de legenda em HTML por cima):

```bash
python _captura-upload.py beterraba/shorts-beet-garlic-en-1080x1920.html --cenas 0,6
```

> **Layout não se vê com grep.** Foi assim que apareceu o bug do `transform=`:
> o repolho do `shorts-chucrute-30s.html` está desenhado **fora do quadro**, no canto
> superior esquerdo, e nenhuma das checagens antigas acusava.

### 🔴 O bug do `transform=` (achado em 12 dos 13 shorts)

```html
<!-- ERRADO: a animação apaga o translate(202,372) -->
<g transform="translate(202,372)" style="animation:floatUpDown 3.4s infinite"> … </g>

<!-- CERTO: o transform fica no <g> de fora, a animação no de dentro -->
<g transform="translate(202,372)">
  <g style="animation:floatUpDown 3.4s infinite"> … </g>
</g>
```

Em SVG o `transform` é um **atributo de apresentação** — a declaração CSS (incluindo a
que vem de uma animação) **ganha** dele. Então todo elemento com `transform="…"` **e**
uma animação que mexe em `transform` é desenhado na **origem do SVG**, não onde você
posicionou. Sintoma: o assunto principal some do centro e aparece um pedaço dele
cortado no canto superior esquerdo.

**Como conferir:** `python _revisar-cenas.py <arquivo>` e depois
`python _revisar-cenas.py <arquivo> --no-anim`. Se as duas imagens forem diferentes,
é este bug.

---

## Estado atual

**Série de legumes:** 7 legumes, 50 cenas de animação prontas.
**Vídeo longo:** roteiro, player 16:9 e pacote de publicação prontos.
**Versão acelerada 30s:** pronta em `repolho/shorts-chucrute-30s.html`.
**Capas em inglês:** 8 capas 1080×1920 em `capas-canva/_english/` (ver abaixo).
**Vídeo pilar (nº 11):** ✅ pronto em `guia-geral/shorts-5-easiest-en.html` —
os 11 vídeos do pacote estão cobertos.
**Short do chucrute no formato de upload:** ✅ pronto em
`repolho/shorts-sauerkraut-en-1080x1920.html` (1080×1920, 8 cenas, 52 s, em inglês).
**Short novo — beterraba + alho, mãos brancas:** ✅ pronto em
`beterraba/shorts-beet-garlic-en-1080x1920.html` (1080×1920, 8 cenas, 54 s, em inglês,
**tempo em SEMANAS**).

**Galeria de todos os shorts:** ✅ `galeria-shorts.html` na raiz — lista os
**23 shorts animados** (19:18 de animacao no total) com duracao, idioma, formato e
marcacao de bug. Regenerar com `python _gerar-galeria.py`.

**Bug do `transform=`:** ✅ **corrigido em 15/09** — 69 elementos em 11 arquivos (ver abaixo).
**Cartões invisíveis do `alho` e da `cebola`:** ✅ **corrigido em 15/09** — 6 cartões + ~25 linhas que caíam atrás da barra de legenda.
**Falta fazer:** gravar, editar e publicar.

### 📐 Formato de gravação — decisão nova

Os shorts antigos são cartões de **405 × 720** (com canto arredondado e fundo escuro),
feitos para **olhar na tela**. Gravar isso e subir no YouTube obriga o YouTube a
esticar a imagem e ainda leva a borda junto.

**Já existem 3 arquivos nesse formato** — o vídeo pilar
(`guia-geral/shorts-5-easiest-en.html`), o short do chucrute
(`repolho/shorts-sauerkraut-en-1080x1920.html`) e o short novo de beterraba+alho
(`beterraba/shorts-beet-garlic-en-1080x1920.html`). São **1080 × 1920 nativo, sem borda**,
e o desenho continua em coordenadas 405 × 720 — como é vetorial, ele é desenhado
direto em 1080 × 1920 sem esticar nada. O arquivo se ajusta sozinho: em tela pequena ele
**encolhe só para você olhar**; numa Fonte de Navegador do OBS em 1080 × 1920 ele
sai **pixel por pixel**.

**Como gravar nesse formato:** `guia-geral/como-gravar-e-publicar.md` (Fonte de
Navegador do OBS, 1080 × 1920, com `?rec` na URL) — é o mesmo procedimento para os
dois arquivos. O do chucrute também tem `repolho/como-gravar-sauerkraut.md` com a
URL pronta.

> Os outros shorts continuam em 405 × 720. Se quiser, dá para converter todos para o
> mesmo formato de upload — a mudança é só no `#stage` e nos tamanhos do texto de
> sobreposição; o desenho em si não muda.

### ✅ Bug do `transform=` — CORRIGIDO em 15/09

`_validar-short.py` encontrou **11 shorts** com elementos posicionados com `transform=`
**e** animação no mesmo tag — o que fazia o elemento ser desenhado no **canto superior
esquerdo** em vez do lugar certo. O caso mais grave era
`repolho/shorts-chucrute-30s.html`, onde **o repolho saía do quadro**.

**Correção:** `_consertar-transform.py --apply` envolveu **69 elementos** em 11 arquivos
(`alho`, `beterraba-camadas`, `beterraba-couve`, `beterraba-melancia`,
`beterraba-svg-puro`, `cebola`, `couve-flor`, `rabanete`, `shorts-chucrute-30s`,
`shorts-repolho-maos-canva`, `player-video-longo-7-legumes`). O validador agora dá
**0** para esse bug e as cenas foram **olhadas** uma por uma com `_revisar-cenas.py` —
o repolho voltou para o centro do quadro.

Backup de antes da correção: `../youtube-work-backup-20260915-2133`.

**Junto foi corrigido:** `repolho/shorts-repolho-maos-canva.html` tinha o CTA final
(o "Qual eu fermento depois desse?") dentro de um `<rect>` — **nunca aparecia**: virava
uma pílula vazia. Também subiram os cartões que caíam atrás da barra de legenda nesse
arquivo e no `beterraba/shorts-beterraba-couve.html`.
### ✅ `alho/` e `cebola/` — CORRIGIDOS em 15/09

Eram os dois últimos arquivos com **texto invisível**: 6 cartões tinham o texto dentro de
um `<rect>` (que no SVG **não é contentor**) e o cartão saía como uma **pílula vazia**.
Além disso, ~25 linhas de texto caíam **atrás da barra de legenda** (`y > 645`).

| O quê | Como |
|---|---|
| 6 cartões com `<text>` dentro de `<rect>` | viraram `<g>` com `<rect/>` + `<text/>` |
| ~25 linhas sob a barra de legenda | subiram para o bloco seguro (`y ≤ 638`) |
| cartões com a borda cortada | encurtaram e subiram (cartão `y=556 h=76`, texto em 584 / 613) |
| conteúdo que precisava de espaço | subiu junto: jarro do mel (30), pote giratório (30), jarro da cebola (24), pote final da cebola (26) |
| ponteiros do relógio | `transform-origin:center` → `0 0` |
| pote de mel do `alho` | ganhou `transform-origin` no próprio centro — antes girava em volta da origem do SVG e **voava para o topo do quadro** |

Script: `_consertar-cards.py` (dry-run por padrão; `--apply` grava). Os dois arquivos agora
dão **0 problemas** no `_validar-short.py` e as 16 cenas foram **olhadas** com
`_revisar-cenas.py --final`.

Backup de antes: `../youtube-work-backup-20260915-2157`.


### ⚠️ O que ainda falta consertar

| Onde | O quê |
|---|---|
| **11 arquivos** | 🔴 `transform-origin` com palavra-chave (`center`, `center top`, `center bottom`, `left`) — o pivô cai no viewBox e a faca / a mão / o ponteiro gira em volta do lugar errado. Ver a seção abaixo |
| vários | `@keyframes` nunca usados — lixo morto, inofensivo |

> ✅ `alho/` e `cebola/` **foram consertados em 15/09** (ver abaixo).

> O aviso em `video-longo/player-video-longo-7-legumes.html` **é falso positivo**: é um
> player 16:9 e o quadro 405×720 aparece inteiro dentro do mockup, sem barra de legenda
> por cima. O `_validar-short.py` assume o cartão de 405×720.
### 🔴 O bug do `transform-origin` em SVG (achado em 15/09)

Em SVG o `transform-origin` **não** é resolvido contra a caixa do próprio elemento —
é resolvido contra o **viewBox** (aqui, 405 × 720):

| Escrito | Vira (coordenadas locais) | Serve? |
|---|---|---|
| *(nada — o padrão)* | `0 0`, a origem do próprio elemento | ✅ **certo** |
| `transform-origin:0 0` | `0 0` | ✅ certo |
| `transform-origin:202px 176px` | `202, 176` | ✅ certo, se for isso que você quer |
| `transform-box:fill-box; transform-origin:50% 50%` | centro do **próprio** desenho | ✅ certo |
| `transform-origin:center` | `202.5, 360` | ❌ pivô **longe do desenho** |
| `transform-origin:center top` | `202.5, 0` | ❌ |
| `transform-origin:center bottom` | `202.5, 720` | ❌ |
| `transform-origin:left` | `0, 360` | ❌ |

Sintoma: a faca **gira em volta de um ponto fora do quadro** em vez de cortar no lugar,
o ponteiro do relógio **sai do mostrador**, a mão da massagem **escala para longe**.
O bug só aparece quando o keyframe tem `rotate` ou `scale` — por isso o validador só
acusa nesse caso.

**Conserto:** trocar a palavra-chave por `0 0`. O pivô passa a ser a origem local do
elemento, que é onde o desenho foi construído.

⚠️ **Ainda não corrigido — 11 arquivos** (mais o player do vídeo longo, que é caso à parte):
`beterraba-animado`, `beterraba-camadas`, `beterraba-couve`, `beterraba-melancia`,
`beterraba-svg-puro`, `cenoura`, `couve-flor`, `pepino`, `rabanete`,
`repolho-animado`, `repolho-maos-canva`, `sauerkraut-en-1080x1920`.


---

## 🌍 PÚBLICO INTERNACIONAL — o canal é em INGLÊS

Decisão do usuário: **o público-alvo é internacional** (o Brasil responde pouco a
conteúdo de fermentação). Então tudo que é texto vai em inglês.

### Material em inglês

| Arquivo | O que é |
|---|---|
| `capas-canva/_english/` | **8 capas 1080×1920 em inglês** — prontas para o YouTube |
| `guias/textos-de-tela-capcut-en.md` | Textos para sobrepor no CapCut (gancho/meio/fecho) |
| `guias/pacote-legendas-descricoes-en.md` | Títulos, descrições e hashtags dos **15 vídeos** (14 Shorts + 1 vídeo longo) |
| `alho/shorts-garlic-honey-en.html` | O short do alho — já era em inglês |

### Nomes em inglês (usar SEMPRE estes)

| Português | Inglês |
|---|---|
| Repolho | **CABBAGE** |
| Cenoura | **CARROTS** |
| Rabanete | **RADISHES** |
| Couve-flor | **CAULIFLOWER** |
| Beterraba | **BEETROOT** |
| Cebola (roxa) | **RED ONION** / ONION + BEET |
| Alho no mel | **GARLIC HONEY** |
| Chucrute | **SAUERKRAUT** |
| Pepino | **CUCUMBER** |

### Como as capas em inglês foram feitas

As capas do Canva tinham o **texto em português queimado no PNG** — não dá para apagar.
A solução foi **inpainting com OpenCV**: o programa acha os pixels do texto pela cor,
apaga e **reconstrói o fundo por trás**. Depois um rodapé escuro recebe o texto em inglês.

```
_limpar-texto.py    OpenCV inpaint → arte limpa, sem nenhum texto
_traduzir-capas.py  monta o rodapé com o texto em inglês
```

**Se precisar refazer ou traduzir outra capa:** os dois scripts estão em `capas-canva/`.
Rodar `_limpar-texto.py` e depois `_traduzir-capas.py`.
Requer `opencv-python-headless` + `numpy` no venv do projeto.

> **Cota do Canva:** estava esgotada quando as capas foram feitas (por isso a montagem
> local). Quando renovar, os designs originais continuam editáveis na conta.


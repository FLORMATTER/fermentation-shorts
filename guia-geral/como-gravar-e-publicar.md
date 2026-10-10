# Guia-geral — como gravar e publicar o vídeo pilar

Arquivo de animação: **`guia-geral/shorts-5-easiest-en.html`**
Formato: **1080 × 1920 (9:16)** · 8 cenas · **49 s** · texto em inglês

> Este é o **vídeo pilar** — o nº 11 do pacote, o de maior retenção.
> O plano de postagem coloca ele na **semana 1** junto com o rabanete.
> Título, descrição e hashtags também estão em `guias/pacote-legendas-descricoes-en.md` (§11).

---

## 🔴 A diferença deste arquivo: ele já está no formato de upload

Os outros shorts do projeto são cartões de **405 × 720** com cantos arredondados e
fundo escuro em volta — foi desenhado para **olhar na tela**, não para gravar.
Se você gravar aquilo, o vídeo sai pequeno e com borda.

Este aqui foi feito para **virar o vídeo final direto**:

| | |
|---|---|
| Tamanho | **1080 × 1920** nativo — a resolução que o YouTube pede |
| Borda | zero — o desenho vai até a borda dos 4 lados |
| Escala | o arquivo se ajusta sozinho: em tela pequena ele **encolhe só para você olhar** |
| Controles | os botões ◀ ⏸ ▶ **somem sozinhos** depois de 2 s parados — não aparecem na gravação |

**Por que 405 × 720 não servia:** gravar aquilo e subir no YouTube obriga o YouTube a
esticar a imagem (perde nitidez) e ainda leva os cantos arredondados junto. Aqui o
desenho é vetorial: os 405 × 720 de coordenadas são desenhados direto em 1080 × 1920,
sem esticar nada e sem perder nitidez.

---

## ✅ O jeito certo de gravar: Fonte de Navegador (Browser Source)

Gravar "captura de tela" num monitor deitado (1920 × 1080) **não funciona** para
vídeo vertical — o desenho vertical não cabe na tela. A solução é o OBS desenhar a
página **fora da tela**, no tamanho certo. É o caminho mais limpo: sem crop, sem zoom,
sem perda.

### Passo a passo no OBS

1. Abra o OBS
2. Em **Cenas**, crie uma cena nova (ex.: `short-pilar`)
3. Em **Fontes**, clique no **+** → **Navegador** (Browser)
4. Dê um nome (ex.: `anim`) → **OK**
5. Preencha:
   - **URL:** o caminho do arquivo. Use barras normais e comece com `file:///`:
     ```
     file:///C:/Users/Saxa/Desktop/youtube-work/guia-geral/shorts-5-easiest-en.html?rec
     ```
   - **Largura:** `1080`
   - **Altura:** `1920`
   - Marque **Desligar a fonte quando não estiver visível** (economiza CPU)
6. **OK**

O `?rec` no fim da URL faz a animação **começar sozinha**, **esconde a capa** e
**esconde os botões de play** — que senão apareceriam no vídeo. Sem ele, você teria que
clicar no ▶ dentro da fonte, e isso exige *botão direito na fonte → Interagir*.

> `?play` também inicia sozinho (1,5 s depois de carregar), mas **não esconde a capa**.
> Para gravar, use sempre `?rec`.

### Configurações → Vídeo

| Campo | Valor |
|---|---|
| Resolução da base (canvas) | **1080 × 1920** |
| Resolução de saída (escalada) | **1080 × 1920** |
| FPS | **30** |

Depois, na pré-visualização, **arraste a fonte até encher o quadro** (ela deve encaixar
exatamente, sem sobra).

### Gravar

1. Aperte **Iniciar Gravação**
2. **Espere 3 segundos** parado
3. Clique com o **botão direito na fonte → Atualizar** (ou aperte a tecla de atalho
   que você configurou) para a animação começar do zero
4. **Não mexa em nada** — 49 segundos
5. Quando terminar, **espere 3 segundos**
6. **Parar Gravação**

> O arquivo sai em `1080 × 1920`, MP4, pronto. Sem crop, sem zoom, sem esticar.

---

## 🎬 Textos para o CapCut (opcional)

O arquivo já traz título, cartões e a legenda na tela — **não precisa** sobrepor texto.
Se quiser reforçar o gancho, use só isto, nos 2 primeiros segundos:

```
THE 5 EASIEST
TO FERMENT
```

E no fim, se quiser fixar:

```
SAVE THIS 📌
```

Regra do projeto: **máximo 6 palavras por tela**, fundo escuro + texto branco,
nunca em cima do desenho principal.

---

## 📋 Copiar e colar no YouTube

### Título (recomendado — 47 caracteres)

```
The 5 easiest vegetables to ferment (full chart)
```

Alternativas:
- `5 vegetables you can ferment with just salt`
- `Start fermenting with one of these 5`
- `The 5 easiest ferments for beginners`

### Descrição

```
If you want to start fermenting, start with one of these 5.

FULL CHART

Red cabbage ....... 2% salt ....... 7 days
Beetroot .......... 2% salt ....... 9 days
Carrots ........... 2% salt ....... 6 days
Radish ............ 2% salt ....... 6 days
Cucumber .......... 3% brine ...... 5 days

THE 4 RULES THAT APPLY TO ALL
1. Cut thin — the thinner, the faster
2. Weigh the salt — 2% of the vegetable's weight (cucumber is 3%)
3. Massage until it releases water
4. Press everything down so it stays SUBMERGED

HOW TO KNOW IT'S GOING RIGHT
✅ Bubbles rising = it's working
✅ Sour, pickle-like smell = normal
✅ Cloudy water = normal
❌ Colored mold (green, black, orange) = throw it out
❌ Rotten smell = throw it out

Use non-iodized salt. Iodine kills the ferment.

#fermentation #fermentedfoods #pickles
```

### Hashtags

```
#fermentation #fermentedfoods #pickles #guthealth #healthyeating
```

### Comentário fixado

```
Which one are you trying first? 👇
```

---

## ⚠️ Antes de postar — conferência de 5 segundos

- [ ] O vídeo está **vertical (9:16)** e em **1080 × 1920**?
- [ ] O **gancho** aparece nos 2 primeiros segundos?
- [ ] A música é da **biblioteca do YouTube** (nada do CapCut)?
- [ ] O título tem **menos de 60 caracteres**?
- [ ] Tem **hashtags** na descrição?

Tudo ✔️? Pode postar.

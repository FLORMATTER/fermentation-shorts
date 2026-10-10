# Guia do OBS — do zero até o primeiro `.mp4`

Você escolheu gravar no **PC com OBS**. Este é o caminho completo: do download até
o arquivo de vídeo na sua mão. Se você nunca abriu o OBS na vida, comece aqui.

**No fim você vai ter:** um `.mp4` de **1080 × 1920**, ~50 segundos, sem borda,
sem botão de play e sem som de fundo — pronto para subir no YouTube.

| Etapa | Quanto leva |
|---|---|
| Instalar | 5 minutos |
| Configurar (uma vez só, nunca mais) | 5 minutos |
| Gravar cada vídeo | 2 minutos |

---

# PARTE 1 — Instalar

1. Abra o Chrome e vá em **obsproject.com**
2. Clique no botão **Windows** — o instalador começa a baixar
3. Abra o arquivo baixado (vai estar em **Downloads**)
4. Clique em **Avançar** até o fim. Pode aceitar tudo como vem
5. Abra o **OBS Studio**

## ⚠️ Na primeira vez ele abre um assistente — CANCELAR

O OBS abre sozinho uma janela chamada **"Assistente de configuração automática"**
(ou "Auto-Configuration Wizard").

**Clique em Cancelar.**

Ele configuraria tudo para **tela deitada** — exatamente o oposto do que você
precisa. Vamos configurar na mão, e são só dois lugares.

---

# PARTE 2 — Configurar (uma vez só)

Clique em **Configurações** no canto **inferior direito**.

## 2.1 — Vídeo: o formato vertical

Clique em **Vídeo** na lista da esquerda.

| Campo | O que colocar |
|---|---|
| **Resolução da base (Canvas)** | `1080x1920` |
| **Resolução da saída (escalonada)** | `1080x1920` |
| Filtro de redução de escala | deixe como está |
| **Valor de FPS comum** | **30** |

### ⚠️ A caixa aceita texto — e é isso que você vai usar

Clique dentro da caixa **Resolução da base**, **apague o que está lá** e digite:

```
1080x1920
```

- `x` minúsculo, **sem espaço**, **sem vírgula**, sem o símbolo `×`
- **Não escolha da lista** — nenhuma opção da lista é vertical

Faça o mesmo na **Resolução da saída**.

**Como saber que deu certo:** clique em **Aplicar**. A pré-visualização do OBS
(no meio da tela) vira um retângulo **em pé**, estreito e alto.

Se continuar deitado, o valor não entrou — repita.

## 2.2 — Saída: o arquivo `.mp4`

Ainda em Configurações, clique em **Saída**.

- **Modo de saída:** **Simples**
- Aba **Gravação**:

| Campo | O que colocar |
|---|---|
| Qualidade da gravação | **Alta qualidade, tamanho de arquivo médio** |
| Formato de gravação | **MP4** |
| Caminho de gravação | clique em **Procurar** → escolha a pasta **Vídeos** |

> **Se aparecer a opção "MP4 fragmentado", escolha ela.** É mp4 igual, mas se o OBS
> travar no meio o arquivo não se perde. Se não aparecer, **MP4** normal resolve —
> são clipes de 50 segundos.

📌 **Anote o caminho que aparecer na caixa.** É ali que o vídeo vai nascer. Você vai
precisar dele depois.

Clique em **OK** para fechar as Configurações.

## 2.3 — Áudio: desligar o microfone 🔇

Olhe na **parte de baixo** da tela do OBS. Tem um **Mixer de áudio** com uma barra
chamada **Mic/Aux**.

**Clique no ícone de alto-falante** dessa barra para **silenciar** (o ícone fica
riscado).

⚠️ **Isso é mais importante do que parece.** A animação **não tem som**. Se o
microfone ficar ligado, o OBS grava o barulho do seu ambiente por cima do vídeo —
ventilador, cachorro, teclado, a rua. E não dá para tirar depois sem estragar a
imagem. A música entra **depois**, na hora de publicar.

---

# PARTE 3 — Montar a cena

Isto você faz **uma vez**. Depois é só trocar a URL para gravar outro vídeo.

## 3.1 — Criar a cena

1. No canto **inferior esquerdo**, na caixa **Cenas** → clique no **+**
2. Digite o nome `short` → **OK**

## 3.2 — Criar a fonte

1. Ao lado, na caixa **Fontes** → clique no **+**
2. Escolha **Navegador** (Browser)
3. Dê o nome `anim` → **OK**

## 3.3 — Preencher

| Campo | O que colocar |
|---|---|
| **URL** | o caminho do arquivo **com `?rec` no fim** |
| **Largura** | `1080` |
| **Altura** | `1920` |
| **FPS** | `30` |
| Caixas de baixo | deixe como estão |

A URL é assim — começa com `file:///` e termina com `?rec`:

```
file:///C:/Users/Saxa/Desktop/youtube-work/guia-geral/shorts-5-easiest-en.html?rec
```

Clique em **OK**.

## 3.4 — Se o desenho não encher o quadro

Clique com o **botão direito** na fonte `anim` → **Transformar** → **Ajustar à tela**.

(Atalho: clique na fonte e aperte **Ctrl + F**.)

## ⚠️ As duas coisas que fazem o vídeo dar errado

| ❌ Errado | ✅ Certo | Por quê |
|---|---|---|
| Fonte **"Captura de tela"** | Fonte **"Navegador"** | Captura de tela grava o **monitor inteiro**. Num monitor deitado, o Short vertical sai **deitado e com barras preta dos lados** |
| URL **sem `?rec`** | URL **com `?rec`** | Sem ele, a **capa** e os **botões de play** aparecem dentro do vídeo |

Esses dois são a causa de quase todo vídeo estragado. Confira antes de gravar.

---

# PARTE 4 — O primeiro teste

> **O primeiro vídeo é treino. Não publique ele.**
> Você ainda não escolheu o nome do canal, então ele vai sair com `@yourchannel`
> escrito no canto. Grave, olhe, apague e vá para o de verdade.

1. Aperte **Iniciar gravação** (canto inferior direito)
2. **Conte até 3** sem mexer em nada
3. Clique com o **botão direito** na fonte `anim` → **Atualizar**
   → a animação **recomeça do zero**
4. **Não encoste no mouse.** Deixe rodar até o fim (~50 segundos)
5. **Conte até 3** de novo
6. Aperte **Parar gravação**

### Onde o arquivo foi parar

Na pasta que você escolheu no **2.2** (Vídeos). O nome é a data e a hora, tipo
`2026-09-17 22-10-33.mp4`.

## 💡 Dica: um atalho para gravar

Configurações → **Atalhos** → procure **"Iniciar gravação"** → clique na caixa ao
lado e aperte uma tecla (ex.: **F9**). Faça o mesmo em **"Parar gravação"** com
outra tecla. Aí você grava sem tirar o mouse do lugar.

---

# PARTE 5 — Conferir se deu certo

Abra o arquivo `.mp4` e confira os 5 pontos:

- [ ] Está **vertical** (em pé) e preenche a tela inteira — **sem** barras preta dos lados
- [ ] **Sem** borda e **sem** canto arredondado
- [ ] **Sem** botão de play aparecendo
- [ ] **Silêncio total** — nenhum barulho do ambiente
- [ ] Duração perto de **50 segundos**

**Passou nos 5?** Você acabou de gravar seu primeiro vídeo. Pode apagar esse teste
e partir para os de verdade — o processo é idêntico, só troca a URL.

---

# PARTE 6 — Problemas comuns

| O que você vê | Causa | Solução |
|---|---|---|
| Vídeo **deitado**, com barras preta dos lados | O canvas continua em 1920x1080 | Configurações → Vídeo → digitar `1080x1920` nos **dois** campos e **Aplicar** |
| Tela **preta**, não aparece nada | A fonte está em outra cena, ou o olhinho está fechado | Clique na cena certa; clique no **olho** ao lado da fonte |
| Aparece a **capa** e o **botão de play** | Faltou `?rec` na URL | Botão direito na fonte → Propriedades → acrescente `?rec` no fim |
| Tem **som de fundo** | Microfone ligado | Silencie o **Mic/Aux** no Mixer de áudio |
| O desenho sai **pequeno no meio** | A fonte não foi ajustada | Botão direito → Transformar → **Ajustar à tela** |
| O arquivo **não abre** em lugar nenhum | Gravou em `.mkv` | No OBS: **Arquivo → Remuxar gravações** → escolha o `.mp4` |
| O PC **engasga** ou o vídeo trava | Codificador pesado | Configurações → Saída → troque o **Codificador** para `x264` |
| A imagem está **borrada** | A URL não tinha `?rec` | Sem `?rec` o desenho sai pequeno e esticado. Use `?rec` |

---

# PARTE 7 — Depois do primeiro teste

## Sobre o `@yourchannel`

Nos testes o vídeo vai mostrar **`@yourchannel`** no canto superior. **Não publique
esses** — são treino.

> **Isto vale só para o caminho do OBS.** Os 20 shorts que já têm `.mp4` renderizado
> saem **sem** marca d'água — o motor omite o placeholder sozinho. Gravar pelo OBS
> só é necessário no **vídeo longo (#13)**.

Quando você decidir o nome do canal, eu troco o `@` nos **50 arquivos** de uma vez:

```bash
python _trocar-handle.py @seunome --apply
```

Se preferir, também posso **remover o `@` de todos** e você grava sem marca nenhuma.

## Os outros arquivos

| Para quê | Arquivo |
|---|---|
| Qual vídeo gravar em cada dia, e com qual título | `guias/plano-de-postagem.md` |
| Subir no YouTube, campo por campo | `guias/guia-de-upload.md` |
| Editar e exportar no PC | `guias/guia-capcut-pc.html` |
| Esconder notificação, cortar as pontas, gravar pelo celular | `guias/como-virar-video-de-verdade.md` |

## Para o teste, use este arquivo

```
file:///C:/Users/Saxa/Desktop/youtube-work/guia-geral/shorts-5-easiest-en.html?rec
```

É o vídeo pilar — o mais importante do canal, e o primeiro da semana 1 do plano.

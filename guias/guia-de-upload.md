# Guia de upload — do arquivo ao vídeo publicado

Você quer fazer upload. Só que **upload é o último de três passos** — e hoje nenhum
dos dois primeiros está pronto. Não existe nenhum `.mp4` na pasta: ainda não houve
gravação.

| Porta | O que é | Estado hoje |
|---|---|---|
| **1** | Criar o canal no YouTube | ❌ falta (o nome ainda não foi escolhido) |
| **2** | Gravar o `.mp4` | ❌ falta |
| **3** | Subir no YouTube | ⬅️ **é o que você quer fazer** |

As três seções abaixo estão na ordem. Não pule a 1 e a 2 — sem elas a 3 não tem o
que enviar.

---

# PORTA 1 — Criar o canal

Uma vez só. Leva uns 10 minutos.

1. Abra o Chrome e vá em **youtube.com**
2. Clique em **Fazer login** (canto superior direito) e entre com sua conta Google
3. Clique na sua **foto** (ou na sua inicial) no canto superior direito
4. Clique em **Criar um canal**
5. Vai pedir duas coisas:

| Campo | O que é | Onde aparece |
|---|---|---|
| **Nome** | o nome do canal | embaixo de cada vídeo, na página do canal |
| **@handle** | o `@algumacoisa` | é a marca d'água dos shorts — que **não** sai no `.mp4` pronto (ver `plano-de-postagem.md`) |

6. Clique em **Criar canal**

### ⚠️ Você ainda não escolheu o nome

Duas saídas:

- **Esperar** e criar o canal só quando decidir — mais limpo, mas segura a gravação.
- **Criar agora com um nome provisório** e trocar depois. Dá para trocar:
  o **nome** do canal você muda quando quiser; o **@handle** pode ser trocado
  **3 vezes a cada 14 dias**. Se for por aqui, escolha um handle que você não se
  importe de manter — é melhor ter um "ok" hoje do que o "perfeito" em duas semanas.

**Se você criar o canal, me diga o @handle** que eu troco nos **50 arquivos** de uma
vez (hoje eles mostram `@yourchannel` / `@seucanal` / `@yourhandle`).

⚠️ **Isto não trava a publicação.** Para os Shorts, o `.mp4` já pronto sai **sem**
marca d'água. O handle só precisa estar certo se você for **gravar pelo OBS**.

---

# PORTA 2 — Gravar o `.mp4`

Esta é a parte que dá mais trabalho e a que mais gente erra. As duas guias que
existem já cobrem isso:

| Para quê | Arquivo |
|---|---|
| **Instalar e configurar o OBS do zero** (você não tem OBS ainda) | `guias/guia-obs-passo-a-passo.md` |
| O passo a passo da gravação (OBS, cortes, celular) | `guias/como-virar-video-de-verdade.md` |
| O passo a passo da Fonte de Navegador, botão por botão | `guia-geral/como-gravar-e-publicar.md` |
| A ordem e qual arquivo abrir em cada dia | `guias/plano-de-postagem.md` |

## O resumo do resumo

1. No OBS: **Fontes → + → Navegador** (Browser). **Não** use "Captura de tela".
2. **Largura 1080 · Altura 1920**
3. Na URL, cole o caminho do arquivo **com `?rec` no fim**:
   ```
   file:///C:/Users/Saxa/Desktop/youtube-work/guia-geral/shorts-5-easiest-en.html?rec
   ```
4. **Configurações → Vídeo:** base e saída em **1080 × 1920**, **30 fps**
5. Gravar → esperar 3 s → botão direito na fonte → **Atualizar** → esperar 3 s → Parar

⚠️ **O `?rec` é o que faz a diferença.** Sem ele, o arquivo abre com a capa e com os
botões de play — e os botões aparecem no vídeo. Com ele, a capa e os botões somem, o
desenho preenche os 1080 × 1920 (vetorial, sem borrar) e a animação começa sozinha.

## Você não tem OBS instalado

Não achei o OBS na sua máquina. Tem duas opções:

- **Instalar o OBS** (grátis, `obsproject.com`) — é o caminho que dá o melhor resultado
  e o que as guias descrevem.
- **Xbox Game Bar** — já vem no Windows, não instala nada. Aperte **Windows + G**.
  Funciona, mas é mais instável e às vezes não grava o navegador. Se falhar, volte
  para o OBS.

---

# PORTA 3 — Subir no YouTube (computador) ⭐

É o caminho mais fácil de acertar. A interface do seu YouTube provavelmente está em
português — os nomes abaixo são os que você vai ver.

## Passo 1 — Abrir o YouTube Studio

No Chrome, vá em:

```
studio.youtube.com
```

É diferente do `youtube.com` normal. É a tela de quem publica.

## Passo 2 — Mandar o arquivo

1. Clique em **CRIAR** (canto superior direito, um círculo com **+**)
2. Escolha **Enviar vídeos**
3. **Arraste o `.mp4`** para dentro da janela (ou clique em **Selecionar arquivos**)

O upload começa na hora. Enquanto ele sobe, você preenche o resto — não precisa esperar.

## Passo 3 — Preencher os campos

O painel da direita é onde tudo vai. **Não invente nada**: o texto já está escrito
em `guias/pacote-legendas-descricoes-en.md`.

| Campo | De onde vem | Cuidado |
|---|---|---|
| **Título** | a entrada do vídeo no pacote | máximo **60 caracteres**; nunca repita título |
| **Descrição** | a mesma entrada | as **hashtags já estão no fim** — copie junto |
| **Miniatura** | opcional | no Short quase não aparece; pode deixar sem |
| **Playlists** | opcional | crie uma chamada `Fermentation` e junte os vídeos |
| **Público** | marque **"Não, não é conteúdo para crianças"** | obrigatório responder |
| **Tags** | em **Mostrar mais → Tags** | opcional: cole as hashtags **sem o `#`**, separadas por vírgula |

### Como copiar do pacote sem errar

Abra `guias/pacote-legendas-descricoes-en.md` no Bloco de Notas ou no VS Code. Cada
vídeo tem um número (`# 1. SAUERKRAUT`, `# 7. RADISH`…). Copie **o bloco que está
dentro das três crases** — é exatamente o texto do título e da descrição.

Qual entrada é qual vídeo? A tabela **"🗂️ WHICH FILE TO RECORD"** no fim do pacote diz.

## Passo 4 — Avançar

Clique em **AVANÇAR** no canto inferior direito. São três telas:

1. **Detalhes** ← é aqui que você preencheu
2. **Elementos** ← tela final, cartões. **Pule**, deixe em branco
3. **Verificações** ← o YouTube procura direitos autorais. **Espere terminar.**

Se aparecer aviso de música com direitos autorais, **volte e troque a música**. Não
publique com aviso.

## Passo 5 — Visibilidade e publicar

| Opção | O que acontece | Quando usar |
|---|---|---|
| **Público** | todo mundo vê na hora | quando você já conferiu |
| **Não listado** | só quem tem o link vê | **use este no primeiro** — dá para conferir no celular antes |
| **Agendar** | você escolhe dia e hora | quando quiser postar sempre no mesmo horário |

Clique em **PUBLICAR** (ou **AGENDAR**).

## Short ou vídeo normal?

Você tem **dois formatos** na pasta e eles se comportam diferente:

| | Os 12 shorts | O vídeo longo (#13) |
|---|---|---|
| Formato | vertical **1080 × 1920** | horizontal **1920 × 1080** |
| Duração | menos de 1 minuto | vários minutos |
| Como o YouTube trata | **detecta como Short sozinho** | vídeo normal |
| O que você faz | nada de especial | nada de especial |

**Não existe um botão de "postar como Short".** O YouTube decide pela forma do vídeo:
**vertical + até 3 minutos = Short**. Como os seus são verticais e curtos, viram Short
automaticamente. Não precisa colocar `#Shorts` no título.

---

# PORTA 3B — Subir pelo celular (app do YouTube)

Se preferir fazer tudo pelo celular:

1. Abra o **app do YouTube**
2. Toque no **+** (embaixo, no meio)
3. Escolha **Criar um Short** (para os 12 shorts) ou **Enviar um vídeo** (para o longo)
4. Selecione o `.mp4` da galeria
5. **Título e descrição:** cole do pacote em inglês (mesmo texto)
6. **Visibilidade:** **Não listado** no primeiro
7. Toque em **Enviar**

⚠️ No celular o campo de descrição é apertado. Cole o título e, se a descrição não
couber, publique e **complete depois pelo computador** — a descrição pode ser editada
a qualquer momento.

---

# 🔴 A regra que não se negocia: a música

Se você usar música do **CapCut** e o YouTube identificar direitos autorais, o vídeo é
**bloqueado ou fica mudo**. Sem aviso, sem segunda chance.

**Use só a biblioteca de áudio do próprio YouTube.** Na hora de publicar → **Adicionar
som** → aba **Áudio** (a do YouTube, não a do CapCut). É grátis, nunca dá strike.

**Sem exceção.**

---

# ⚠️ Os 7 erros que travam o upload

| ❌ Erro | ✅ O que fazer |
|---|---|
| Arrastar o `.html` para o YouTube | YouTube **não aceita HTML**. Tem que ser `.mp4` |
| Vídeo deitado num upload de Short | Grave com **Fonte de Navegador** em 1080 × 1920 |
| Título genérico ("fermentação #1") | Use o título exato do pacote |
| Mesmo título em dois vídeos | Cada vídeo tem o título dele |
| Publicar com aviso de direitos autorais | Troque a música antes de publicar |
| Esquecer "não é conteúdo para crianças" | Sem responder, o **PUBLICAR** fica travado |
| Postar os 3 arquivos de repolho na mesma semana | **Um por legume** — veja `plano-de-postagem.md` |

---

# ✅ Depois de publicar — as primeiras 24 horas

1. **Comente você mesmo** uma pergunta. Ex.: `Which one are you trying first? 👇`
   Depois **fixe** esse comentário (segure o comentário → Fixar).
2. **Responda todo comentário** que aparecer. Nas primeiras horas isso pesa.
3. **Fixe o vídeo pilar no perfil:** Studio → **Personalizar** → **Layout** →
   **Vídeo em destaque** → escolha o guia geral (`#11`).
4. **Não apague vídeo com pouca visualização.** Um vídeo com 12 views hoje pode ser o
   que o algoritmo pega no mês que vem. Apagar zera a chance.

---

# 📅 A ordem de postagem

Não poste tudo de uma vez. São **7 semanas, 2 vídeos por semana**, sempre nos mesmos
dois dias.

A tabela completa — **qual arquivo abrir, com qual título, em que dia** — está em:

```
guias/plano-de-postagem.md
```

Semana 1: **Guia geral** (`#11`) + **Rabanete** (`#7`).

---

# 🖊️ O que falta decidir: o nome do canal

É o único item travando a Porta 1. Quando você decidir, é uma linha:

```bash
python _trocar-handle.py @seucanal --apply
```

Isso troca o placeholder nos **50 arquivos** de uma vez, com backup de cada um.
**Lembrando:** para os Shorts já renderizados isto é opcional — o `.mp4` sai limpo.

**Se quiser gravar antes de decidir o nome**, também dá: eu **removo** o handle de
todos e o vídeo sai limpo, sem marca nenhuma:

```bash
python _trocar-handle.py --limpar --apply
```

A diferença: se você gravar sem o handle, vai precisar **regravar** depois para o nome
aparecer. Se gravar com um handle provisório, é só trocar o canal e o vídeo continua
válido.

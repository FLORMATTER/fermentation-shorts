# Como transformar a animação HTML em vídeo de verdade

Guia para quem nunca gravou a tela na vida. Siga na ordem: **Parte 1 → Parte 2 → Parte 3**.

---

# PARTE 1 — GRAVAR A TELA DO COMPUTADOR

Se você está no computador, é o jeito mais fácil e o resultado sai com melhor qualidade.

## Passo 1 — Abrir a animação

1. Vá até a pasta `youtube-work` na sua Área de Trabalho
2. Dê **dois cliques** no arquivo `.html` (ex: `rabanete/shorts-rabanete-animado.html`)
3. Ele abre no navegador (Chrome, Edge, Firefox — tanto faz)
4. **Aperte F11** para ficar em tela cheia

✅ Você deve ver a animação com um botão de play no meio.

## Passo 2 — Preparar a tela para gravar

Antes de gravar, faça isto:

| O que fazer | Por quê |
|---|---|
| Feche **todas** as outras abas | Não aparecer notificação nem barra estranha |
| Desligue notificações do celular/PC | Não aparecer balãozinho no meio do vídeo |
| Esconda a barra de tarefas | Windows: botão direito na barra → Configurações → "Ocultar automaticamente" |
| Deixe o navegador em **tela cheia (F11)** | Só o desenho aparece |
| Tire o mouse do meio da tela | O cursor não deve aparecer no vídeo |

## Passo 3 — Escolher o programa de gravação

Escolha **UMA** das opções:

### Opção A — Xbox Game Bar (já vem no Windows, grátis)
1. Aperte **Windows + G**
2. Vai abrir uma barrinha. Clique no ícone de **círculo com bolinha** (Capturar)
3. Clique em **Gravar** (ou aperte **Windows + Alt + R**)
4. Para parar: aperte **Windows + Alt + R** de novo

⚠️ **Problema:** o Game Bar às vezes **não grava a Área de Trabalho nem o navegador**. Se não funcionar, use a Opção B.

### Opção B — OBS Studio (grátis, é o melhor) ⭐ RECOMENDO

1. Baixe em **obsproject.com** e instale
2. Abra o OBS
3. Em **Fontes**, clique no **+** → **Navegador** (Browser)
4. No campo **URL**, cole o caminho do arquivo com `file:///` na frente e **`?rec` no fim**:
   ```
   file:///C:/Users/Saxa/Desktop/youtube-work/rabanete/shorts-rabanete-animado-en.html?rec
   ```
   - **Largura:** `1080` · **Altura:** `1920`
5. Vá em **Configurações → Vídeo**:
   - Base (canvas) e Saída: **1080x1920**
   - FPS: **30**
6. Aperte **Iniciar Gravação**
7. **Espere 3 segundos** → clique com o **botão direito na fonte → Atualizar**
   (a animação recomeça do zero)
8. Quando acabar, **Parar Gravação**

> **Por que `?rec` na URL:** ele esconde a capa e os botões de play (que apareceriam
> no vídeo) e faz a animação começar sozinha. Sem `?rec`, o arquivo abre como short
> normal, só para assistir.
>
> ⚠️ **Por que NÃO usar "Captura de tela":** ela grava o monitor inteiro. Num monitor
> deitado (1920x1080) o Short vertical sai **deitado e com borda preta dos lados**.
> A Fonte de Navegador desenha a página fora da tela, no tamanho certo — sem crop,
> sem zoom e sem perda de qualidade.

### Opção C — Loom (mais simples, tem limite de tempo no plano grátis)
1. Acesse **loom.com** no navegador
2. Instale a extensão
3. Clique no ícone do Loom → **Screen and camera** → escolha só a aba
4. Grave

## Passo 4 — Gravar (o momento importante)

**A ordem certa é essa — não inverta:**

1. Aperte o botão de **gravar** primeiro
2. **Espere 3 segundos** parado (isso dá margem pra cortar depois)
3. Agora clique no **▶** da animação
4. **Não mexa no mouse. Não mexa em nada.** Deixe rodar até o fim
5. Quando a animação terminar, **espere 3 segundos** de novo
6. Só então **pare a gravação**

> **Por que esperar 3 segundos?** Porque o começo e o fim sempre têm um "tremidinho". Com essa sobra, você corta fora e fica limpo.

## Passo 5 — Onde o arquivo foi salvo

- **Game Bar:** `Vídeos\Capturas` (pasta Vídeos do Windows)
- **OBS:** a pasta que você escolheu (padrão: `Vídeos`)
- **Loom:** fica na nuvem, você baixa depois

O arquivo vai ser `.mp4`.

---

# PARTE 2 — GRAVAR A TELA DO CELULAR (Android)

Se você só tem celular, dá pra fazer também.

## Android — gravação nativa (a forma mais fácil)

1. Puxe a **barra de notificações** de cima pra baixo (duas vezes, pra abrir tudo)
2. Procure o ícone **"Gravador de tela"** ou **"Captura de tela"**
   - Não achou? Deslize para o lado — tem mais ícones escondidos
   - Ainda não achou? Vá em **Configurações** → pesquise "gravar tela"
3. Toque nele
4. Escolha:
   - **Áudio:** microfone desligado (você quer sem voz)
   - **Qualidade:** alta
5. Toque em **Iniciar**
6. Abra o arquivo `.html` no navegador do celular
   - **Como abrir:** abra o app **Arquivos** → encontre a pasta → toque no arquivo `.html` → escolha abrir com o Chrome
7. Gire o celular na **vertical** e dê play na animação
8. Terminou? Puxe a barra de novo e toque em **Parar**

## iPhone — gravação nativa

1. **Ajustes** → **Central de Controle** → adicione **Gravação de Tela**
2. Puxe a central de controle → toque no ícone de **bolinha dupla**
3. Espere a contagem de 3 segundos
4. Abra o HTML no **Safari** e dê play
5. **Mantenha o celular na vertical**
6. Para parar: toque na barra vermelha no topo

⚠️ **Dica pro celular:** gire o celular na **vertical** antes de gravar, senão o vídeo sai deitado e fica ruim pra Shorts.

---

# PARTE 3 — EDITAR NO CAPCUT E EXPORTAR

Agora você tem um arquivo `.mp4` meio "cru". Vamos deixá-lo apresentável.

## Passo 1 — Abrir o CapCut

1. Baixe o **CapCut** (grátis) na Play Store / App Store
2. Abra → **Novo projeto**
3. Selecione o vídeo que você gravou

## Passo 2 — Cortar as pontas

1. Você vai ver uma linha do tempo com o clipe
2. **Arraste o começo** do clipe para a direita — até onde a animação realmente começa
3. **Arraste o fim** para a esquerda — até onde a animação termina
4. Resultado: nada de "tremidinho" no começo nem no fim

## Passo 3 — Ajustar o formato (9:16)

1. Toque em **Proporção** (ou "Formato")
2. Escolha **9:16** (vertical)
3. Se o vídeo tiver barras pretas, use **Zoom** para preencher

## Passo 4 — Aumentar a velocidade (opcional, mas ajuda)

Vídeos de Shorts gostam de ritmo rápido.

1. Toque no clipe → **Velocidade** → **1.2x** ou **1.5x**
2. Veja se ainda dá tempo de ler os textos. Se não der, volte para 1.2x

## Passo 5 — Colocar música

1. Toque em **Áudio** → **Músicas** (biblioteca do CapCut) ou **Sons**
2. Busque por: `lofi`, `cooking`, `kitchen`, `beat` — músicas sem voz cantada
3. **Aumente o volume** da música
4. ⚠️ **Cuidado:** o CapCut já vem com música popular (tipo TikTok). Se o YouTube identificar direitos autorais, seu vídeo pode ser bloqueado. Se der problema, use música do próprio YouTube (na hora de postar, o YouTube oferece a biblioteca de áudio dele)

## Passo 6 — Exportar

1. Toque em **Exportar** (canto superior direito)
2. Escolha:
   - Resolução: **1080p**
   - FPS: **30**
3. Toque em Exportar de novo
4. O vídeo vai para a **galeria** do seu celular

✅ **Agora você tem um vídeo de verdade. Está pronto para postar.**

---

# PARTE 4 — POSTAR NO YOUTUBE

> **Guia completo de upload** — pelo computador, campo por campo, dizendo o que colar
> em cada um: `guias/guia-de-upload.md`. O resumo abaixo é o caminho pelo celular.

1. Abra o **app do YouTube** no celular
2. Toque no **+** (embaixo, no meio)
3. Escolha **Criar um Short**
4. Selecione o vídeo da galeria
5. **Título e descrição:** copie do pacote em inglês —
   `guias/pacote-legendas-descricoes-en.md`. Cada vídeo tem o título dele lá.
   ⚠️ **Não invente título genérico e não repita título entre dois vídeos.**
6. **Visibilidade:** comece com **"Não listado"** se quiser revisar antes, ou **"Público"** se já estiver satisfeito
7. Toque em **Enviar**

---

# RESUMO EM 7 PASSOS

```
1. Abrir o HTML no navegador (F11)
2. Esconder tudo da tela
3. Apertar GRAVAR
4. Esperar 3s → dar play → esperar o fim → esperar 3s → PARAR
5. Mandar o .mp4 pro CapCut
6. Cortar pontas + velocidade 1.2x + música
7. Exportar 1080p e postar como Short
```

---

# OS 6 ERROS QUE ESTRAGAM O VÍDEO

| ❌ Erro | ✅ Como evitar |
|---|---|
| Notificação aparecendo no meio | Desligar notificações ANTES de gravar |
| Mouse passando na tela | Tirar o mouse da tela depois de dar play |
| Vídeo deitado no celular | Girar o celular na vertical ANTES |
| Barras pretas em cima/embaixo | No CapCut, escolher 9:16 e usar Zoom |
| Começo tremido | Sempre esperar 3s antes de dar play |
| Música com direitos autorais | Usar a biblioteca de música do próprio YouTube |

---

# PERGUNTAS FREQUENTES

**P: Não tenho computador. Consigo só com o celular?**
Sim. Use a Parte 2 (gravar a tela do celular) e depois a Parte 3 (CapCut). Dá certo.

**P: Posso postar o arquivo .html direto no YouTube?**
Não. O YouTube não aceita HTML. Tem que ser vídeo `.mp4`.

**P: Quanto tempo leva pra fazer isso?**
A primeira vez, uns 30 minutos (você está aprendendo). Depois, uns 10 minutos por vídeo.

**P: Posso usar essas animações no vídeo final?**
Pode, mas **não use só elas**. Grave também o vídeo real com o legume de verdade. Vídeo real performa muito melhor que desenho.

**P: Preciso mostrar meu rosto?**
Não. Você já escolheu o formato "só as mãos". Isso funciona bem em canal de comida.

---

# O QUE FAZER DEPOIS

O caminho certo não é só gravar a animação. É:

1. **Grave o vídeo real** (legume de verdade, mão de verdade, mesa de verdade)
2. **Use a animação** como abertura ou como cena de explicação
3. **Some os dois** no CapCut
4. **Poste com constância** — 2x por semana, por 3 meses

O dinheiro não vem do primeiro vídeo. Vem do **décimo quinto**.

# -*- coding: utf-8 -*-
"""_skill-pao.py — skill: o botao nao e' texto extraivel + o gerador e' a fonte da verdade.

    python _skill-pao.py

Duas licoes do short do pao (`pao/`), que so' apareceram DEPOIS de tudo "limpo":
  1. o botao (`⏸ Pause` / `▶ Watch`) escapa do extrator — quem pega e' a comparacao;
  2. conserto feito por script a parte tem de VOLTAR para o gerador, senao regerar
     o arquivo desfaz o conserto — e sem erro nenhum.

Entram logo antes do "Selo mais estreito", que e' o assunto vizinho (idioma/traducao).

Ancora contada, aborta SEM GRAVAR.
"""
import io
import sys

ALVO = 'C:/Users/Saxa/.workbuddy-ai/skills/shorts-svg-animado/SKILL.md'

ANCORA = '### 📐 Selo mais estreito que o texto (o erro (h)) — o render é o único juiz'

NOVO = '''### 🔴 O botão não é texto extraível — e o gerador tem de ser a fonte da verdade

Dois furos que só apareceram no short do pão (`pao/`), **depois** de tudo parecer limpo.

**(1) O botão escapa do extrator.** `⏸ Pause` / `▶ Watch` não estão em `cap:`/`sub:`, nem
são nó de texto do corpo: um está no `<button>`, o outro em `btnPlay.textContent`. O
extrator do `_sobras-vs-original.py` **não os vê** — quem pegou foi o **teste por
comparação**, que confronta os **dois arquivos** e não depende de onde o texto mora.

> **Lição:** o teste por comparação é mais forte que o extrator. Um texto que não está em
> `cap:`/`sub:`/`<text>`/nó de texto **ainda assim** é pego — porque o teste olha o arquivo
> inteiro dos dois lados.

**(2) Conserto por script separado VOLTA para o gerador.** Os defeitos de contraste do pão
foram consertados pelo `_consertar-pao-contraste.py`, um script à parte. Só que o
`_criar-pao.py` **regenera** o arquivo a partir do template: rodar o gerador de novo
**desfazia o conserto** e o pote voltava a ler como bloco vazio.

> **Regra:** se um script **gera** o arquivo, todo conserto posterior tem de ser **dobrado
> de volta no gerador** (a lista `CONTRASTE`, a tradução dos botões). O gerador é a **fonte
> da verdade**. Conserto que fica só num script solto é dívida: o próximo que regenerar
> perde o trabalho e **não recebe erro nenhum**.

**Como provar que não regrediu** — duas medidas baratas:

```bash
md5sum <arquivo>-en.html        # o EN tem de sair com o MESMO md5 de antes
diff <(sed 's/\\r$//' antigo) <(sed 's/\\r$//' novo)   # o PT só difere nas linhas previstas
```

No pão: o EN saiu **byte-idêntico** (`4a810617…`) e o `diff` do PT mostrou **exatamente 3
linhas** (as dos botões). Como o **conteúdo** do EN não mudou, o `.mp4` já gravado
**continua válido** — não precisa regravar.

**Detalhe de âncora:** a lista `CONTRASTE` guarda as entradas com `\\n` e o laço converte
para o `eol` do arquivo (`v.replace('\\n', eol)`) **antes** de contar. Sem isso, uma âncora
de várias linhas casa **0 vezes** num arquivo CRLF.

**E cuidado com âncora que é PREFIXO de outra.** `"…no Portuguese original** - it was built
in English."` casava **2 vezes** (#18 e #20). Quando a contagem esperada é 1 e a string pode
ser prefixo, **incluir a linha de baixo no texto da âncora** — foi o que resolveu.

'''


def main():
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    antes = len(d.encode('utf-8'))
    print('%s\n  %d bytes, %s' % (ALVO, antes, 'CRLF' if eol == '\r\n' else 'LF'))

    a = ANCORA.replace('\n', eol)
    c = d.count(a)
    if c != 1:
        print('  ERRO: ancora casou %d (esperado 1)' % c)
        print('\nABORTADO — nada foi gravado.')
        return 1

    if 'O gerador é a **fonte\n  da verdade**' in d or 'o gerador tem de ser a fonte da verdade' in d:
        print('  ja\' registrado — nada a fazer')
        return 0

    d = d.replace(a, NOVO.replace('\n', eol) + a, 1)

    provas = [
        ('botao nao extraivel', 'O botão escapa do extrator' in d),
        ('gerador fonte da verdade', 'fonte\n  da verdade' in d or 'fonte da verdade' in d),
        ('prova md5', 'md5sum <arquivo>-en.html' in d),
        ('ancora prefixo', 'PREFIXO de outra' in d),
        ('ancora preservada', d.count(a) == 1),
    ]
    ruins = [n for n, ok in provas if not ok]
    if ruins:
        print('\nABORTADO — prova falhou: %s' % ruins)
        return 1
    print('  provas: %d/%d ok' % (len(provas), len(provas)))

    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    depois = len(d.encode('utf-8'))
    print('  gravado: %d -> %d bytes (+%d)' % (antes, depois, depois - antes))
    return 0


if __name__ == '__main__':
    sys.exit(main())

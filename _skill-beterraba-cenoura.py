# -*- coding: utf-8 -*-
"""_skill-beterraba-cenoura.py — 3 inserts contados no SKILL.md.

  1. VERIFICADOR do erro (k) — com os dois furos que ele mesmo teve;
  2. as licoes de FORMA do #25 (colher, faca, relogio, folha, rotulos colidindo);
  3. o 3o furo da troca de BLOCO por regex: alternacao no meio do padrao.

O arquivo e' editado UMA vez, por script com contagem — duas edicoes no mesmo
arquivo na mesma mensagem se sobrescrevem.

    python _skill-beterraba-cenoura.py
"""
import io
import os
import sys

SKILL = os.path.expanduser('~/.workbuddy-ai/skills/shorts-svg-animado/SKILL.md')

VERIFICADOR = '''**Verificar isso por script e' melhor que olhar.** Em 23/09, no `#25` (beterraba+cenoura),
o erro (k) apareceu em **3 das 7 cenas** — e eu mesmo tinha escrito os dois lados. O
verificador que pega:

```python
def acha_repeticoes(txt):
    """Cenas em que o `cap` repete algum <text> da propria cena."""
    blocos = re.findall(
        r'def s(\\d)\\(t\\):(.*?)(?=\\ndef s\\d\\(t\\):|\\n# -{3,} montagem)', txt, re.S)
    caps = re.findall(r"TAG, '([^']*)',", txt)
    fora = []
    for (idx, corpo), cap in zip(blocos, caps):
        textos = [t.strip().lower() for t in
                  re.findall(r'<text[^>]*>([^<]*)</text>', corpo)]
        if cap.strip().lower() in textos:
            fora.append('s%s "%s"' % (idx, cap))
    return fora
```

**Dois furos que esse verificador ja' teve:**

1. **Selecionar "o titulo" por `font-size` nao funciona.** A 1a versao procurava
   `font-size="18"` e a conta nao fechou: a cena do sal titula com **46 px** (e' o "2%") e a
   do truque com **17 px**. **Varrer TODOS os `<text>` da cena** e' o certo — o titulo e'
   qualquer texto que esteja la'.
2. **Verificador que nunca falha nao prova nada.** Rodar a checagem **no arquivo ANTES do
   conserto** e exigir que ela **acuse**. Se passar limpa nos dois estados, nao esta medindo
   nada. No #25 ela acusou **3** antes e **0** depois — foi assim que se soube que funcionava.

'''

FORMA = '''**Colher ≠ quadrilatero.** A cuia sozinha, de perfil, le' como **folha de papel flutuando**.
O que faz ler "colher" e' a dupla **CUIA + CABO**: elipse funda com aro **e** o cabo visivel
preso nela.

**Faca de pe' ≠ faca.** Lamina estreita e vertical le' como **tubo de ensaio**. A faca de
chef tem de ser desenhada **deitada** — lamina longa (2x a largura) + bolster + cabo curto
com rebites — e so' entao girada.

**Relogio com 4 marcas ≠ relogio.** Le' como **bussola**. Sao **12** marcas, com as das horas
mais compridas.

**Folha com limbo fino ≠ folha.** Le' como **broto**. O limbo tem de ser largo e ter nervura.

**Dois marcadores proximos colam os ROTULOS.** Numa barra de pH, "BEET" (5,3) e "CARROT"
(5,9) ficam a **0,6 de pH = 37 px**, e "CARROT" a 13 px tem ~47 px de largura -> saiu
**"BEETCARROT"**. Nao e' o texto que e' longo demais para a caixa (erro (h)): e' a
**posicao**, que vem do dado. Conserto: um `dy` que **escalona o rotulo na vertical**.

'''

REGEX3 = '''3. **Alternacao no meio do padrao monta o nome errado.** Generalizar o padrao para servir
   dois tipos de bloco — `r'(?:def|TEXTOS = )%s\\(?.*?\\n' % nome` — produz
   **`TEXTOS = TEXTOS`** para o segundo caso e **nunca casa**. **Dar a cada bloco o padrao
   COMPLETO, escrito por extenso**, em vez de montar um generico com `%`.

'''

# (ancora, texto a PREPOR, quantas vezes)
INSERTS = (
    ('## 📐 Formato de UPLOAD (1080×1920) — o short que já sai pronto', VERIFICADOR, 1),
    ('**A regra que fica:** quando o desenho "não parece", **não é a cor** — é a **forma**, e forma',
     FORMA, 1),
    ('**E o `%` do Python:** uma string SVG com `%` solto', REGEX3, 1),
)


def main():
    with io.open(SKILL, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    antes = len(d.encode('utf-8'))

    for ancora, texto, n in INSERTS:
        achou = d.count(ancora)
        if achou != n:
            print('ERRO: ancora casou %d vez(es), esperava %d:\n  %s'
                  % (achou, n, ancora[:70]))
            return 1

    for ancora, texto, n in INSERTS:
        d = d.replace(ancora, texto + ancora, n)
        print('  ok: +%d bytes antes de "%s..."'
              % (len(texto.encode('utf-8')), ancora[:44]))

    for ancora, _, _ in INSERTS:
        if d.count(ancora) != 1:
            print('ERRO: a ancora sumiu/duplicou depois da troca')
            return 1
    if len(d.encode('utf-8')) <= antes:
        print('ERRO: o arquivo nao cresceu')
        return 1

    with io.open(SKILL, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('OK: 3 inserts | %d -> %d bytes' % (antes, len(d.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())

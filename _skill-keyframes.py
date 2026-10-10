# -*- coding: utf-8 -*-
"""_skill-keyframes.py — registra na SKILL.md as licoes da limpeza de keyframes.

Dois inserts, com contagem: se alguma ancora nao casar exatamente 1 vez, ABORTA
sem gravar (regra do projeto: nunca editar o mesmo arquivo as cegas).

    python _skill-keyframes.py            # dry-run
    python _skill-keyframes.py --apply
"""
import io
import os
import sys

SKILL = os.path.join(os.path.expanduser('~'), '.workbuddy-ai', 'skills',
                     'shorts-svg-animado', 'SKILL.md')

ANCORA_A = ("> Para isso existe o `python _y-absoluto.py <arquivo>`, que soma os "
            "`translate()` aninhados.\n")

NOVO_A = ANCORA_A + """>
>
> 🔴 **O validador não sabe LER HTML — só casar regex.** Duas famílias de falso positivo
> que já custaram tempo (23/09): (a) o `@keyframes\\s+(\\w+)` casa **prosa** — numa aula,
> *"Escreva o @keyframes **dentro** do `<style>`"* entrou como uma definição chamada
> `dentro`; (b) o "hex suspeito" casa **id** — `#card` vira `#car`, e a barra de legenda do
> player 16:9 (`#cap`, `#cbar`, `#ffi`) entra como se fosse cor. **Antes de "consertar" um
> aviso, abrir a linha no arquivo e olhar.** Os 6 avisos que sobraram na série são todos
> desse tipo — não há mais defeito real escondido neles.
>
> **Limpar `@keyframes` morto:** `python _limpar-keyframes.py` (dry-run) / `--apply`. Só
> remove quando o nome aparece **UMA** vez no arquivo (só na própria definição) — é o que
> cobre o furo do `animation:\\s*([\\w-]+)`, que num shorthand `animation: 2s spin` captura
> `2s` e deixaria `spin` passar por morto. Em 23/09: **42 regras em 19 arquivos**; o
> validador da série caiu de **25 para 6** avisos, e os 6 são falso positivo.
"""

ANCORA_B = "## 🗂 Organizar as pastas do projeto (quando a raiz estiver cheia)\n"

NOVO_B = """## 🧪 Provar que um refactor não mudou nada — A/B de render

Tirar código morto, renomear, mexer em CSS: o `_validar-short.py` **não** prova que a tela
ficou igual — ele mede coordenadas. A prova é **renderizar as duas versões e comparar os
PNGs byte a byte**. Foi assim que se limpou 42 `@keyframes` mortos de 19 arquivos (23/09):

```bash
python _provar-keyframes.py --teste   # CONTROLE NEGATIVO — fazer SEMPRE primeiro
python _provar-keyframes.py           # A/B de todos os arquivos do registro
```

- 🔴 **O controle negativo é obrigatório.** Comparador que nunca acusa nada não prova nada.
  O `--teste` arranca de propósito um keyframe **USADO** e **exige** que a comparação acuse
  a diferença (acusou: 48.880 vs 50.088 bytes). Só depois disso o "idêntico" dos outros vale.
- 🔴 **Descobrir os PNGs novos por `os.listdir` antes/depois NÃO funciona.** Vários
  `-final.png` desses shorts **já existiam** de sessões anteriores: o render sobrescreve o
  arquivo e o nome **não** aparece como novo — **12 renders que deram certo foram
  reportados como "falhou"**. Ler os caminhos que o próprio `_revisar-cenas.py` imprime
  (`-> caminho`).
- **O Chrome não solta o perfil de primeira.** Em 38 renders seguidos no mesmo
  `--user-data-dir`, alguns saem sem PNG nenhum. **Repetir até 3 vezes, com 2 s de espera.**
- **O modo é o `--final`** (estado final congelado) — é onde um keyframe que faltasse
  apareceria. O `--no-anim` **não** serve para isso: sem animação o elemento aparece no
  lugar certo de qualquer jeito.
- **Chaves: conferir o TRECHO removido, não o arquivo inteiro.** `arquivo.count('{')` não
  fecha em HTML nenhum (o JS tem chave dentro de string e de regex) — a checagem "chaves
  balanceadas" reprovou os 19 arquivos de uma vez, por falso positivo. O que vale é
  `trecho.count('{') == trecho.count('}')` na regra que saiu.

""" + ANCORA_B


def main():
    aplicar = '--apply' in sys.argv
    d = io.open(SKILL, encoding='utf-8', newline='').read()
    antes = len(d)

    for nome, anc, novo in (('A (falso positivo do validador)', ANCORA_A, NOVO_A),
                            ('B (secao A/B de render)', ANCORA_B, NOVO_B)):
        n = d.count(anc)
        print('ancora %-34s %d vez(es)' % (nome, n))
        if n != 1:
            print('ABORTA: a ancora %s nao casou 1 vez.' % nome)
            return 1
    for anc, novo in ((ANCORA_A, NOVO_A), (ANCORA_B, NOVO_B)):
        d = d.replace(anc, novo, 1)

    for trecho in ('O validador não sabe LER HTML', '_limpar-keyframes.py',
                   'A/B de render', '_provar-keyframes.py --teste',
                   'controle negativo é obrigatório'):
        if trecho not in d:
            print('ABORTA: nao achei "%s" no texto novo.' % trecho)
            return 1

    print('SKILL.md: %d -> %d bytes (+%d)' % (antes, len(d), len(d) - antes))
    if not aplicar:
        print('(dry-run — use --apply)')
        return 0
    with io.open(SKILL, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

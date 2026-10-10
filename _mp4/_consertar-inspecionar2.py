# -*- coding: utf-8 -*-
"""Corrige o contador de quadros do _mp4/inspecionar.py (2a tentativa).

   A 1a tentativa so caia no 'trun' quando o box stsz NAO existia. Mas o mp4
   fragmentado do MediaRecorder TEM stsz — declarando 0 amostras (as amostras de
   verdade ficam nos 'trun' dos 10 fragmentos). Entao a condicao tem que ser
   "contagem == 0", nao "box ausente".
   Aborta SEM GRAVAR se a ancora nao casar exatamente 1 vez."""
import io, os, sys

ARQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inspecionar.py')

OLD = u'''    amostras = achar(d, 0, len(d), ['moov', 'trak', 'mdia', 'minf', 'stbl', 'stsz'])
    if amostras:
        n = struct.unpack('>I', d[amostras[0] + 8:amostras[0] + 12])[0]
        print('quadros   : %d  (~%.1f fps)' % (n, n / seg if seg else 0))
    else:
        # mp4 FRAGMENTADO (o que o MediaRecorder produz) nao tem stbl/stsz: os
        # quadros vivem nos 'trun' dos fragmentos. Sem isto o relatorio dizia
        # "quadros: 0", que parece video vazio e nao e.
        n = 0
        i = -1
        while True:
            i = d.find(b'trun', i + 1)
            if i < 0:
                break
            try:
                n += struct.unpack('>I', d[i + 8:i + 12])[0]
            except struct.error:
                pass
        if n:
            print('quadros   : %d  (~%.1f fps)  [mp4 fragmentado]'
                  % (n, n / seg if seg else 0))
        else:
            print('quadros   : (sem tabela de amostras e sem trun)')
    return 0'''

NEW = u'''    n = 0
    amostras = achar(d, 0, len(d), ['moov', 'trak', 'mdia', 'minf', 'stbl', 'stsz'])
    if amostras:
        n = struct.unpack('>I', d[amostras[0] + 8:amostras[0] + 12])[0]
    if n:
        print('quadros   : %d  (~%.1f fps)' % (n, n / seg if seg else 0))
    else:
        # mp4 FRAGMENTADO (o que o MediaRecorder produz): o stsz existe mas
        # declara 0 amostras — os quadros de verdade ficam nos 'trun' dos
        # fragmentos. Sem isto o relatorio dizia "quadros: 0", que parece video
        # vazio e nao e. Layout do trun: [size][type][ver+flags][sample_count]...
        # entao sample_count esta em (indice do 'trun') + 8.
        i = -1
        while True:
            i = d.find(b'trun', i + 1)
            if i < 0:
                break
            try:
                n += struct.unpack('>I', d[i + 8:i + 12])[0]
            except struct.error:
                pass
        if n:
            print('quadros   : %d  (~%.1f fps)  [mp4 fragmentado, %d trun]'
                  % (n, n / seg if seg else 0, d.count(b'trun')))
        else:
            print('quadros   : (sem amostras no stsz e sem trun)')
    return 0'''

d = io.open(ARQ, encoding='utf-8', newline='').read()
n = d.count(OLD)
print('ancora: %d ocorrencia(s) %s' % (n, 'OK' if n == 1 else '<-- FALHOU'))
if n != 1:
    print('ABORTADO: nada foi gravado.')
    sys.exit(1)
io.open(ARQ, 'w', encoding='utf-8', newline='').write(d.replace(OLD, NEW, 1))
print('GRAVADO: %s' % ARQ)

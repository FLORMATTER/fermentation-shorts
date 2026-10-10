# -*- coding: utf-8 -*-
"""Le os boxes de um .mp4 e imprime marca, duracao real e resolucao do video.
   Sem ffmpeg: le o cabecalho na mao. Uso: python _mp4/inspecionar.py arquivo.mp4"""
import io, struct, sys


def boxes(d, ini, fim):
    """Percorre os boxes de uma faixa. Devolve (tipo, inicio_payload, fim)."""
    p = ini
    while p + 8 <= fim:
        size = struct.unpack('>I', d[p:p + 4])[0]
        typ = d[p + 4:p + 8].decode('latin-1')
        head = 8
        if size == 1:
            size = struct.unpack('>Q', d[p + 8:p + 16])[0]
            head = 16
        elif size == 0:
            size = fim - p
        if size < head or p + size > fim:
            return
        yield typ, p + head, p + size
        p += size


def achar(d, ini, fim, caminho):
    """caminho = ['moov','trak','tkhd'] -> (inicio, fim) do payload do ultimo."""
    for alvo in caminho:
        achou = None
        for typ, a, b in boxes(d, ini, fim):
            if typ == alvo:
                achou = (a, b)
                break
        if not achou:
            return None
        ini, fim = achou
    return (ini, fim)


def ler_mvhd(d, a):
    ver = d[a]
    p = a + 4
    if ver == 1:
        ts, du = struct.unpack('>IQ', d[p + 16:p + 28])
    else:
        ts, du = struct.unpack('>II', d[p + 8:p + 16])
    return ts, du


def ler_tkhd(d, a):
    ver = d[a]
    p = a + 4
    if ver == 1:
        w, h = struct.unpack('>II', d[p + 84:p + 92])
    else:
        w, h = struct.unpack('>II', d[p + 72:p + 80])
    return w / 65536.0, h / 65536.0


def ler_stsd_codec(d, a):
    """Primeiro sample entry do stsd -> nome do codec."""
    n = struct.unpack('>I', d[a + 4:a + 8])[0]
    if n == 0:
        return '?'
    return d[a + 12:a + 16].decode('latin-1')


def main(caminho):
    d = io.open(caminho, 'rb').read()
    print('arquivo   : %s' % caminho)
    print('tamanho   : %d bytes (%.1f MB)' % (len(d), len(d) / 1048576.0))

    marca = '?'
    for typ, a, b in boxes(d, 0, len(d)):
        if typ == 'ftyp':
            marca = d[a:a + 4].decode('latin-1')
            break
    print('marca     : %s' % marca)

    mv = achar(d, 0, len(d), ['moov', 'mvhd'])
    if not mv:
        print('SEM moov/mvhd -> o arquivo nao esta finalizado (gravacao interrompida?)')
        return 1
    ts, du = ler_mvhd(d, mv[0])
    seg = du / float(ts)
    print('duracao   : %.2f s  (timescale %d, duration %d)' % (seg, ts, du))

    tk = achar(d, 0, len(d), ['moov', 'trak', 'tkhd'])
    if tk:
        w, h = ler_tkhd(d, tk[0])
        print('resolucao : %.0f x %.0f' % (w, h))
        if h > w:
            print('formato   : VERTICAL 9:16  ->  %s' % ('OK' if abs(w / h - 9 / 16.0) < 0.01 else 'ATENCAO, nao e 9:16'))
        else:
            print('formato   : horizontal 16:9')

    st = achar(d, 0, len(d), ['moov', 'trak', 'mdia', 'minf', 'stbl', 'stsd'])
    if st:
        print('codec     : %s' % ler_stsd_codec(d, st[0]))

    n = 0
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
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '_mp4/out/proto.mp4'))

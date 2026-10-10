"""_mp4/diagnosticar.py — conta as amostras que REALMENTE entraram no arquivo e
compara com o que o motor desenhou. Sem ffmpeg.

    python _mp4/diagnosticar.py <arquivo>.mp4 [--desenhou=N]

Responde tres perguntas que decidem se a retimagem e' valida:
  1. quantas amostras existem e como estao distribuidas nos fragmentos;
  2. a soma das duracoes cruas bate com a duracao do mvhd?
  3. (com --desenhou) quantos quadros o motor empurrou e quantos sobreviveram?
"""
import struct
import sys


def iter_boxes(buf, ini, fim):
    p = ini
    while p + 8 <= fim:
        tam = struct.unpack_from('>I', buf, p)[0]
        tipo = buf[p + 4:p + 8].decode('latin-1')
        cab = 8
        if tam == 1:
            tam = struct.unpack_from('>Q', buf, p + 8)[0]
            cab = 16
        elif tam == 0:
            tam = fim - p
        if tam < cab or p + tam > fim:
            return
        yield (tipo, p, cab, tam)
        p += tam


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    arq = args[0]
    desenhou = None
    for a in sys.argv[1:]:
        if a.startswith('--desenhou='):
            desenhou = int(a.split('=')[1])

    buf = open(arq, 'rb').read()
    tops = list(iter_boxes(buf, 0, len(buf)))

    # mvhd / mdhd
    ts_movie = ts_media = dur_movie = None
    for tipo, p, cab, tam in tops:
        if tipo != 'moov':
            continue
        for t2, p2, c2, m2 in iter_boxes(buf, p + cab, p + tam):
            if t2 in ('trak', 'mdia'):
                pass
        for t2, p2, c2, m2 in iter_boxes(buf, p + cab, p + tam):
            if t2 in ('trak',):
                for t3, p3, c3, m3 in iter_boxes(buf, p2 + c2, p2 + m2):
                    if t3 == 'mdia':
                        for t4, p4, c4, m4 in iter_boxes(buf, p3 + c3, p3 + m3):
                            if t4 == 'mdhd':
                                c = p4 + c4
                                v = buf[c]
                                ts_media = struct.unpack_from('>I', buf, c + (20 if v == 1 else 12))[0]
                                dur_media = struct.unpack_from('>Q' if v == 1 else '>I', buf, c + (24 if v == 1 else 16))[0]
                                print('mdhd  : timescale=%d duration=%d' % (ts_media, dur_media))

    frags = []
    durs = []
    for tipo, p, cab, tam in tops:
        if tipo != 'moof':
            continue
        for t2, p2, c2, m2 in iter_boxes(buf, p + cab, p + tam):
            if t2 != 'traf':
                continue
            for t3, p3, c3, m3 in iter_boxes(buf, p2 + c2, p2 + m2):
                if t3 == 'trun':
                    c = p3 + c3
                    flags = struct.unpack_from('>I', buf, c)[0] & 0xFFFFFF
                    n = struct.unpack_from('>I', buf, c + 4)[0]
                    q = c + 8
                    if flags & 0x000001:
                        q += 4
                    if flags & 0x000004:
                        q += 4
                    passo = 4 * ((1 if flags & 0x000100 else 0) + (1 if flags & 0x000200 else 0) +
                                 (1 if flags & 0x000400 else 0) + (1 if flags & 0x000800 else 0))
                    for i in range(n):
                        durs.append(struct.unpack_from('>I', buf, q + i * passo)[0] if flags & 0x000100 else 0)
                    frags.append(n)

    total = sum(frags)
    print('fragmentos : %d  -> %s amostras' % (len(frags), frags))
    print('amostras   : %d' % total)
    if durs and ts_media:
        print('soma crua  : %d / %d = %.3f s' % (sum(durs), ts_media, sum(durs) / ts_media))
        print('duracao 1a : %d / %d = %.3f s' % (durs[0], ts_media, durs[0] / ts_media))
        print('duracao ult: %d / %d = %.3f s' % (durs[-1], ts_media, durs[-1] / ts_media))
        print('mediana    : %d / %d = %.1f ms' % (sorted(durs)[len(durs) // 2], ts_media,
                                                  sorted(durs)[len(durs) // 2] / ts_media * 1000))
    if desenhou:
        print('desenhados : %d   perdidos: %d  (%.0f%% sobreviveu)'
              % (desenhou, desenhou - total, 100.0 * total / desenhou))


if __name__ == '__main__':
    main()

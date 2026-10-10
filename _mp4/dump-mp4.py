"""_mp4/dump-mp4.py — mostra a ARVORE de boxes de um .mp4 e os campos que a
retimagem precisa mexer. Sem ffmpeg.

    python _mp4/dump-mp4.py mosquito/shorts-mosquito-trap-en.mp4

Por que existe: antes de reescrever a duracao de cada amostra (para transformar
um arquivo VFR gravado em tempo real num arquivo de taxa constante) e' preciso
saber EXATAMENTE onde estao os campos: qual timescale o mdhd usa, se o trun
carrega duracao por amostra ou se ela vem do tfhd, e se existe tfdt/mehd/elst.
Chutar isso corrompe o arquivo.
"""
import sys
import struct

CAMPO = {
    'ftyp': 0, 'moov': 0, 'trak': 0, 'mdia': 0, 'minf': 0, 'stbl': 0, 'mvex': 0,
    'moof': 0, 'traf': 0, 'edts': 0, 'dinf': 0,
}


def boxes(buf, ini, fim, nivel=0, saida=None):
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
        if tam < cab:
            saida.append('  ' * nivel + '!! box invalido em %d (%s tam=%d)' % (p, tipo, tam))
            return
        corpo = p + cab
        fimb = p + tam
        saida.append('  ' * nivel + '%-6s off=%-9d tam=%-9d' % (tipo, p, tam))
        if tipo in CAMPO:
            boxes(buf, corpo, fimb, nivel + 1, saida)
        else:
            detalhe(buf, tipo, corpo, fimb, nivel + 1, saida)
        p = fimb


def detalhe(buf, tipo, c, f, nivel, saida):
    pre = '  ' * nivel
    ver = buf[c]
    flags = struct.unpack_from('>I', buf, c)[0] & 0xFFFFFF
    try:
        if tipo == 'mvhd':
            if ver == 1:
                ts = struct.unpack_from('>I', buf, c + 20)[0]
                du = struct.unpack_from('>Q', buf, c + 24)[0]
            else:
                ts = struct.unpack_from('>I', buf, c + 12)[0]
                du = struct.unpack_from('>I', buf, c + 16)[0]
            saida.append('%smvhd v%d timescale=%d duration=%d (%.3f s)'
                         % (pre, ver, ts, du, du / ts if ts else 0))
        elif tipo == 'tkhd':
            if ver == 1:
                du = struct.unpack_from('>Q', buf, c + 28)[0]
            else:
                du = struct.unpack_from('>I', buf, c + 20)[0]
            saida.append('%stkhd v%d flags=0x%06x duration=%d (escala do MOVIE)'
                         % (pre, ver, flags, du))
        elif tipo == 'mdhd':
            if ver == 1:
                ts = struct.unpack_from('>I', buf, c + 20)[0]
                du = struct.unpack_from('>Q', buf, c + 24)[0]
            else:
                ts = struct.unpack_from('>I', buf, c + 12)[0]
                du = struct.unpack_from('>I', buf, c + 16)[0]
            saida.append('%smdhd v%d timescale=%d duration=%d (%.3f s)  <-- escala da MIDIA'
                         % (pre, ver, ts, du, du / ts if ts else 0))
        elif tipo == 'mehd':
            du = struct.unpack_from('>Q', buf, c + 4)[0] if ver == 1 else struct.unpack_from('>I', buf, c + 4)[0]
            saida.append('%smehd v%d fragment_duration=%d' % (pre, ver, du))
        elif tipo == 'elst':
            n = struct.unpack_from('>I', buf, c + 4)[0]
            saida.append('%selst v%d entradas=%d' % (pre, ver, n))
            p = c + 8
            for i in range(min(n, 4)):
                if ver == 1:
                    sd, mt = struct.unpack_from('>QQ', buf, p)
                    p += 20
                else:
                    sd, mt = struct.unpack_from('>II', buf, p)
                    p += 12
                saida.append('%s   [%d] segment_duration=%d media_time=%d' % (pre, i, sd, mt))
        elif tipo == 'tfhd':
            tid = struct.unpack_from('>I', buf, c + 4)[0]
            p = c + 8
            extra = []
            if flags & 0x000001:
                extra.append('base_data_offset=%d' % struct.unpack_from('>Q', buf, p)[0]); p += 8
            if flags & 0x000002:
                extra.append('sample_desc=%d' % struct.unpack_from('>I', buf, p)[0]); p += 4
            if flags & 0x000008:
                extra.append('default_sample_duration=%d' % struct.unpack_from('>I', buf, p)[0]); p += 4
            if flags & 0x000010:
                extra.append('default_sample_size=%d' % struct.unpack_from('>I', buf, p)[0]); p += 4
            if flags & 0x000020:
                extra.append('default_sample_flags=0x%08x' % struct.unpack_from('>I', buf, p)[0]); p += 4
            saida.append('%stfhd flags=0x%06x track=%d %s' % (pre, flags, tid, ' '.join(extra)))
        elif tipo == 'tfdt':
            if ver == 1:
                b = struct.unpack_from('>Q', buf, c + 4)[0]
            else:
                b = struct.unpack_from('>I', buf, c + 4)[0]
            saida.append('%stfdt v%d baseMediaDecodeTime=%d' % (pre, ver, b))
        elif tipo == 'trun':
            n = struct.unpack_from('>I', buf, c + 4)[0]
            p = c + 8
            durs = []
            if flags & 0x000001:
                p += 4
            if flags & 0x000004:
                p += 4
            tam_amostra = 0
            if flags & 0x000100:
                tam_amostra += 4
            if flags & 0x000200:
                tam_amostra += 4
            if flags & 0x000400:
                tam_amostra += 4
            if flags & 0x000800:
                tam_amostra += 4
            if flags & 0x000100:
                for i in range(min(n, 6)):
                    durs.append(struct.unpack_from('>I', buf, p + i * tam_amostra)[0])
            saida.append('%strun flags=0x%06x amostras=%d dur_por_amostra=%s %s'
                         % (pre, flags, n, 'SIM' if flags & 0x000100 else 'NAO',
                            ('primeiras: ' + str(durs)) if durs else ''))
        elif tipo == 'stts':
            n = struct.unpack_from('>I', buf, c + 4)[0]
            saida.append('%sstts v%d entradas=%d' % (pre, ver, n))
        elif tipo == 'stsz':
            n = struct.unpack_from('>I', buf, c + 8)[0]
            saida.append('%sstsz v%d amostras=%d' % (pre, ver, n))
        elif tipo == 'stsd':
            n = struct.unpack_from('>I', buf, c + 4)[0]
            codec = buf[c + 12:c + 16].decode('latin-1') if f - c > 16 else '?'
            saida.append('%sstsd v%d entradas=%d codec=%s' % (pre, ver, n, codec))
    except Exception as e:
        saida.append('%s%s  (nao li: %s)' % (pre, tipo, e))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    buf = open(sys.argv[1], 'rb').read()
    saida = []
    print('arquivo: %s  (%d bytes)' % (sys.argv[1], len(buf)))
    boxes(buf, 0, len(buf), 0, saida)
    print('\n'.join(saida))


if __name__ == '__main__':
    main()

"""_mp4/retimar.py — converte o .mp4 gravado em TEMPO REAL (VFR) num .mp4 de
TAXA CONSTANTE (CFR). Sem ffmpeg, sem recodificar: so reescreve a duracao de
cada amostra, no lugar (o tamanho do arquivo nao muda).

    python _mp4/retimar.py <arq>.mp4 --fps=30 --quadros=1710 --bruto

Por que existe: o MediaRecorder carimba cada quadro com a hora REAL da chamada de
track.requestFrame(). E pior: quando a fila do codificador enche ele DESCARTA
quadro sem avisar (medido: 76% sobreviveu a 19 q/s). Quadro descartado deixa o
anterior o DOBRO do tempo na tela — e' isso que o olho le como travamento.

A solucao tem duas partes:
  1. gravar em CFR (um indice de quadro por vez, sem olhar o relogio) com PASSO,
     para o codificador nunca encher a fila;
  2. retimar aqui: toda amostra recebe a mesma duracao 1/fps.

--quadros=N e' a rede de seguranca. Se o navegador ainda descartar algum quadro,
o video NAO sai curto: as N amostras que sobraram sao distribuidas na duracao
certa, entao o arquivo toca no tempo certo, em taxa constante, um pouco mais
devagar. Nunca sai acelerado nem cortado.

Estrutura real do arquivo do Chrome (conferida com dump-mp4.py):
    mvhd v1  timescale=1000   duration=<ms>
    tkhd v1  duration=<ms>                 (escala do MOVIE)
    mdhd v1  timescale=30000  duration=<lixo! o Chrome grava ms aqui>
    mvex > trex                            (sem mehd)
    moof > traf > tfhd flags=0x020020      (default-base-is-moof + sample_flags)
                > tfdt v1  baseMediaDecodeTime
                > trun flags=0x000305      (data_offset + first_sample_flags
                                            + duracao + tamanho por amostra)
    stts entradas=0 / stsz amostras=0      -> fragmentado, nada a mexer no stbl
"""
import shutil
import struct
import sys

CONTEDOR = {'moov', 'trak', 'mdia', 'minf', 'stbl', 'mvex', 'moof', 'traf', 'edts', 'dinf'}


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


def percorre(buf, ini, fim, pilha=()):
    for tipo, p, cab, tam in iter_boxes(buf, ini, fim):
        yield (pilha + (tipo,), p, cab, tam)
        if tipo in CONTEDOR:
            for item in percorre(buf, p + cab, p + tam, pilha + (tipo,)):
                yield item


def achar(arvore, caminho):
    for cam, p, cab, tam in arvore:
        if cam == caminho:
            return p, cab, tam
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__)
        return 2
    arq = args[0]
    fps = 30
    esperado = 0
    for a in sys.argv[1:]:
        if a.startswith('--fps='):
            fps = int(a[6:])
        elif a.startswith('--quadros='):
            esperado = int(a[10:])
    bruto = '--bruto' in sys.argv

    buf = bytearray(open(arq, 'rb').read())
    arvore = list(percorre(buf, 0, len(buf)))

    mvhd = achar(arvore, ('moov', 'mvhd'))
    tkhd = achar(arvore, ('moov', 'trak', 'tkhd'))
    mdhd = achar(arvore, ('moov', 'trak', 'mdia', 'mdhd'))
    if not (mvhd and tkhd and mdhd):
        print('ERRO: nao achei mvhd/tkhd/mdhd')
        return 1

    def ler_ts(box):
        p, cab, tam = box
        c = p + cab
        off = 20 if buf[c] == 1 else 12
        return struct.unpack_from('>I', buf, c + off)[0]

    ts_movie = ler_ts(mvhd)
    ts_media = ler_ts(mdhd)
    if not ts_movie or not ts_media:
        print('ERRO: timescale zero')
        return 1
    if ts_media % fps:
        print('ERRO: timescale da midia %d nao divide por %d' % (ts_media, fps))
        return 1
    D = ts_media // fps

    # ---------- 1. colher as posicoes de cada duracao de amostra ----------
    truns = [x for x in arvore if x[0][-1] == 'trun']
    tfdts = [x for x in arvore if x[0][-1] == 'tfdt']
    if not truns:
        print('ERRO: nenhum trun (arquivo nao e fragmentado?)')
        return 1

    slots = []
    counts = []
    sem_duracao = 0
    for cam, p, cab, tam in truns:
        c = p + cab
        flags = struct.unpack_from('>I', buf, c)[0] & 0xFFFFFF
        n = struct.unpack_from('>I', buf, c + 4)[0]
        q = c + 8
        if flags & 0x000001:
            q += 4
        if flags & 0x000004:
            q += 4
        passo = 4 * ((1 if flags & 0x000100 else 0) + (1 if flags & 0x000200 else 0) +
                     (1 if flags & 0x000400 else 0) + (1 if flags & 0x000800 else 0))
        if flags & 0x000100:
            slots.extend(q + i * passo for i in range(n))
        else:
            sem_duracao += n
        counts.append(n)
    total = sum(counts)

    # ---------- 2. decidir a duracao de cada amostra ----------
    exato = True
    if esperado and total != esperado:
        exato = False
        alvo_total = round(esperado / float(fps) * ts_media)
        base = alvo_total // total
        resto = alvo_total - base * total
        durs = []
        acc = 0
        for i in range(total):
            acc += resto
            extra = 0
            if acc >= total:
                acc -= total
                extra = 1
            durs.append(base + extra)
        print('AVISO: %d amostras para %d quadros esperados (%.0f%% sobreviveu)'
              % (total, esperado, 100.0 * total / esperado))
        print('       A duracao e preservada: %.2f q/s constante em vez de %d.'
              % (total / (esperado / float(fps)), fps))
        print('       Aumente o --passo para nao perder quadro.')
    else:
        durs = [D] * total

    for off, v in zip(slots, durs):
        struct.pack_into('>I', buf, off, v)

    if sem_duracao:
        achou = False
        for cam, p, cab, tam in arvore:
            if cam[-1] != 'tfhd':
                continue
            c = p + cab
            flags = struct.unpack_from('>I', buf, c)[0] & 0xFFFFFF
            if not (flags & 0x000008):
                print('ERRO: %d amostras sem duracao e o tfhd nao tem default_sample_duration'
                      % sem_duracao)
                return 1
            q = c + 8
            if flags & 0x000001:
                q += 8
            if flags & 0x000002:
                q += 4
            struct.pack_into('>I', buf, q, durs[0])
            achou = True
        if not achou:
            print('ERRO: nao achei tfhd')
            return 1

    # ---------- 3. tfdt cumulativo ----------
    if len(tfdts) == len(truns):
        acc = 0
        pos = 0
        for i, (cam, p, cab, tam) in enumerate(tfdts):
            c = p + cab
            ver = buf[c]
            if ver == 1:
                struct.pack_into('>Q', buf, c + 4, acc)
            else:
                struct.pack_into('>I', buf, c + 4, acc)
            acc += sum(durs[pos:pos + counts[i]])
            pos += counts[i]
    else:
        print('AVISO: %d tfdt para %d trun — nao mexi no tfdt' % (len(tfdts), len(truns)))

    # ---------- 4. duracoes de nivel superior ----------
    dur_media = sum(durs)
    dur_movie = round(dur_media / ts_media * ts_movie)

    def grava(box, offs, valor):
        p, cab, tam = box
        c = p + cab
        ver = buf[c]
        off, larg = offs[1] if ver == 1 else offs[0]
        if larg == 8:
            struct.pack_into('>Q', buf, c + off, valor)
        else:
            struct.pack_into('>I', buf, c + off, valor)

    grava(mvhd, ((16, 4), (24, 8)), dur_movie)
    grava(tkhd, ((20, 4), (28, 8)), dur_movie)
    grava(mdhd, ((16, 4), (24, 8)), dur_media)

    if bruto:
        shutil.copyfile(arq, arq + '.vfr.mp4')
    open(arq, 'wb').write(bytes(buf))

    print('retimado : %s' % arq)
    print('  amostras  : %d em %d fragmento(s)' % (total, len(truns)))
    print('  timescale : movie %d | midia %d' % (ts_movie, ts_media))
    print('  duracao   : %.3f s' % (dur_media / ts_media))
    print('  taxa      : %.3f q/s constante%s'
          % (total / (dur_media / ts_media), '' if exato else '  (ajustada)'))
    return 0


if __name__ == '__main__':
    sys.exit(main())

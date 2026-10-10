# -*- coding: utf-8 -*-
"""Perfil do Chrome NOVO a cada gravacao.

   Descoberta de 18/09: reusar o mesmo --user-data-dir entre gravacoes degrada o
   render. A MESMA configuracao caiu de 16,1 para 11,5 quadros/s ao longo da
   sessao, e apagar o perfil devolveu o desempenho (11,5 -> 14,6). Como o piloto
   roda varias gravacoes seguidas, isso envenenava todas as medidas.
   Aborta SEM GRAVAR se a ancora nao casar exatamente 1 vez."""
import io, os, sys

ARQ = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '_gerar-mp4.js')

OLD = """  const perfil = path.join(os.tmpdir(), 'mp4-chrome-profile');
  fs.mkdirSync(perfil, { recursive: true });"""

NEW = """  const perfil = path.join(os.tmpdir(), 'mp4-chrome-profile');
  /* Perfil NOVO a cada gravacao. Reusar o mesmo perfil degrada o render: a mesma
     configuracao caiu de 16,1 para 11,5 quadros/s ao longo de uma sessao, e
     apagar o perfil devolveu o desempenho. */
  try { fs.rmSync(perfil, { recursive: true, force: true }); } catch (e) {}
  fs.mkdirSync(perfil, { recursive: true });"""

d = io.open(ARQ, encoding='utf-8', newline='').read()
n = d.count(OLD)
print('ancora: %d ocorrencia(s) %s' % (n, 'OK' if n == 1 else '<-- FALHOU'))
if n != 1:
    print('ABORTADO: nada foi gravado.')
    sys.exit(1)
io.open(ARQ, 'w', encoding='utf-8', newline='').write(d.replace(OLD, NEW, 1))
print('GRAVADO: %s' % ARQ)
print('  fs.rmSync(perfil...: %d' % d.replace(OLD, NEW, 1).count('fs.rmSync(perfil'))

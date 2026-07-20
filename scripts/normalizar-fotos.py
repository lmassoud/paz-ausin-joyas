#!/usr/bin/env python3
"""
Normaliza el encuadre de las fotos del catalogo: la joya queda centrada y a un
tamano parecido en todas, para que la grilla se vea ordenada.

REGLA PRINCIPAL: acercar cuando sobra fondo, NUNCA inventar fondo para alejar.
(La v1 hacia lo contrario y generaba manchones de borde estirado.)

Por foto:
  1. Detecta la joya por energia de bordes (la pieza tiene detalle, el fondo de
     estudio no).
  2. Calcula un recorte 4:5 centrado en la joya. Si la foto tiene fondo de
     sobra, acerca hasta TARGET_FILL. Si no lo tiene, se queda con lo que hay:
     nunca agranda el cuadro solo para que la joya se vea mas chica.
  3. Solo cuando la joya no cabe en 4:5 (fotos apaisadas) agrega fondo, y lo
     hace con un degradado suave sacado de la propia foto, con transicion
     difuminada. Nada de replicar el borde: eso era lo que rayaba la imagen.
  4. Guarda foto grande en fotos/ y miniatura en fotos/thumbs/.

Uso:
    python3 scripts/normalizar-fotos.py --dry-run   # solo reporta
    python3 scripts/normalizar-fotos.py             # aplica

Los originales quedan respaldados en fotos/_originales/ y SIEMPRE se reprocesa
desde ahi, asi que correrlo varias veces no degrada nada.
"""

import sys, shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter, sobel, binary_closing, binary_opening, label

# ---------------------------------------------------------------- parametros
TARGET_FILL  = 0.78   # cuanto ocupa la joya cuando hay fondo de sobra
MAX_FILL     = 0.92   # nunca dejar que la joya toque el borde
OUT_ASPECT   = 4/5
FULL_LONGSIDE, THUMB_LONGSIDE = 1600, 640
FULL_Q, THUMB_Q = 86, 78
EXCLUIR = {'og.jpg'}  # no son fotos de producto (og.jpg es la vista previa 1200x630)

# defensas del detector (heredadas de la correccion sobre v1):
BORDE_MALO_MAX_PX = 8     # franjas de color saturado pegadas al borde (defecto de exportacion)
BORDE_MALO_SAT    = 25    # saturacion media minima para considerar mala una franja
BORDE_COMP_MARGEN = 0.03  # componentes 100% dentro de este margen de UN borde se descartan

FOTOS  = Path('fotos')
THUMBS = FOTOS/'thumbs'
BACKUP = FOTOS/'_originales'


def sin_borde_malo(img):
    """Recorta franjas finas de color saturado pegadas al borde (defecto de
    exportacion, p.ej. una columna de pixeles verdes que engana al detector)."""
    a = np.asarray(img).astype(np.int16)
    sat = a.max(axis=2) - a.min(axis=2)   # saturacion aproximada por pixel
    H, W = sat.shape

    def franjas_malas(perfil):
        n = 0
        for v in perfil[:BORDE_MALO_MAX_PX]:
            if v >= BORDE_MALO_SAT: n += 1
            else: break
        return n

    filas, cols = sat.mean(axis=1), sat.mean(axis=0)
    t, b = franjas_malas(filas), franjas_malas(filas[::-1])
    l, r = franjas_malas(cols), franjas_malas(cols[::-1])
    if t or b or l or r:
        img = img.crop((l, t, W-r, H-b))
    return img


def subject_bbox(img):
    g = img.convert('L'); W0, H0 = g.size
    sc = 700/max(W0, H0)
    g = g.resize((max(1,int(W0*sc)), max(1,int(H0*sc))))
    a = gaussian_filter(np.array(g).astype(np.float32), 1.2)
    mag = gaussian_filter(np.hypot(sobel(a,0), sobel(a,1)), 6)
    m = mag > max(np.percentile(mag,97)*0.18, mag.max()*0.10)
    m = binary_opening(binary_closing(m, np.ones((9,9))), np.ones((5,5)))
    lab, n = label(m)
    if n == 0: return None
    sz = np.bincount(lab.ravel()); sz[0] = 0
    keep = np.where(sz >= sz.max()*0.10)[0]

    # descarta componentes contenidos por completo en el margen exterior de UN
    # borde (brillos del canto de la mesa, restos de franjas defectuosas): una
    # pieza real —o su cadena— siempre se interna mas en el cuadro.
    H, W = m.shape
    mg = BORDE_COMP_MARGEN
    centrales = []
    for k in keep:
        ys, xs = np.where(lab == k)
        x0, x1, y0, y1 = xs.min()/W, xs.max()/W, ys.min()/H, ys.max()/H
        if x1 <= mg or x0 >= 1-mg or y1 <= mg or y0 >= 1-mg:
            continue
        centrales.append(k)
    if centrales:
        keep = centrales

    m2 = np.isin(lab, keep)
    ys, xs = np.where(m2)
    return xs.min()/W, ys.min()/H, xs.max()/W, ys.max()/H


def plan_crop(W, H, b):
    """Devuelve (left, top, cw, ch) del recorte, posiblemente fuera de la foto."""
    x0, y0, x1, y1 = b[0]*W, b[1]*H, b[2]*W, b[3]*H
    sw, sh = x1-x0, y1-y0
    cx, cy = (x0+x1)/2, (y0+y1)/2

    deseado = max(sw/TARGET_FILL, (sh/TARGET_FILL)*OUT_ASPECT)  # lo ideal
    minimo  = max(sw/MAX_FILL,   (sh/MAX_FILL)*OUT_ASPECT)      # para que quepa
    cabe    = min(W, H*OUT_ASPECT)                              # sin salirse

    cw = max(min(deseado, max(cabe, minimo)), minimo)
    ch = cw/OUT_ASPECT
    # centrar en la joya, pero sin salirse mas de lo necesario
    l = cx - cw/2
    t = cy - ch/2
    if cw <= W: l = min(max(l, 0), W-cw)
    else:       l = (W-cw)/2
    if ch <= H: t = min(max(t, 0), H-ch)
    else:       t = (H-ch)/2
    return l, t, cw, ch


def render(img, l, t, cw, ch):
    """Recorta; si el recorte se sale, rellena con fondo suave de la propia foto."""
    W, H = img.size
    l_i, t_i, cw_i, ch_i = int(round(l)), int(round(t)), int(round(cw)), int(round(ch))

    if l_i >= 0 and t_i >= 0 and l_i+cw_i <= W and t_i+ch_i <= H:
        return img.crop((l_i, t_i, l_i+cw_i, t_i+ch_i))   # cabe entero: sin invento

    # fondo suave: version muy desenfocada de la foto, estirada al cuadro nuevo.
    # Al no tener detalle, estirarla no produce rayas ni manchones.
    base = img.copy().filter(ImageFilter.GaussianBlur(max(W, H)*0.06))
    canvas = base.resize((cw_i, ch_i), Image.LANCZOS)

    # pegar la foto real encima con los bordes difuminados
    px, py = -l_i, -t_i
    mask = Image.new('L', img.size, 255)
    feather = int(max(W, H)*0.03)
    if feather > 1:
        m = np.array(mask).astype(np.float32)
        ramp = np.linspace(0, 255, feather)
        m[:feather, :] = np.minimum(m[:feather, :], ramp[:, None])
        m[-feather:, :] = np.minimum(m[-feather:, :], ramp[::-1][:, None])
        m[:, :feather] = np.minimum(m[:, :feather], ramp[None, :])
        m[:, -feather:] = np.minimum(m[:, -feather:], ramp[::-1][None, :])
        mask = Image.fromarray(m.astype(np.uint8))
    canvas.paste(img, (px, py), mask)
    return canvas


def resize_long(img, longside):
    W, H = img.size
    if max(W, H) <= longside: return img
    sc = longside/max(W, H)
    return img.resize((int(W*sc), int(H*sc)), Image.LANCZOS)


def main():
    dry = '--dry-run' in sys.argv
    if not FOTOS.is_dir():
        sys.exit('Corre esto desde la raiz del repo (no encuentro fotos/).')
    THUMBS.mkdir(exist_ok=True)
    if not dry: BACKUP.mkdir(exist_ok=True)

    avisos = []
    ok = 0
    for p in sorted(FOTOS.glob('*.jpg')):
        if p.name in EXCLUIR:
            print(f'  - {p.name}: excluida (no es foto de producto)')
            continue
        src = BACKUP/p.name if (BACKUP/p.name).exists() else p
        img = sin_borde_malo(Image.open(src).convert('RGB'))
        b = subject_bbox(img)
        if b is None:
            print(f'  ! {p.name}: no detecte la pieza, la dejo igual'); continue

        W, H = img.size
        l, t, cw, ch = plan_crop(W, H, b)
        invent = max(0, (cw-W)/cw) + max(0, (ch-H)/ch)
        if invent > 0.15:
            avisos.append((p.name, invent))

        if dry:
            print(f'  · {p.name}: {W}x{H} -> {int(cw)}x{int(ch)}' + (f'  (fondo agregado {invent*100:.0f}%)' if invent>0.02 else ''))
            ok += 1; continue

        out = render(img, l, t, cw, ch)
        if not (BACKUP/p.name).exists(): shutil.copy2(p, BACKUP/p.name)
        resize_long(out, FULL_LONGSIDE).save(p, 'JPEG', quality=FULL_Q, optimize=True)
        resize_long(out, THUMB_LONGSIDE).save(THUMBS/p.name, 'JPEG', quality=THUMB_Q, optimize=True)
        ok += 1

    print(f'\nListo: {ok} fotos.')
    if avisos:
        print('\nOJO — a estas fotos hubo que agregarles bastante fondo porque la')
        print('pieza no cabe en formato vertical 4:5. Revisalas y considera')
        print('reemplazarlas por una toma vertical:')
        for n, v in sorted(avisos, key=lambda x: -x[1]):
            print(f'   {n:<40} {v*100:.0f}% de fondo agregado')


if __name__ == '__main__':
    main()

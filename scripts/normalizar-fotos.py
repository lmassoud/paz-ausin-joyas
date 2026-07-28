#!/usr/bin/env python3
"""
Normaliza el encuadre de las fotos del catalogo: la joya queda centrada y
SIEMPRE del mismo porte, para que la grilla se vea pareja.

Referencia de tamano: la portada de la Pulsera Grumet (fotos/pulsera-grumet-01.jpg),
donde la pieza ocupa el 71,5% del ancho del cuadro. Ese es el valor de OBJETIVO.

Por foto:
  1. Detecta la joya (scripts/detector_joya.py — por rango dinamico local, no por
     gradiente: ver ahi el porque).
  2. Calcula el recorte 4:5 que deja la pieza centrada y ocupando OBJETIVO de la
     caja. La dimension que manda es la que "toca" primero: una pulsera ancha
     toca los costados, un anillo alto toca arriba y abajo.
  3. Si para alejarse hace falta salir de la foto, EXTIENDE el fondo: ajusta una
     superficie suave al fondo real de esa misma foto y la continua hacia afuera,
     con el mismo grano. No replica el borde (eso rayaba la imagen en la v4) ni
     estira una version desenfocada (v5, que dejaba manchones).
  4. Nunca extiende mas de MAX_RELLENO: pasado ese punto se queda con lo que hay
     y la pieza sale un poco mas grande, que es preferible a inventar medio cuadro.
  5. Guarda foto grande en fotos/ y miniatura en fotos/thumbs/.

Uso:
    python3 scripts/normalizar-fotos.py --dry-run   # solo reporta
    python3 scripts/normalizar-fotos.py             # aplica
    python3 scripts/normalizar-fotos.py --solo anillo-sello-01.jpg

Los originales quedan respaldados en fotos/_originales/ y SIEMPRE se reprocesa
desde ahi, asi que correrlo varias veces no degrada nada.
"""

import sys
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import binary_dilation, gaussian_filter, zoom

sys.path.insert(0, str(Path(__file__).resolve().parent))
from detector_joya import detectar, sin_borde_malo

# ---------------------------------------------------------------- parametros
OBJETIVO      = 0.715  # cuanto ocupa la pieza en la caja 4:5 (= pulsera-grumet-01)
MAX_FILL      = 0.92   # tope: nunca dejar que la pieza toque el borde
MAX_RELLENO   = 0.26   # tope de fondo agregado (suma de los dos ejes)
OUT_ASPECT    = 4 / 5
FULL_LONGSIDE, THUMB_LONGSIDE = 1600, 640
FULL_Q, THUMB_Q = 86, 78
MAX_AGRANDE   = 2.0    # tope para agrandar una foto que quedo chica al recortar
EXCLUIR = {'og.jpg'}   # og.jpg es la vista previa 1200x630, no es foto de producto

# Si la caja completa no es mucho mayor que el nucleo, es que no hay cadena y
# conviene exigir que la pieza entera quepa. Si es mucho mayor, hay cadena y se
# la deja salir del cuadro a proposito.
FACTOR_CADENA = 1.6

# Cajas puestas a mano, en fracciones del cuadro (x0, y0, x1, y1). Son las fotos
# donde el detector automatico se equivoca; en vez de aflojar los umbrales para
# todas —lo que empeora las 148 que estan bien— se le dice donde esta la pieza
# solo en estas. Medidas sobre el original, despues de sin_borde_malo().
CAJAS_A_MANO = {
    # El primer plano de la mesa esta enfocado y tiene tanta textura como el
    # metal: el detector lo sumaba al anillo y la pieza salia al 35%.
    'anillo-sello-01.jpg':      (0.36, 0.37, 0.61, 0.60),
    # El degradado del fondo desenfocado se le pega por debajo al anillo.
    'anillo-aguamarina-01.jpg': (0.27, 0.34, 0.73, 0.62),
}

FOTOS  = Path('fotos')
THUMBS = FOTOS / 'thumbs'
BACKUP = FOTOS / '_originales'


# ------------------------------------------------------------------ encuadre
def _relleno(cw, ch, W, H):
    """Fraccion de lienzo que habria que inventar con este recorte."""
    return max(0.0, (cw - W) / cw) + max(0.0, (ch - H) / ch)


def _acomodar(W, H, cw, cx, cy, minimo):
    """Aplica los topes (relleno maximo, tamano minimo) y centra el recorte."""
    if _relleno(cw, cw / OUT_ASPECT, W, H) > MAX_RELLENO:
        lo, hi = min(W, H * OUT_ASPECT), cw
        for _ in range(40):
            mid = (lo + hi) / 2
            if _relleno(mid, mid / OUT_ASPECT, W, H) > MAX_RELLENO:
                hi = mid
            else:
                lo = mid
        cw = lo
    cw = max(cw, minimo)
    ch = cw / OUT_ASPECT

    # centrar en la pieza; si el recorte cabe, se corre lo justo para no salirse
    l, t = cx - cw / 2, cy - ch / 2
    if cw <= W:
        l = min(max(l, 0), W - cw)
    if ch <= H:
        t = min(max(t, 0), H - ch)
    return l, t, cw, ch


def plan_crop(W, H, nucleo, full):
    """Devuelve (left, top, cw, ch, minimo) — el recorte puede caer fuera."""
    nx0, ny0, nx1, ny1 = nucleo[0] * W, nucleo[1] * H, nucleo[2] * W, nucleo[3] * H
    nw, nh = nx1 - nx0, ny1 - ny0
    cx, cy = (nx0 + nx1) / 2, (ny0 + ny1) / 2

    deseado = max(nw / OBJETIVO, (nh / OBJETIVO) * OUT_ASPECT)

    # minimo para que la pieza no toque el borde
    minimo = max(nw / MAX_FILL, (nh / MAX_FILL) * OUT_ASPECT)
    fx0, fy0, fx1, fy1 = full[0] * W, full[1] * H, full[2] * W, full[3] * H
    fw, fh = fx1 - fx0, fy1 - fy0
    if fw * fh <= nw * nh * FACTOR_CADENA:
        # sin cadena: la pieza entera tiene que caber
        minimo = max(minimo, fw / MAX_FILL, (fh / MAX_FILL) * OUT_ASPECT)

    l, t, cw, ch = _acomodar(W, H, deseado, cx, cy, minimo)
    return l, t, cw, ch, minimo


def encuadrar(img, res, pasadas=4, fijo=False):
    """Encuadra midiendo el RESULTADO, no solo la entrada.

    El detector no da exactamente la misma caja antes y despues de recortar (al
    cambiar la proporcion de fondo cambian sus estadisticas), y esa diferencia
    era lo que dejaba unas piezas visiblemente mas chicas que otras aun teniendo
    todas el mismo objetivo. Aca se renderiza, se vuelve a medir sobre lo
    renderizado y se corrige el zoom hasta que la pieza mide el objetivo EN LA
    FOTO FINAL, que es lo unico que se ve.
    """
    W, H = img.size
    l, t, cw, ch, minimo = plan_crop(W, H, res['nucleo'], res['full'])
    out = render(img, res['mascara'], l, t, cw, ch)
    mejor = (out, l, t, cw, ch, None)
    if fijo:
        # con la caja puesta a mano no hay nada que corregir: volver a medir
        # solo la arrastraria de vuelta al error que estamos evitando
        nx = (res['nucleo'][2] - res['nucleo'][0]) * W
        ny = (res['nucleo'][3] - res['nucleo'][1]) * H
        return out, max(nx / cw, ny / ch)

    for _ in range(pasadas):
        r2 = detectar(out)
        if r2 is None:
            break
        n = r2['nucleo']
        fill = max(n[2] - n[0], n[3] - n[1])
        if mejor[5] is None or abs(fill - OBJETIVO) < abs(mejor[5] - OBJETIVO):
            mejor = (out, l, t, cw, ch, fill)
        if abs(fill - OBJETIVO) <= 0.015:
            break
        # el centro de la pieza en la salida, llevado a coordenadas del original
        cx = l + (n[0] + n[2]) / 2 * cw
        cy = t + (n[1] + n[3]) / 2 * ch
        nuevo = cw * (fill / OBJETIVO)
        l, t, cw, ch = _acomodar(W, H, nuevo, cx, cy, minimo)
        out = render(img, res['mascara'], l, t, cw, ch)

    return mejor[0], mejor[5]


# --------------------------------------------------------- extension de fondo
def _fondo_limpio(a, sub):
    """Pixeles de fondo de estudio: ni la pieza, ni la piel de la mano.

    En las fotos puestas (anillo en el dedo, pulsera en la muneca) la piel ocupa
    medio cuadro y si entra al ajuste tine el fondo inventado de rosado. Se la
    saca por distancia al color mediano, con dos pasadas de recorte robusto.
    """
    fondo = ~sub
    for _ in range(2):
        if fondo.sum() < 200:
            break
        med = np.median(a[fondo], axis=0)
        d = np.linalg.norm(a - med, axis=-1)
        corte = np.percentile(d[fondo], 75) * 1.8 + 6.0
        nuevo = fondo & (d < corte)
        if nuevo.sum() < 200:
            break
        fondo = nuevo
    return fondo


def _extension_armonica(conocido, valores, iteraciones=260):
    """Rellena lo desconocido con la continuacion mas suave del borde conocido.

    Es una extension armonica (promediar repetidamente dejando fijo lo conocido).
    Dos propiedades que aqui importan: empalma exacto con el borde real —no queda
    el rectangulo de la foto marcado, que es lo que pasaba ajustando un plano— y
    todo valor nuevo queda dentro del rango de los valores reales, asi que no
    puede aparecer un color que no estuviera en la foto.
    """
    x = valores.copy()
    x[~conocido] = valores[conocido].mean(axis=0) if conocido.any() else 0.0
    for _ in range(iteraciones):
        s = gaussian_filter(x, (1.0, 1.0, 0))
        x[~conocido] = s[~conocido]
    return x


def extender_fondo(img, mascara_sub, l, t, cw, ch):
    """Lienzo cw x ch con la foto pegada y el fondo continuado hacia afuera.

    El fondo nuevo se calcula difundiendo el fondo real de la propia foto hacia
    afuera (extension armonica), a baja resolucion —es una superficie suave, no
    necesita detalle— y despues se le devuelve el grano para que no quede una
    zona plastica. La pieza y la piel se marcan como desconocidas para que no
    tinan la extension: en las fotos puestas la piel ocupa medio cuadro y si
    entraba al modelo el fondo inventado salia rosado.
    """
    a = np.asarray(img).astype(np.float32)
    H, W, _ = a.shape

    sub = zoom(mascara_sub.astype(np.float32),
               (H / mascara_sub.shape[0], W / mascara_sub.shape[1]), order=1) > 0.4
    sub = binary_dilation(sub, np.ones((9, 9)))
    fondo_px = _fondo_limpio(a, sub)
    if fondo_px.sum() < 200:
        fondo_px = ~sub

    cw_i, ch_i = int(round(cw)), int(round(ch))
    l_i, t_i = int(round(l)), int(round(t))

    # --- resolver la extension en chico
    esc = min(1.0, 190 / max(cw_i, ch_i))
    lw, lh = max(8, int(cw_i * esc)), max(8, int(ch_i * esc))
    chico = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize(
        (max(1, int(W * esc)), max(1, int(H * esc))), Image.LANCZOS)
    fondo_chico = np.asarray(Image.fromarray((fondo_px * 255).astype(np.uint8)).resize(
        chico.size, Image.BILINEAR)) > 200

    conocido = np.zeros((lh, lw), bool)
    valores = np.zeros((lh, lw, 3), np.float32)
    ox, oy = int(round(-l_i * esc)), int(round(-t_i * esc))
    ax0, ay0 = max(0, ox), max(0, oy)
    ax1, ay1 = min(lw, ox + chico.width), min(lh, oy + chico.height)
    if ax1 > ax0 and ay1 > ay0:
        recorte = np.asarray(chico).astype(np.float32)[ay0 - oy:ay1 - oy, ax0 - ox:ax1 - ox]
        mrec = fondo_chico[ay0 - oy:ay1 - oy, ax0 - ox:ax1 - ox]
        valores[ay0:ay1, ax0:ax1] = recorte
        conocido[ay0:ay1, ax0:ax1] = mrec
    if not conocido.any():
        conocido[:] = True
        valores[:] = np.median(a[fondo_px], axis=0)

    ext = _extension_armonica(conocido, valores)
    lienzo = np.asarray(Image.fromarray(np.clip(ext, 0, 255).astype(np.uint8)).resize(
        (cw_i, ch_i), Image.BICUBIC)).astype(np.float32)

    # --- grano, para que el fondo nuevo no se vea plastico
    lum = a.mean(-1)
    grano = float(np.std((lum - gaussian_filter(lum, 3))[fondo_px]))
    if grano > 0.05:
        ruido = np.random.default_rng(0).normal(0, grano, (ch_i, cw_i)).astype(np.float32)
        lienzo += gaussian_filter(ruido, 0.6)[..., None]

    # --- pegar la foto real, difuminando solo los bordes que se extendieron
    lienzo_img = Image.fromarray(np.clip(lienzo, 0, 255).astype(np.uint8))
    pluma = max(3, int(min(W, H) * 0.020))
    alpha = np.full((H, W), 255.0, np.float32)
    rampa = np.linspace(0, 255, pluma)
    if l_i < 0:
        alpha[:, :pluma] = np.minimum(alpha[:, :pluma], rampa[None, :])
    if t_i < 0:
        alpha[:pluma, :] = np.minimum(alpha[:pluma, :], rampa[:, None])
    if l_i + cw_i > W:
        alpha[:, -pluma:] = np.minimum(alpha[:, -pluma:], rampa[::-1][None, :])
    if t_i + ch_i > H:
        alpha[-pluma:, :] = np.minimum(alpha[-pluma:, :], rampa[::-1][:, None])
    lienzo_img.paste(img, (-l_i, -t_i), Image.fromarray(alpha.astype(np.uint8)))
    return lienzo_img


def render(img, mascara_sub, l, t, cw, ch):
    W, H = img.size
    l_i, t_i, cw_i, ch_i = int(round(l)), int(round(t)), int(round(cw)), int(round(ch))
    if l_i >= 0 and t_i >= 0 and l_i + cw_i <= W and t_i + ch_i <= H:
        return img.crop((l_i, t_i, l_i + cw_i, t_i + ch_i))   # cabe entero
    return extender_fondo(img, mascara_sub, l_i, t_i, cw_i, ch_i)


def resize_long(img, longside):
    """Lleva la foto a `longside`, agrandando si hace falta.

    Igualar el tamano de la pieza obliga a recortar, y en las fotos que venian
    chicas eso dejaba archivos de 300-400 px que en el celular se veian blandos.
    Se permite agrandar hasta MAX_AGRANDE (mas que eso ya es puro invento) con
    Lanczos y un enfoque suave, que se ve mejor que dejar que el navegador
    estire un archivo diminuto.
    """
    W, H = img.size
    actual = max(W, H)
    objetivo = min(longside, actual * MAX_AGRANDE)
    if abs(objetivo - actual) < 1:
        return img
    sc = objetivo / actual
    out = img.resize((max(1, round(W * sc)), max(1, round(H * sc))), Image.LANCZOS)
    if sc > 1.05:
        out = out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=3))
    return out


# ---------------------------------------------------------------------- main
def main():
    dry = '--dry-run' in sys.argv
    solo = None
    if '--solo' in sys.argv:
        solo = set(sys.argv[sys.argv.index('--solo') + 1].split(','))

    if not FOTOS.is_dir():
        sys.exit('Corre esto desde la raiz del repo (no encuentro fotos/).')
    THUMBS.mkdir(exist_ok=True)
    if not dry:
        BACKUP.mkdir(exist_ok=True)

    avisos, fills, ok = [], [], 0
    for p in sorted(FOTOS.glob('*.jpg')):
        if p.name in EXCLUIR:
            print(f'  - {p.name}: excluida (no es foto de producto)')
            continue
        if solo and p.name not in solo:
            continue

        src = BACKUP / p.name if (BACKUP / p.name).exists() else p
        img = sin_borde_malo(Image.open(src).convert('RGB'))
        res = detectar(img)
        if res is None:
            print(f'  ! {p.name}: no detecte la pieza, la dejo igual')
            continue

        a_mano = CAJAS_A_MANO.get(p.name)
        if a_mano:
            res['nucleo'] = res['full'] = a_mano

        W, H = img.size
        l, t, cw, ch, _ = plan_crop(W, H, res['nucleo'], res['full'])
        rell = _relleno(cw, ch, W, H)
        if rell > 0.02:
            avisos.append((p.name, rell))

        if dry:
            nw = (res['nucleo'][2] - res['nucleo'][0]) * W
            nh = (res['nucleo'][3] - res['nucleo'][1]) * H
            fills.append(max(nw / cw, nh / ch))
            print(f'  · {p.name}: {W}x{H} -> {int(cw)}x{int(ch)}'
                  + (f'  fondo agregado {rell*100:.0f}%' if rell > 0.02 else ''))
            ok += 1
            continue

        out, fill = encuadrar(img, res, fijo=bool(a_mano))
        fills.append(fill if fill is not None else OBJETIVO)
        if fill is not None and abs(fill - OBJETIVO) > 0.05:
            print(f'  ~ {p.name}: la pieza quedo al {fill:.0%} (objetivo {OBJETIVO:.0%})')
        if not (BACKUP / p.name).exists():
            shutil.copy2(p, BACKUP / p.name)
        resize_long(out, FULL_LONGSIDE).save(p, 'JPEG', quality=FULL_Q, optimize=True)
        resize_long(out, THUMB_LONGSIDE).save(THUMBS / p.name, 'JPEG',
                                              quality=THUMB_Q, optimize=True)
        ok += 1

    print(f'\nListo: {ok} fotos.')
    if fills:
        f = np.array(fills)
        print(f'Tamano de la pieza en el cuadro: min={f.min():.0%} '
              f'mediana={np.median(f):.0%} max={f.max():.0%}  (objetivo {OBJETIVO:.0%})')
        print(f'Fuera del objetivo por mas de 3 puntos: '
              f'{int((np.abs(f - OBJETIVO) > 0.03).sum())} de {len(f)}')
    if avisos:
        print(f'\nCon fondo agregado ({len(avisos)}):')
        for n, v in sorted(avisos, key=lambda x: -x[1])[:20]:
            print(f'   {n:<44} {v*100:.0f}%')


if __name__ == '__main__':
    main()

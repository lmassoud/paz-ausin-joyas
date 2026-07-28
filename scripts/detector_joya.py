#!/usr/bin/env python3
"""Detector de joya sobre fondo de estudio.

Señal principal: RANGO DINAMICO LOCAL (max - min en una ventana chica).
Medido sobre las fotos de este catalogo, el fondo del mantel queda en 5-15
(de 255) y la joya llega a 130-220: una separacion de 10 a 20 veces. Las bandas
de tono, el degradado y el desenfoque del fondo —que enganaban a los detectores
por gradiente de las versiones anteriores— aqui no aparecen, porque son
variaciones lentas: dentro de una ventana chica casi no cambian.

Se le suma el rango de croma, para las piedras de color que tienen poco
contraste de luminancia contra el gris pero saltan a la vista.

La caja NO se saca del contorno binario sino de la distribucion de energia.
Motivo medido: la mascara siempre arrastra algo pegado a la pieza —tipicamente
la franja del mantel que quedo enfocada y si tiene textura real— y eso disparaba
el ancho de la caja al cuadro completo. Esas colas aportan poquisima energia
comparadas con el metal, asi que recortar por percentil de energia las deja
fuera solas, sin un umbral que haya que calibrar foto por foto.

Devuelve, en coordenadas 0..1:
  nucleo — el cuerpo de la pieza (con lo que se encuadra)
  full   — la pieza entera, cadena incluida
"""
import numpy as np
from PIL import Image
from scipy.ndimage import (gaussian_filter, maximum_filter, minimum_filter,
                           binary_closing, binary_fill_holes, label,
                           binary_dilation, binary_erosion, binary_propagation)

WORK = 640           # lado mayor al que se analiza (no la salida)
BORDE_MALO_MAX_PX = 8
BORDE_MALO_SAT = 25

VENTANA    = 0.020   # ventana del rango local, fraccion del lado menor
ALTO_FONDO = 5.0     # umbral alto = nivel de fondo x esto
ALTO_PICO  = 0.28    # ...o esta fraccion del pico, lo que sea mayor
BAJO_FONDO = 2.2     # hasta donde se deja crecer por histeresis
BAJO_PICO  = 0.08
COMP_MIN   = 0.02    # componentes menores a esto del mayor se descartan
COMP_PICO  = 0.35    # un componente es pieza si su pico llega a esto del global
                     # (una sombra difusa nunca lo alcanza; un segundo aro si)
ENERGIA_EXP    = 2.0    # la energia se eleva a esto: la pieza pesa mas que la cola
CORTE_NUCLEO   = 0.02   # 2%-98% de la energia  -> cuerpo de la pieza
CORTE_COMPLETO = 0.002  # 0.2%-99.8%            -> pieza entera


def sin_borde_malo(img):
    """Recorta franjas finas de color saturado pegadas al borde (defecto de
    exportacion: p.ej. una columna de pixeles verdes que engana al detector)."""
    a = np.asarray(img).astype(np.int16)
    sat = a.max(axis=2) - a.min(axis=2)
    H, W = sat.shape

    def franjas(perfil):
        n = 0
        for v in perfil[:BORDE_MALO_MAX_PX]:
            if v >= BORDE_MALO_SAT:
                n += 1
            else:
                break
        return n

    filas, cols = sat.mean(axis=1), sat.mean(axis=0)
    t, b = franjas(filas), franjas(filas[::-1])
    l, r = franjas(cols), franjas(cols[::-1])
    if t or b or l or r:
        img = img.crop((l, t, W - r, H - b))
    return img


def _rango(x, k):
    return maximum_filter(x, k) - minimum_filter(x, k)


def mapa_rango(img):
    """Devuelve (imagen reducida, mapa de rango local)."""
    W0, H0 = img.size
    sc = WORK / max(W0, H0)
    small = img.resize((max(16, int(W0 * sc)), max(16, int(H0 * sc))), Image.LANCZOS)
    a = np.asarray(small).astype(np.float32)
    lado = min(a.shape[:2])
    k = max(3, int(lado * VENTANA))
    gray = gaussian_filter(a.mean(-1), 1.0)
    croma = gaussian_filter(np.linalg.norm(a - a.mean(-1)[..., None], axis=-1), 1.0)
    Rt = np.maximum(_rango(gray, k), _rango(croma, k) * 1.5)
    return small, gaussian_filter(Rt, 1.0)


def detectar(img, debug=False):
    small, Rt = mapa_rango(img)
    H, W = Rt.shape
    lado = min(H, W)

    # nivel de fondo: mediana del anillo exterior del cuadro
    m = max(2, int(lado * 0.05))
    ring = np.zeros((H, W), bool)
    ring[:m, :] = ring[-m:, :] = ring[:, :m] = ring[:, -m:] = True
    fondo = float(np.median(Rt[ring]))
    pico = float(np.percentile(Rt, 99.5))
    if pico <= 1e-6:
        return None

    thr_alto = max(fondo * ALTO_FONDO, ALTO_PICO * pico, 20.0)
    thr_bajo = max(fondo * BAJO_FONDO, BAJO_PICO * pico, 9.0)

    alto = Rt > thr_alto
    if not alto.any():
        alto = Rt > max(thr_bajo, 0.5 * pico)
        if not alto.any():
            return None
    mask = binary_propagation(alto, mask=Rt > thr_bajo)

    r = max(2, int(lado * 0.014))
    mask = binary_closing(mask, np.ones((2 * r + 1, 2 * r + 1)))
    mask = binary_fill_holes(mask)
    mask = binary_erosion(mask, np.ones((3, 3)))
    mask = binary_dilation(mask, np.ones((3, 3)))

    lab, n = label(mask)
    if n == 0:
        return None
    sz = np.bincount(lab.ravel())
    sz[0] = 0
    if sz.max() == 0:
        return None

    # Un componente es parte de la pieza si su rango PICO se acerca al global:
    # el metal y las piedras llegan; una sombra difusa o un reflejo del mantel,
    # por grande que sea, se queda muy abajo.
    pico_global = float(Rt.max())
    keep = []
    for k in np.where(sz >= sz.max() * COMP_MIN)[0]:
        comp = lab == k
        if float(Rt[comp].max()) < COMP_PICO * pico_global:
            continue
        ys, xs = np.where(comp)
        x0, x1 = xs.min() / W, xs.max() / W
        y0, y1 = ys.min() / H, ys.max() / H
        if x1 <= 0.02 or x0 >= 0.98 or y1 <= 0.02 or y0 >= 0.98:
            continue     # vive pegado a un borde: canto de la mesa, reflejo
        keep.append(k)
    if not keep:
        keep = [int(sz.argmax())]
    full = np.isin(lab, keep)

    peso = (Rt * full) ** ENERGIA_EXP
    if peso.sum() <= 0:
        return None

    def _rango_energia(perfil, corte):
        c = np.cumsum(perfil)
        c /= c[-1]
        a = int(np.searchsorted(c, corte))
        b = int(np.searchsorted(c, 1 - corte))
        n = len(perfil)
        return max(0, min(a, n - 1)), max(1, min(b + 1, n))

    def caja(corte):
        x0, x1 = _rango_energia(peso.sum(axis=0), corte)
        y0, y1 = _rango_energia(peso.sum(axis=1), corte)
        return (x0 / W, y0 / H, x1 / W, y1 / H)

    out = dict(nucleo=caja(CORTE_NUCLEO), full=caja(CORTE_COMPLETO),
               mascara=full, escala=(W, H),
               area=float(full.sum()) / (H * W), fondo=fondo, pico=pico)
    if debug:
        out.update(small=small, Rt=Rt, peso=peso)
    return out

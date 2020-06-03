import pygame as pg
from PIL import ImageFont

pg.init()

_FONT_SIZING_CACHE = {
    # fontname: (height factor, height offset)
}


def font_sizing(fontname):
    """Return factor and offset to compute text size in pixels from front size

    About:
        When loading a font one must precise a size that does not match the
        actual height in pixels the text will have. The difference depends on
        the font.

    Return:
        (2-float-tuple): factor and offset of the given font so that
            height (in pixels) = factor * size (of font) + offset
    """
    try:
        return _FONT_SIZING_CACHE[fontname]
    except KeyError:
        pass

    s1, s2 = 100, 200  # I tried a few and those give the best precision
    args = ("Text", True, (0, 0, 0))
    h1 = pg.font.SysFont(fontname, size=s1).render(*args).get_size()[1]
    h2 = pg.font.SysFont(fontname, size=s2).render(*args).get_size()[1]
    factor = (h2 - h1) / (s2 - s1)
    offset = (h1 * s2 - s1 * h2) / (s2 - s1)

    params = (factor, offset)
    _FONT_SIZING_CACHE[fontname] = params
    return params


def font_size(fontname, height):
    """Return font size to use in order to get text with height in pixels"""
    factor, offset = font_sizing(fontname)
    return int(round((height - offset) / factor))



def get_font(fontname, height):
    """Return pillow font image"""
    fontname = 'arial' if fontname is None else fontname
    size = font_size(fontname, height)
    return ImageFont.truetype(fontname, size)

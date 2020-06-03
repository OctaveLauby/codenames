"""

https://www.rapidtables.com/web/color/RGB_Color.html
"""
from olutils import Param


COLOR_TUPLES = {
    # Red-ish
    'maroon': (128, 0, 0), 'dark_red': (139, 0, 0),
    'brown': (165, 42, 42), 'firebrick': (178, 34, 34),
    'crimson': (220, 20, 60), 'red': (255, 0, 0),
    'tomato': (255, 99, 71), 'coral': (255, 127, 80),
    'light_coral': (240, 128, 128), 'dark_salmon': (233, 150, 122),
    'salmon': (250, 128, 114), 'light_salmon': (255, 160, 122),
    'orange_red': (255, 69, 0), 'dark_orange': (255, 140, 0),
    'orange': (255, 165, 0),

    # Yellow-ish
    'gold': (255, 215, 0), 'dark_golden_rod': (184, 134, 11),
    'golden_rod': (218, 165, 32), 'pale_golden_rod': (238, 232, 170),
    'dark_khaki': (189, 183, 107), 'khaki': (240, 230, 140),
    'olive': (128, 128, 0), 'yellow': (255, 255, 0),

    # Green-ish
    'yellow_green': (154, 205, 50), 'dark_olive_green': (85, 107, 47),
    'olive_drab': (107, 142, 35), 'lawn_green': (124, 252, 0),
    'chart_reuse': (127, 255, 0), 'green_yellow': (173, 255, 47),
    'dark_green': (0, 100, 0), 'green': (0, 128, 0),
    'forest_green': (34, 139, 34), 'lime': (0, 255, 0),
    'lime_green': (50, 205, 50), 'light_green': (144, 238, 144),
    'pale_green': (152, 251, 152), 'dark_sea_green': (143, 188, 143),
    'medium_spring_green': (0, 250, 154), 'spring_green': (0, 255, 127),
    'sea_green': (46, 139, 87), 'medium_aqua_marine': (102, 205, 170),
    'medium_sea_green': (60, 179, 113),

    # Blue-ish
    'light_sea_green': (32, 178, 170), 'dark_slate_gray': (47, 79, 79),
    'teal': (0, 128, 128), 'dark_cyan': (0, 139, 139),
    'aqua': (0, 255, 255), 'cyan': (0, 255, 255),
    'light_cyan': (224, 255, 255), 'dark_turquoise': (0, 206, 209),
    'turquoise': (64, 224, 208), 'medium_turquoise': (72, 209, 204),
    'pale_turquoise': (175, 238, 238), 'aqua_marine': (127, 255, 212),
    'powder_blue': (176, 224, 230), 'cadet_blue': (95, 158, 160),
    'steel_blue': (70, 130, 180), 'corn_flower_blue': (100, 149, 237),
    'deep_sky_blue': (0, 191, 255), 'dodger_blue': (30, 144, 255),
    'light_blue': (173, 216, 230), 'sky_blue': (135, 206, 235),
    'light_sky_blue': (135, 206, 250), 'midnight_blue': (25, 25, 112),
    'navy': (0, 0, 128), 'dark_blue': (0, 0, 139),
    'medium_blue': (0, 0, 205), 'blue': (0, 0, 255),
    'royal_blue': (65, 105, 225),

    # Violet-ish
    'blue_violet': (138, 43, 226), 'indigo': (75, 0, 130),
    'dark_slate_blue': (72, 61, 139), 'slate_blue': (106, 90, 205),
    'medium_slate_blue': (123, 104, 238), 'medium_purple': (147, 112, 219),
    'dark_magenta': (139, 0, 139), 'dark_violet': (148, 0, 211),
    'dark_orchid': (153, 50, 204), 'medium_orchid': (186, 85, 211),
    'purple': (128, 0, 128), 'thistle': (216, 191, 216),
    'plum': (221, 160, 221), 'violet': (238, 130, 238),
    'fuchsia': (255, 0, 255), 'orchid': (218, 112, 214),
    'medium_violet_red': (199, 21, 133), 'pale_violet_red': (219, 112, 147),
    'deep_pink': (255, 20, 147), 'hot_pink': (255, 105, 180),
    'light_pink': (255, 182, 193), 'pink': (255, 192, 203),
    'antique_white': (250, 235, 215), 'magenta': (255, 0, 255),

    # Brown-ish
    'beige': (245, 245, 220), 'bisque': (255, 228, 196),
    'blanched_almond': (255, 235, 205),
    'wheat': (245, 222, 179), 'corn_silk': (255, 248, 220),
    'lemon_chiffon': (255, 250, 205), 'light_golden_rod_yellow': (250, 250, 210),
    'light_yellow': (255, 255, 224), 'saddle_brown': (139, 69, 19),
    'sienna': (160, 82, 45), 'chocolate': (210, 105, 30),
    'peru': (205, 133, 63), 'sandy_brown': (244, 164, 96),
    'burly_wood': (222, 184, 135), 'tan': (210, 180, 140),
    'rosy_brown': (188, 143, 143), 'moccasin': (255, 228, 181),
    'navajo_white': (255, 222, 173), 'peach_puff': (255, 218, 185),
    'misty_rose': (255, 228, 225), 'lavender_blush': (255, 240, 245),
    'linen': (250, 240, 230), 'old_lace': (253, 245, 230),
    'papaya_whip': (255, 239, 213), 'sea_shell': (255, 245, 238),
    'mint_cream': (245, 255, 250),

    # Gray-ish
    'slate_gray': (112, 128, 144), 'light_slate_gray': (119, 136, 153),
    'light_steel_blue': (176, 196, 222), 'lavender': (230, 230, 250),
    'floral_white': (255, 250, 240), 'alice_blue': (240, 248, 255),
    'ghost_white': (248, 248, 255), 'honeydew': (240, 255, 240),
    'ivory': (255, 255, 240), 'azure': (240, 255, 255),
    'snow': (255, 250, 250), 'black': (0, 0, 0),
    'dim_gray': (105, 105, 105), 'gray': (128, 128, 128),
    'dark_gray': (169, 169, 169), 'silver': (192, 192, 192),
    'light_gray': (211, 211, 211), 'gainsboro': (220, 220, 220),
    'white_smoke': (245, 245, 245),
    'white': (255, 255, 255),
}
COLORS = {}  # Defined below


def cut_in(component):
    """Truncate component so it fits b/w 0 and 255"""
    return  max(0, min(component, 255))


class Color(tuple):
    """Class to define and manage colors"""

    def __new__(cls, r, g, b):
        """Return new color"""
        for comp in (r, g, b):
            if not 0 <= comp < 256:
                raise ValueError("Color component must be b/w 0 and 255")
        return tuple.__new__(cls, (r, g, b))

    @property
    def r(self):
        """Red component of color"""
        return self[0]

    @property
    def g(self):
        """Green component of color"""
        return self[1]

    @property
    def b(self):
        """Blue component of color"""
        return self[2]

    def __add__(self, other):
        operation = lambda sc, oc: sc + oc
        return Color(*[cut_in(operation(*args)) for args in zip(self, other)])

    def __mul__(self, other):
        operation = lambda sc, oc: (sc + oc)/2
        return Color(*[cut_in(operation(*args)) for args in zip(self, other)])

    def __sub__(self, other):
        operation = lambda sc, oc: sc - oc
        return Color(*[cut_in(operation(*args)) for args in zip(self, other)])

    @classmethod
    def get(cls, color):
        """Return Color object from color description

        Args:
            color (3-int-tuple|str|Color): color description
        """
        if isinstance(color, cls):
            return color
        if isinstance(color, (list, tuple)):
            return cls(*color)
        if isinstance(color, str):
            key = color.replace(" ", "_").replace("grey", "gray").lower()
            try:
                return COLORS[key]
            except KeyError:
                raise KeyError(f"Unknown color '{color}' (key={key})")
        raise TypeError(f"Can't build color from {type(color)} objects")

    @classmethod
    def mix(cls, *colors):
        """Return mean of colors"""
        if not colors:
            raise TypeError("Expecting at least one color to mix")
        if len(colors) == 1:
            return colors[0]
        return colors[0] * cls.mix(*colors[1:])


COLORS = Param({n: Color(*t) for n, t in COLOR_TUPLES.items()})

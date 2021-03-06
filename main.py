import pygame as pg
from os.path import dirname, join
from oldisplay import Window
from oldisplay.collections import Color
from oldisplay.components import Disk, Grid, Rectangle, Text
from olutils import load, mkdirs, read_params, wait_until
from logzero import logger, loglevel

WORD_DIR = "words"
OUTPUT_DIR = "outputs"


# --------------------------------------------------------------------------- #
# ---- UTILS

def screenshot(window, path):
    """Screenshot window

    Args:
        window (oldisplay.Window)
        output (str): relative path to output directory to save screenshot
    """
    tick = window.ticks
    wait_until(lambda: window.ticks > tick, timeout=5 * window.settings.fps)
    mkdirs(dirname(path))
    pg.image.save(window.screen, path)
    logger.info(f"Screenshot made and saved at '{path}'")


# --------------------------------------------------------------------------- #
# ---- GRID

GRID_PARAMS = {
    'color': 'light_grey',
    'width': 1,
    'xy_margin': (10, 10),
}


class CardGrid(Grid):

    def __init__(self, window, card_size, **params):
        params = read_params(params, GRID_PARAMS)
        page_x, page_y = window.settings.size
        x_margin, y_margin = params.pop('xy_margin')
        assert page_x > 2*x_margin, "x-margin must be twice smaller than page x-size"
        assert page_y > 2*y_margin, "y-margin must be twice smaller than page y-size"
        params['xbounds'] = (x_margin, page_x-x_margin)
        params['ybounds'] = (y_margin, page_y-y_margin)
        super().__init__(*card_size, **params)
        self.window = window
        self.init(self.window.screen)

def build_display_grid(window, card_size, **params):
    grid = CardGrid(window, card_size, **params)
    window.components.append(grid)
    return grid


# --------------------------------------------------------------------------- #
# ---- WORD CARDS

WORD_PARAMS = {
    'txt_height_r': 6,
    'txt_xmargin_r': 10,
    'txt_ymargin_r': 20,
    'top_txt_font': 'consolas',
    'top_txt_c': 'magenta',
    'bot_txt_font': None,
    'bot_txt_c': 'dodger_blue',
    'bot_txt_rect': 'lavender',
    'grid': {},
}


def load_words(dictionary):
    """Load available words for given dictionary"""
    try:
        words = load(
            join(WORD_DIR, f"{dictionary}.txt"),
            w_eol=False,
            encoding="utf-8"
        )
    except FileNotFoundError:
        raise ValueError(f"No dictionary called {dictionary} in {WORD_DIR}")
    words_nb = len(words)
    words = sorted(set([word.lower() for word in words]))
    duplicates = words_nb - len(words)
    logger.info(
        f"{len(words)} words loaded from dictionary '{dictionary}'"
        f", {duplicates} duplicates ignored"
    )
    return words

def display_word_cards(window, words, card_size, **params):
    """Display one grid of words on window"""
    params = read_params(params, WORD_PARAMS)
    assert window.initiated, "Window must be initialized"
    window.components = []

    # ---- Create Grid
    grid_params = params.pop('grid', {})
    grid = build_display_grid(window, card_size, **grid_params)

    # ---- Read parameters
    txt_height = grid.dy // params.txt_height_r
    txt_xmargin = grid.dx // params.txt_xmargin_r
    txt_ymargin = grid.dy // params.txt_ymargin_r
    bot_txt_font = params.top_txt_font if params.bot_txt_font is None else params.bot_txt_font
    bot_txt_c = params.top_txt_c if params.bot_txt_c is None else params.bot_txt_c


    # ---- Write Words
    if len(words) > grid.cell_nb:
        logger.warning(
            f"Too many words ({len(words)}) regarding the number of cells"
            f" ({grid.cell_nb}): will only use first ({grid.cell_nb}) words"
        )
        words = words[:grid.cell_nb]

    for (x, y), word in grid.xy_enum(words):
        ym = y+grid.dy//2
        window.components += [
            Text(
                word.upper(),
                (x+txt_xmargin, ym-txt_ymargin),
                height=txt_height,
                align="bot-left",
                color=params.top_txt_c,
                font=params.top_txt_font
            ),
            Rectangle(
                (x+txt_xmargin, ym+txt_ymargin//2),
                (grid.dx-3*txt_xmargin//2, txt_height+txt_ymargin),
                color=params.bot_txt_rect,
            ),
            Text(
                word.upper(),
                (x+grid.dx-txt_xmargin, ym+txt_ymargin),
                height=txt_height,
                align="top-right",
                rotate=180,
                color=bot_txt_c,
                font=bot_txt_font
            ),
        ]
    logger.debug(f"{len(words)} word cards displayed on window")


def create_word_cards(window, words, card_size, directory, **params):
    """Create grids of word cards"""
    grid_params = params.get('grid', {})
    grid = CardGrid(window, card_size, **grid_params)

    path_frmt = join(directory, "word_cards_{:02d}.jpg")
    for count, i in enumerate(range(0, len(words), grid.cell_nb), 1):
        display_word_cards(
            window,
            words[i:i+grid.cell_nb],
            card_size,
            **params
        )
        screenshot(window, path_frmt.format(count))


# --------------------------------------------------------------------------- #
# ---- COMPETITION CARDS

GAME_PARAMS = {
    'board_size': (5, 5),
    'guess_nb': 8,
    't1_color': "tomato",
    't2_color': "corn_flower_blue",
    'neutral_color': "pale_golden_rod",
    'death_color': "black",
    'grid': {},
}

VALIDATION_PARAMS = GAME_PARAMS.copy()
VALIDATION_PARAMS.update({
    'form_ratio': 4,
})

BOARD_PARAMS = GAME_PARAMS.copy()
BOARD_PARAMS.update({
    'form_ratio': 4,
    'grid': {'width': 3},
})

# -- Validation Cards

def display_validation_cards(window, card_size, **params):
    """Display validation cards on window"""
    params = read_params(params, VALIDATION_PARAMS)
    assert window.initiated, "Window must be initialized"
    window.components = []

    # ---- Display grid
    grid_params = params.pop('grid', {})
    grid = build_display_grid(window, card_size, **grid_params)

    # Display cards content
    colors = (
        [params.t1_color] * params.guess_nb
        + [params.t2_color] * params.guess_nb
        + [Color.mix(params.t1_color, params.t2_color)]
    )
    assert len(colors) <= (grid.i_max * grid.j_max), (
        "Not enough space to display all validation cards"
    )
    sx, sy = grid.dx//params.form_ratio, grid.dy//params.form_ratio
    for (x, y), color in grid.xy_enum(colors):
        x, y = x+grid.dx//2, y+grid.dy//2
        window.components.append(
            Rectangle((x, y), (sx, sy), color=color, align='center')
        )
    logger.debug(f"{len(colors)} validation cards displayed on window")


def create_validation_cards(window, card_size, directory, **params):
    """Create grid of validation cards"""
    display_validation_cards(
        window,
        card_size,
        **params
    )
    screenshot(window, join(directory, "validation_cards.jpg"))


# -- Board cards

def display_board_cards(window, card_size, **params):
    """Display validation cards on window"""
    params = read_params(params, BOARD_PARAMS)
    assert window.initiated, "Window must be initialized"
    window.components = []


    # Main grid
    grid_params = params.pop('grid', {})
    grid = build_display_grid(window, card_size, **grid_params)

    # Card grids
    cell_dx = grid.dx // params.board_size[0]
    cell_dy = grid.dy // params.board_size[1]
    cell_di, cell_dj = params.board_size
    colors = [params.t1_color, params.t2_color] * (grid.cell_nb//2)
    for (x, y), color in grid.xy_enum(colors):
        # Inner grid
        window.components.append(Grid(
            cell_dx, cell_dy,
            xbounds=(x, x+grid.dx),
            ybounds=(y, y+grid.dy),
            color=color,
            only_inside=True,
        ))

        # Card colors
        positions = [
            (x+i*cell_dx, y+j*cell_dy)
            for i in range(cell_di)
            for j in range(cell_dj)
        ]
        card_colors = (
            [params.t1_color] * params.guess_nb
            + [params.t2_color] * params.guess_nb
            + [color, params.death_color]
        )
        assert len(card_colors) < len(positions)
        card_colors += [params.neutral_color] * (len(positions)-len(card_colors))
        rd.shuffle(card_colors)
        radius = min(cell_dx, cell_dx) // (params.form_ratio*2)
        for (x, y), color in zip(positions, card_colors):
            window.components.append(Disk(
                (x+cell_dx//2, y+cell_dy//2),
                radius=radius,
                color=color
            ))
    logger.debug(f"{len(colors)} board cards displayed on window")


def create_board_cards(window, card_size, directory, **params):
    """Create grids of board cards"""
    grid_nb = 2
    path_frmt = join(directory, "board_cards_{:02d}.jpg")
    for i in range(1, grid_nb+1):
        display_board_cards(
            window,
            card_size,
            **params
        )
        screenshot(window, path_frmt.format(i))

# --------------------------------------------------------------------------- #
# ---- MAIN

if __name__ == "__main__":
    import random as rd
    loglevel("INFO")

    # Params
    dictionary = "french"
    output_dir = join(OUTPUT_DIR, f"output_{dictionary}")
    page = (29.7, 21)
    wcard = (4.6, 3)        # Word card
    bcard = (6, 6)          # Board card
    factor = 45

    # Read Params
    page_size = int(page[0] * factor), int(page[1] * factor)
    wcard_size = int(wcard[0] * factor), int(wcard[1] * factor)
    bcard_size = int(bcard[0] * factor), int(bcard[1] * factor)

    # Initialize components
    window = Window(size=page_size, background='white')
    window.open()
    words = load_words(dictionary)
    rd.shuffle(words)

    # Build word grid
    create_word_cards(
        window,
        words,
        wcard_size,
        directory=output_dir,
    )
    create_validation_cards(
        window,
        wcard_size,
        directory=output_dir,
    )
    create_board_cards(
        window,
        bcard_size,
        directory=output_dir,
    )

    # End
    window.wait_close()

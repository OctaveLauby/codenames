import pygame as pg
from os.path import dirname, join
from oldisplay import Window
from oldisplay.collections import Color
from oldisplay.components import Disk, Grid, Rectangle, Text
from olutils import load, mkdirs, read_params, wait_until
from logzero import logger


WORD_DIR = "words"
OUTPUT_DIR = "outputs"


# --------------------------------------------------------------------------- #
# ---- TOOLS

def ij_enumerate(iterable, max_j):
    """Enumerate iterable on (i,j) positions in matrix with max_j columns"""
    for k, item in enumerate(iterable):
        j = k // max_j
        i = k % max_j
        yield (i, j), item


def xy_enumerate(iterable, max_j, x_step, y_step):
    """Enumerate iterable on (x, y) positions in grid with max_j columns"""
    for (i, j), item in ij_enumerate(iterable, max_j):
        yield (i*x_step, j*y_step), item


# --------------------------------------------------------------------------- #
# ---- WINDOW UTILS

GRID_PARAMS = {
    'color': 'light_grey',
    'width': 1,
}

def display_grid(window, card_size, **params):
    params = read_params(params, GRID_PARAMS)
    page_dx, page_dy = window.settings.size
    card_dx, card_dy = card_size
    assert page_dx > card_dx, "Required card x-size must be smaller than page"
    assert page_dy > card_dy, "Required card y-size must be smaller than page"

    window.components.append(Grid(card_dx, card_dy, **params))
    grid_di = page_dy // card_dy
    grid_dj = page_dx // card_dx
    cell_nb = grid_di * grid_dj
    logger.debug(f"Grid built with {grid_di}x{grid_dj}={cell_nb} cells")
    return grid_di, grid_dj

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
    'grid_c': GRID_PARAMS['color'],
}


def load_words(dictionary):
    """Load available words for given dictionary"""
    try:
        words = load(join(WORD_DIR, f"{dictionary}.txt"), w_eol=False)
    except FileNotFoundError:
        raise ValueError(f"No dictionary called {dictionary} in {WORD_DIR}")
    logger.info(f"{len(words)} words loaded from dictionary '{dictionary}'")
    return words

def display_word_cards(window, words, card_size, **params):
    """Display one grid of words on window"""
    params = read_params(params, WORD_PARAMS)
    assert window.initiated, "Window must be initialized"
    window.components = []

    # ---- Read parameters
    card_dx, card_dy = card_size

    txt_height = card_dy // params.txt_height_r
    txt_xmargin = card_dx // params.txt_xmargin_r
    txt_ymargin = card_dy // params.txt_ymargin_r
    bot_txt_font = params.top_txt_font if params.bot_txt_font is None else params.bot_txt_font
    bot_txt_c = params.top_txt_c if params.bot_txt_c is None else params.bot_txt_c

    # ---- Create Grid
    grid_di, grid_dj = display_grid(window, card_size, color=params.grid_c)
    cell_nb = grid_di * grid_dj

    # ---- Write Words
    if len(words) > cell_nb:
        logger.warning(
            f"Too many words ({len(words)}) regarding the number of cells"
            f" ({cell_nb}): will only use first ({cell_nb}) words"
        )
        words = words[:cell_nb]

    for (x, y), word in xy_enumerate(words, grid_dj, card_dx, card_dy):
        ym = y+card_dy//2
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
                (card_dx-3*txt_xmargin//2, txt_height+txt_ymargin),
                color=params.bot_txt_rect,
            ),
            Text(
                word.upper(),
                (x+card_dx-txt_xmargin, ym+txt_ymargin),
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
    page_dx, page_dy = page_size
    card_dx, card_dy = card_size
    grid_di = page_dy // card_dy
    grid_dj = page_dx // card_dx
    card_nb = grid_di * grid_dj

    path_frmt = join(directory, "word_cards_{:02d}.jpg")
    for count, i in enumerate(range(0, len(words), card_nb), 1):
        display_word_cards(
            window,
            words[i:i+card_nb],
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
    'disk_r': 6,
    'grid_c': GRID_PARAMS['color'],
}

# -- Validation Cards

def display_validation_cards(window, card_size, **params):
    """Display validation cards on window"""
    params = read_params(params, GAME_PARAMS)
    assert window.initiated, "Window must be initialized"
    window.components = []

    # ---- Display grid

    grid_di, grid_dj = display_grid(window, card_size, color=params.grid_c)

    # Display cards content
    colors = (
        [params.t1_color] * params.guess_nb
        + [params.t2_color] * params.guess_nb
        + [Color.mix(params.t1_color, params.t2_color)]
    )
    assert len(colors) <= (grid_di * grid_dj), (
        "Not enough space to display all validation cards"
    )
    dx, dy = card_size
    sx, sy = dx//3, dy//3
    for (x, y), color in xy_enumerate(colors, grid_dj, *card_size):
        x, y = x+dx//2, y+dy//2
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
    params = read_params(params, GAME_PARAMS)
    assert window.initiated, "Window must be initialized"
    window.components = []

    card_dx, card_dy = card_size
    cell_dx = card_dx // params.board_size[0]
    cell_dy = card_dy // params.board_size[1]

    # Main grid
    grid_di, grid_dj = display_grid(window, card_size, color=params.grid_c, width=3)
    card_nb = grid_di * grid_dj

    # Card grids
    card_di, card_dj = params.board_size
    colors = [params.t1_color, params.t2_color] * (card_nb//2)
    for (x, y), color in xy_enumerate(colors, grid_dj, *card_size):
        # Inner grid
        window.components.append(Grid(
            cell_dx, cell_dy,
            xbounds=(x, x+card_dx),
            ybounds=(y, y+card_dy),
            color=color,
            inner_grid=True,
        ))

        # Card colors
        positions = [
            (x+i*cell_dx, y+j*cell_dy)
            for i in range(card_di)
            for j in range(card_dj)
        ]
        card_colors = (
            [params.t1_color] * params.guess_nb
            + [params.t2_color] * params.guess_nb
            + [color, params.death_color]
        )
        assert len(card_colors) < len(positions)
        card_colors += [params.neutral_color] * (len(positions)-len(card_colors))
        rd.shuffle(card_colors)
        radius = min(cell_dx, cell_dx) // params.disk_r
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

    # Params
    dictionary = "english"
    output_dir = join(OUTPUT_DIR, f"output_{dictionary}")
    page = (29.7, 21)
    wcard = (4, 2.5)        # Word card
    bcard = (5, 5)          # Board card
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

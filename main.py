import pygame as pg
from os.path import dirname, join
from oldisplay import Window
from oldisplay.components import Grid, Rectangle, Text
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
}

def display_grid(window, card_size, **params):
    params = read_params(params, GRID_PARAMS)
    page_dx, page_dy = window.settings.size
    card_dx, card_dy = card_size
    assert page_dx > card_dx, "Required card x-size must be smaller than page"
    assert page_dy > card_dy, "Required card y-size must be smaller than page"

    window.components.append(Grid(card_dx, card_dy, color=params.color))
    grid_di = page_dy // card_dy
    grid_dj = page_dx // card_dx
    cell_nb = grid_di * grid_dj
    logger.info(f"Grid built with {grid_di}x{grid_dj}={cell_nb} cells")
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
    'line_c': GRID_PARAMS['color'],
}


def load_words(dictionary):
    """Load available words for given dictionary"""
    try:
        words = load(join(WORD_DIR, f"{dictionary}.txt"), w_eol=False)
    except FileNotFoundError:
        raise ValueError(f"No dictionary called {dictionary} in {WORD_DIR}")
    logger.info(f"{len(words)} words loaded for dictionary '{dictionary}'")
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
    grid_di, grid_dj = display_grid(window, card_size, color=params.line_c)
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


def create_word_cards(window, words, card_size, directory, **params):
    """Create grids of word cards"""
    page_dx, page_dy = page_size
    card_dx, card_dy = card_size
    grid_di = page_dy // card_dy
    grid_dj = page_dx // card_dx
    cell_nb = grid_di * grid_dj

    path_frmt = join(directory, "word_cards_{:02d}.jpg")
    for count, i in enumerate(range(0, len(words), cell_nb), 1):
        display_word_cards(
            window,
            words[i:i+cell_nb],
            card_size,
            **params
        )
        screenshot(window, path_frmt.format(count))


# --------------------------------------------------------------------------- #
# ---- COMPETITION CARDS

GAME_PARAMS = {
    't1_color': "tomato",
    't2_color': "corn_flower_blue",
    'board_size': (5, 5),
    'guess_nb': 7,
}

def display_validation_cards(window, card_size, **params):
    """Display validation cards on window"""
    params = read_params(params, GAME_PARAMS)
    assert window.initiated, "Window must be initialized"
    window.components = []

    # ---- Display grid

    grid_di, grid_dj = display_grid(window, card_size)

    # Display cards content
    colors = (
        [params.t1_color] * params.guess_nb
        + [params.t1_color] * params.guess_nb
    )
    assert len(colors) + 1 <= (grid_di + grid_dj), (
        "Not enough space to display all validation cards"
    )
    for x, y, color in xy_enumerate(colors, grid_dj, *card_size):
        window.components.append(
            Rectangle((x, y), card_size, color=color)
        )


def create_validation_cards(window, card_size, directory, **params):
    display_validation_cards(
        window,
        card_size,
        **params
    )
    screenshot(window, join(directory, "validation_cards.jpg"))

# --------------------------------------------------------------------------- #
# ---- MAIN

if __name__ == "__main__":
    import random as rd

    # Params
    dictionary = "english"
    output_dir = join(OUTPUT_DIR, f"output_{dictionary}")
    page = (29.7, 21)
    card = (4, 2.5)
    factor = 45

    # Read Params
    page_size = int(page[0] * factor), int(page[1] * factor)
    card_size = int(card[0] * factor), int(card[1] * factor)

    # Initialize components
    window = Window(size=page_size, background='white')
    window.open()
    words = load_words(dictionary)
    rd.shuffle(words)

    # Build word grid
    create_word_cards(
        window,
        words,
        card_size,
        directory=output_dir,
    )

    # End
    window.wait_close()

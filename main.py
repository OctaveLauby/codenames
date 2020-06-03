import pygame as pg
from os.path import join
from oldisplay import Window
from oldisplay.components import Grid, Rectangle, Text
from olutils import load, read_params
from logzero import logger


WORD_DIR = "words"
OUTPUT_DIR = "outputs"

GRID_PARAMS = {
    'txt_height_r': 6,
    'txt_xmargin_r': 10,
    'txt_ymargin_r': 20,
    'top_txt_font': 'consolas',
    'top_txt_c': 'magenta',
    'bot_txt_font': None,
    'bot_txt_c': 'dodger_blue',
    'bot_txt_rect': 'lavender',
    'back_c': 'white',
    'line_c': 'light_grey',
}



def load_words(dictionary):
    """Load available words for given dictionary"""
    try:
        words = load(join(WORD_DIR, f"{dictionary}.txt"), w_eol=False)
    except FileNotFoundError:
        raise ValueError(f"No dictionary called {dictionary} in {WORD_DIR}")
    logger.info(f"{len(words)} words loaded for dictionary '{dictionary}'")
    return words


def create_word_grid(words, page_size, card_size, save=None, show=None, **params):
    """Create grid of words"""
    params = read_params(params, GRID_PARAMS)

    # ---- Read parameters
    show = True if save is None and show is None else show
    assert save or show, "Create grid requires to at least save or show result"

    page_dx, page_dy = page_size
    card_dx, card_dy = card_size
    assert page_dx > card_dx, "Required card x-size must be smaller than page"
    assert page_dy > card_dy, "Required card y-size must be smaller than page"

    txt_height = card_dy // params.txt_height_r
    txt_xmargin = card_dx // params.txt_xmargin_r
    txt_ymargin = card_dy // params.txt_ymargin_r
    bot_txt_font = params.top_txt_font if params.bot_txt_font is None else params.bot_txt_font
    bot_txt_c = params.top_txt_c if params.bot_txt_c is None else params.bot_txt_c


    # ---- Initiate Page
    window = Window(size=page_size, background=params.back_c)

    # ---- Create Grid
    kwargs = {'color': params.line_c}
    window.components.append(Grid(card_dx, card_dy, **kwargs))
    grid_di = page_dy // card_dy
    grid_dj = page_dx // card_dx
    cell_nb = grid_di * grid_dj
    logger.info(f"Grid built with {grid_di}x{grid_dj}={cell_nb} cells")

    # ---- Write Words
    if len(words) > cell_nb:
        logger.warning(
            f"Too many words ({len(words)}) regarding the number of cells"
            f" ({cell_nb}): will only use first ({cell_nb}) words"
        )
        words = words[:cell_nb]

    for k, word in enumerate(words):
        j = k // grid_dj
        i = k % grid_dj
        x, y = i*card_dx, j*card_dy
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


    # ---- Return
    window.open()
    if save:
        pg.image.save(window.screen, join(OUTPUT_DIR, save))
    if show:
        window.wait_close()
    else:
        window.stop = True


def create_word_grids(words, page_size, card_size, output, **params):
    raise NotImplementedError



if __name__ == "__main__":
    import random as rd

    # Params
    dictionary = "english"
    page = (29.7, 21)
    card = (4, 2.5)
    factor = 45

    # Code
    page_size = int(page[0] * factor), int(page[1] * factor)
    card_size = int(card[0] * factor), int(card[1] * factor)
    words = load_words(dictionary)
    rd.shuffle(words)
    create_word_grid(
        words, page_size, card_size,
        save="word_grid.jpg",
        show=True,
    )

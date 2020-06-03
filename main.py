import pygame as pg
from os.path import join
from oldisplay import components, Window
from olutils import load
from logzero import logger


WORD_DIR = "words"
OUTPUT_DIR = "outputs"



def load_words(language):
    """Load available words for given language"""
    try:
        words = load(join(WORD_DIR, f"{language}.txt"), w_eol=False)
    except FileNotFoundError:
        raise ValueError(f"No words could be find for {language} language")
    logger.info(f"{len(words)} words loaded for language {language}")
    return words


def create_grid(words, page_size, card_size, save=None, show=None,
                txt_height=None, txt_height_r=5,
                top_txt_font=None, top_txt_c='blue',
                bot_txt_font=None, bot_txt_c='cyan',
                back_c='white', line_c='black'):
    """Create grid of words"""

    # ---- Read parameters
    show = True if save is None and show is None else show
    assert save or show, "Create grid requires to at least save or show result"

    page_dx, page_dy = page_size
    card_dx, card_dy = card_size
    assert page_dx > card_dx, "Required card x-size must be smaller than page"
    assert page_dy > card_dy, "Required card y-size must be smaller than page"

    txt_height = (card_dy // txt_height_r) if txt_height is None else txt_height
    assert txt_height < (card_dy // 2), "Text height must be at most half of page size"
    bot_txt_font = top_txt_font if bot_txt_font is None else bot_txt_font
    bot_txt_c = top_txt_c if bot_txt_c is None else bot_txt_c

    # ---- Initiate Page
    window = Window(size=page_size, background=back_c)

    # ---- Create Grid
    kwargs = {'color': line_c}
    window.components.append(components.Grid(card_dx, card_dy, **kwargs))
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
        x += card_dx // 2
        y += card_dy // 2
        print(repr(word))
        window.components += [
            components.Text(
                word.upper(), (x, y), height=txt_height,
                align="bot-mid",
                color=top_txt_c, font=top_txt_font
            ),
            components.Text(
                word.upper(), (x, y), height=txt_height,
                align="top-mid",  rotate=180,
                color=bot_txt_c, font=bot_txt_font
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


if __name__ == "__main__":
    import random as rd

    # Params
    language = "english"
    page = (21, 29.7)
    card = (4, 3)
    factor = 30

    # Code
    page_size = int(page[0] * factor), int(page[1] * factor)
    card_size = int(card[0] * factor), int(card[1] * factor)
    words = load_words(language)
    rd.shuffle(words)
    create_grid(
        words, page_size, card_size,
        save="word_grid.jpg",
        show=True,
        line_c="light grey",

        txt_height_r = 6,
        top_txt_font="calibri",
        top_txt_c="magenta",
    )

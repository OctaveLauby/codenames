from os.path import join
from olutils import load
from PIL import Image, ImageDraw
from logzero import logger

from colors import Color

WORD_DIR = "words"
OUTPUT_DIR = "outputs"



def load_words(language):
    """Load available words for given language"""
    try:
        words = load(join(WORD_DIR, f"{language}.txt"))
    except FileNotFoundError:
        raise ValueError(f"No words could be find for {language} language")
    logger.info(f"{len(words)} words loaded for language {language}")
    return words


def create_grid(words, page_size, card_size, save=None, show=None,
                back_c='white', line_c='grey', text_c='cyan'):
    """Create grid of words"""
    show = True if save is None and show is None else show
    assert save or show, "Create grid requires to at least save or show result"

    # ---- Initiate Page
    img = Image.new('RGB', page_size, color=Color.get(back_c))
    draw = ImageDraw.Draw(img)

    # ---- Create Grid
    page_dx, page_dy = page_size
    card_dx, card_dy = card_size
    assert page_dx > card_dx, "Required card x-size must be smaller than page"
    assert page_dy > card_dy, "Required card y-size must be smaller than page"

    # Horizontal Lines
    grid_dj = -1
    position = 0
    while position < page_dx:
        draw.line((position, 0, position, page_dy), fill=Color.get(line_c))
        grid_dj += 1
        position += card_dx

    # Vertical Lines
    grid_di = -1
    position = 0
    while position < page_dy:
        draw.line((0, position, page_dx, position), fill=Color.get(line_c))
        grid_di += 1
        position += card_dy

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
        draw.text((x, y), word, fill=Color.get(text_c), align='center')

    if save:
        img.save(join(OUTPUT_DIR, save))
    if show:
        img.show()




if __name__ == "__main__":
    # Params
    language = "english"

    # Code
    words = load_words(language)
    create_grid(words, (2100, 2970), (400, 300))

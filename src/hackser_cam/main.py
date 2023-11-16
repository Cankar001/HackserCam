import click
import cv2 as cv
import sys
from pathlib import Path

from src.hackser_cam.analyzers.greyscale_detection.greyscale_detection import greyscale_detector
from .utils import logger as log

from .analyzers.edge_detection import edge_detector
from .analyzers.greyscale_detection import greyscale_detector
from .analyzers.color_spectrum import color_spectrum
from .analyzers.contrast_analyzer import contrast_analyzer

def load_image(path: Path) -> cv.typing.MatLike:
    img = cv.imread(path)
    assert img is not None, "file could not be read"
    return img

@click.command()
@click.option("--analyzer", help="the analyzer to use (dev only)")
@click.option("--img-path", help="The image path (dev only)", type=click.Path(exists=True))
def main(analyzer: str, img_path: click.Path):

    img = cv.imread(img_path)
    detector = None

    if analyzer == 'greyscale_detection':
        log.info('Running greyscale_detection analysis...')
        detector = greyscale_detector()
    elif analyzer == 'edge_detection':
        log.info('Running edge detection analysis...')
        detector = edge_detector()
    elif analyzer == 'color_spectrum':
        log.info('Running color spectrum analysis...')
        detector = color_spectrum()
    elif analyzer == 'contrast_analyzer':
        detector = contrast_analyzer;
        log.info('Running contrast analysis...')
    else:
        log.error('unknown analyzer. Stop.')
        sys.exit(1)

    fuzzy_value = detector.run(img)
    log.info(f'Fuzzy value: {fuzzy_value}')

    while 1:
        detector.update()
        cv.imshow('input', img)
        key = cv.waitKey(0)
        if key == ord('q') or key == 27: # 27 = ESCAPE
            break

    cv.destroyAllWindows()
if __name__ == '__main__':
    main()

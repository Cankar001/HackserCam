import click
import cv2 as cv
from pathlib import Path

from .utils import logger as log

def load_image(path: Path) -> cv.typing.MatLike:
    img = cv.imread(path)
    assert img is not None, "file could not be read"
    return img

@click.command()
# @click.option("--analyzer", help="the analyzer to use")
@click.argument("analyzer", type=str)
@click.argument("img_path", type=click.Path(exists=True))
def main(analyzer: str, img_path: click.Path):
    click.echo(f"analyzing file: {img_path} \nwith analyzer: {analyzer}")

if __name__ == '__main__':
    main()

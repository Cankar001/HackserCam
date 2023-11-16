import click
import cv2 as cv
import sys
import os
from pathlib import Path

from src.hackser_cam.analyzers.greyscale_detection.greyscale_detection import greyscale_detector
from .utils import logger as log

from .analyzers import analyzer
from .analyzers.edge_detection import edge_detector
from .analyzers.greyscale_detection import greyscale_detector
from .analyzers.color_spectrum import color_spectrum
from .analyzers.contrast_analyzer import contrast_analyzer

def load_image(path: Path) -> cv.typing.MatLike:
    img = cv.imread(path)
    assert img is not None, "file could not be read"
    return img

def create_analyzer(analyzer: str) -> analyzer:
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
        detector = contrast_analyzer()
        log.info('Running contrast analysis...')
    else:
        log.error('unknown analyzer. Stop.')
        sys.exit(1)

    return detector

def get_all_images_of_directory(file_path: str) -> list:
    valid_extensions = [".jpg", ".jpeg", ".png", ".tga"]
    result = []
    parent_path = os.path.relpath(file_path)

    for f in os.listdir(file_path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_extensions:
            continue

        result.append(parent_path + '/' + f)

    return result

@click.command()
@click.option("--analyzer", help="the analyzer to use (dev only)")
@click.option("--img-path", help="The image path (dev only)", type=click.Path(exists=True))
@click.option("--cropped", help="Crops the image by <cropped_x>x<cropped_y> (dev only)")
@click.option("--single-shot", is_flag=True, help="Takes in a single file path as input image instead of a folder (dev only)")
def main(analyzer: str, img_path: click.Path, cropped: str, single_shot: bool):

    if single_shot:
        # We take in a single image path and 
        # apply the analysis a single time on a single image.
        img = cv.imread(img_path)

        if cropped is not None:
            tmp = cropped.split('x')
            crop_x = int(tmp[0])
            crop_y = int(tmp[1])
            img = img[crop_y:len(img), crop_x:len(img[0])-crop_x]

        detector = create_analyzer(analyzer)
        fuzzy_value = detector.run(img)
        log.info(f'Fuzzy value: {fuzzy_value}')

        while 1:
            detector.update()
            preview = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
            cv.imshow('input', preview)
            key = cv.waitKey(0)
            if key == ord('q') or key == 27: # 27 = ESCAPE
                break

        cv.destroyAllWindows()
    else:
        # We take in a folder and apply the analysis foreach image in the directory
        image_paths = get_all_images_of_directory(img_path)
        
        # TODO: later we should create all analyzers and run the analysis foreach analyzer.
        detector = create_analyzer(analyzer)

        for image in image_paths:
            img = cv.imread(image)

            # Crop image if needed
            if cropped is not None:
                tmp = cropped.split('x')
                crop_x = int(tmp[0])
                crop_y = int(tmp[1])
                img = img[crop_y:len(img), crop_x:len(img[0])-crop_x]

            fuzzy_value = detector.run(img)
            log.info(f'Fuzzy value: {fuzzy_value}')
            detector.update()

            preview = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
            cv.imshow('input', preview)
            key = cv.waitKey(1500)
            if key == ord('q') or key == 27: # 27 = ESCAPE
                break

    cv.destroyAllWindows()


if __name__ == '__main__':
    main()

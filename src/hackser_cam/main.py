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

def create_analyzer(analyzer: str, initial_img) -> analyzer:
    detector = None

    if analyzer == 'greyscale_detection':
        log.info('Running greyscale_detection analysis...')
        detector = greyscale_detector()
    elif analyzer == 'edge_detection':
        log.info('Running edge detection analysis...')
        detector = edge_detector(initial_img)
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

def split_images(images: list, raster_size):
    
    i = 0
    result = list()
    parts = list()
    for image in images:

        if i % raster_size == 0 and len(parts) == raster_size:
            result.append(parts)
            parts = []

        parts.append(image)
        i += 1

    return result

def print_image_split(images, raster_size):
    i = 0
    for image_parts in images:
        for image in image_parts:
            if i % raster_size == 0:
                i = 0
                print()

            print(f'  {i}: {image}')
            i += 1

def crop_image(image, cropped: str):
    tmp = cropped.split('x')
    crop_x = int(tmp[0])
    crop_y = int(tmp[1])
    cropped_image = image[crop_y:len(image), crop_x:len(image[0])-crop_x]
    return cropped_image

@click.command()
@click.option("--analyzer", help="the analyzer to use (dev only)")
@click.option("--img-path", help="The image path (dev only)", type=click.Path(exists=True))
@click.option("--cropped", help="Crops the image by <cropped_x>x<cropped_y> (dev only)")
def main(analyzer: str, img_path: click.Path, cropped: str):

    # how many pictures are taken at once.
    bulk_image_count = 15
    
    if not os.path.exists('./test_data/initial_image.jpg'):
        log.error('Error: initial image not found. Check readme. Stop.')
        sys.exit(1)

    initial_img = cv.imread('./test_data/initial_image.jpg')

    # first check if img_path is a folder or a file
    if os.path.isfile(img_path):
        # We take in a single image path and 
        # apply the analysis a single time on a single image.
        img = cv.imread(img_path)

        # Crop image, if needed
        if cropped is not None:
            img = crop_image(img, cropped)

        detector = create_analyzer(analyzer, initial_img)
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
        image_groups = split_images(image_paths, bulk_image_count)
        #print_image_split(image_groups, bulk_image_count)

        detectors = [
            greyscale_detector(),
            edge_detector(initial_img),
            color_spectrum(),
            contrast_analyzer()
        ]

        for image_group in image_groups:
            fuzzies = []
            for image in image_group:
                img = cv.imread(image)

                # Crop image, if needed
                if cropped is not None:
                    img = crop_image(img, cropped)

                # run through every registered detector
                detector_fuzzies = []
                for detector in detectors:
                    fuzzy_value = detector.run(img)
                    log.info(f'Fuzzy value: {fuzzy_value}')
                    detector.update()
                    detector_fuzzies.append(fuzzy_value)

                # calculate average value of the detectors
                average_fuzzy = 0
                for fuzzy in detector_fuzzies:
                    average_fuzzy = average_fuzzy + fuzzy


                detector_fuzzy = average_fuzzy /len(detector_fuzzies)
                fuzzies.append(detector_fuzzy)

                # render preview window
                preview = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
                cv.imshow('input', preview)
                key = cv.waitKey(500)
                
                # exit, if key press
                if key == ord('q') or key == 27: # 27 = ESCAPE
                    cv.destroyAllWindows()
                    sys.exit(0)
            
            # get the min value of the fuzzie value of the whole bulk_image_count
            min_fuzzy = sys.float_info.max
            for fuzzy in fuzzies:
                if fuzzy < min_fuzzy:
                    min_fuzzy = fuzzy

            log.success(f'Final fuzzy: {min_fuzzy}')

    cv.destroyAllWindows()


if __name__ == '__main__':
    main()

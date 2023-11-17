# HackserCam

## pre requirements

a good picture without smoke or dirt has to be in the `test_data` folder, named `initial_image.jpg`.

## run main with poetry
- install dependencies
```sh
  poetry install
```
- run
```sh
  poetry run cam --analyzer <analyzer> --img-path <image path>
```

## build from source
- install `poetry`
```sh
  pip install poetry
```
- build with poetry
```sh
  poetry build
```

## dependencies
- click
- colorama
- opencv

## Command line options

| Name                         | Optional | Default | Description  |
| :---                         |  :----:  | :----:  |         :--- |
| --help                       |   Yes    |  None   | Show the help menu and quit
| --analyzer <analyzer_name>   |   No     |  None   | the analyzer to use (dev only)
| --img-path <img_path>        |   No     |  None   | The image path (dev only)
| --cropped <crop_x>x<crop_y>  |   Yes    |  None   | Crops the image by crop_x and crop_y (dev only)

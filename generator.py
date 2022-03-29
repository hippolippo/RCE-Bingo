from PIL import Image, ImageDraw, ImageFilter
from json import load
import os
from random import sample


def generate_board():
    with open("board_specs.json", "r") as specs:
        settings = load(specs)
    tile_count = settings["dimensions"][0] * settings["dimensions"][1]
    tiles_files = os.listdir("tiles")
    if settings["free-tile"]["activated"] and settings["free-tile"]["image"] in tiles_files:
        tiles_files.remove(settings["free-tile"]["image"])
    tiles_files = sample(tiles_files, tile_count)
    image = Image.open("backdrops/background.jpg")
    counter = 0
    for y in range(settings["dimensions"][1]):
        for x in range(settings["dimensions"][0]):
            tile = Image.open(os.path.join("tiles", tiles_files[counter]))
            if settings["free-tile"]["activated"] and x == settings["free-tile"]["position"][0] and\
                    y == settings["free-tile"]["position"][1]:
                tile = Image.open(os.path.join("tiles", settings["free-tile"]["image"]))
            coordinates = [settings["top-left"][0] + settings["offset"][0] * x,
                           settings["top-left"][1] + settings["offset"][1] * y]
            image.paste(tile, (coordinates[0], coordinates[1]))
            counter += 1
    overlay = Image.open("backdrops/foreground.png")
    image.paste(overlay, (0, 0), overlay)
    return image


if __name__ == "__main__":
    generate_board().save("output.png")

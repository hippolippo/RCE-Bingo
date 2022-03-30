from PIL import Image
from json import load
import os
from random import choices, sample, shuffle


def wsample(population, k, weights):
    """
    similar to sample function but takes a weights parameter
    :param population: iterable object
    :param k: integer number of results
    :param weights: iterable object same size as population
    :return: tuple with results
    """
    if len([x for x in weights if x != weights[0]]) == 0:
        return sample(population, k)
    population = [i for i in population]
    result = []
    for n in range(k):
        picked = choices([i for i in range(len(population))], weights)[0]
        weights.pop(picked)
        result.append(population.pop(picked))
    # prevents high weights from always being a the top
    shuffle(result)
    return tuple(result)


def generate_board():
    with open("board_specs.json", "r") as specs:
        settings = load(specs)
    with open("weights.json", "r") as specs:
        weight_settings = load(specs)
    tile_count = settings["dimensions"][0] * settings["dimensions"][1]
    tiles_files = os.listdir("tiles")
    # remove free tile from pick-able tiles
    if settings["free-tile"]["activated"] and settings["free-tile"]["image"] in tiles_files:
        tiles_files.remove(settings["free-tile"]["image"])
    weights = [(weight_settings["default-weight"] if tile not in weight_settings["overrides"]
                else weight_settings["overrides"][tile]) for tile in tiles_files]
    tiles_files = wsample(tiles_files, tile_count, weights)
    background = Image.open("backdrops/background.png")
    counter = 0
    for y in range(settings["dimensions"][1]):
        for x in range(settings["dimensions"][0]):
            tile = Image.open(os.path.join("tiles", tiles_files[counter]))
            # use free tile instead if in the free tile position
            if settings["free-tile"]["activated"] and x == settings["free-tile"]["position"][0] and \
                    y == settings["free-tile"]["position"][1]:
                tile = Image.open(os.path.join("tiles", settings["free-tile"]["image"]))
            coordinates = [settings["top-left"][0] + settings["offset"][0] * x,
                           settings["top-left"][1] + settings["offset"][1] * y]
            background.paste(tile, (coordinates[0], coordinates[1]))
            counter += 1
    # use foreground containing "Free" overlay
    if settings["free-tile"]["activated"]:
        overlay = Image.open("backdrops/foreground_free.png")
    else:
        overlay = Image.open("backdrops/foreground.png")
    final_image = Image.alpha_composite(background, overlay)
    return final_image


if __name__ == "__main__":
    generate_board().save("output.png")

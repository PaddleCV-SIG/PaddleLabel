import random
import time


def rgb_to_hex(rgb):
    rgb = tuple(int(c) for c in rgb)
    return ("#%02x%02x%02x" % rgb).upper()


def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def name_to_hex(name):
    color_map = {
        "red": "#FF0000",
        "white": "#FFFFFF",
        "cyan": "#00FFFF",
        "silver": "#C0C0C0",
        "blue": "#0000FF",
        "gray": "#808080",
        "darkblue": "#0000A0",
        "black": "#000000",
        "lightblue": "#ADD8E6",
        "orange": "#FFA500",
        "purple": "#800080",
        "brown": "#A52A2A",
        "yellow": "#FFFF00",
        "maroon": "#800000",
        "lime": "#00FF00",
        "green": "#008000",
        "magenta": "#FF00FF",
        "olive": "#808000",
    }
    if name[0] == "#" and len(name) == 7:
        return name

    name = name.lower()
    if name not in color_map.keys():
        raise RuntimeError(f"Don't have hex value for color {name}")

    return color_map[name]


# TODO: generate color with high contrast
# TODO: generate color within certain range
# TODO: even devide color space
def rand_hex_color(current_colors=[]):
    random.seed(time.time())
    r = lambda: random.randint(0, 255)
    while True:
        c = "#%02X%02X%02X" % (r(), r(), r())
        c = c.upper()
        if c not in current_colors:
            break
    return c


# Red 	#FF0000
# White 	#FFFFFF
# Cyan 	#00FFFF
# Silver 	#C0C0C0
# Blue 	#0000FF
# Gray 	#808080
# DarkBlue 	#0000A0
# Black 	#000000
# LightBlue 	#ADD8E6
# Orange 	#FFA500
# Purple 	#800080
# Brown 	#A52A2A
# Yellow 	#FFFF00
# Maroon 	#800000
# Lime 	#00FF00
# Green 	#008000
# Magenta 	#FF00FF
# Olive 	#808000

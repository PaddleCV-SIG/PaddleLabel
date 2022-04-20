import numpy as np
import scipy as sp
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt


def polygon2mask(poly):
    nx, ny = 10, 10

    poly = [(1, 1), (2, 1), (3, 1), (2, 3)]

    img = Image.new("L", [nx, ny], 0)
    ImageDraw.Draw(img).polygon(poly, outline=1, fill=1)  # col, row
    mask = np.array(img)

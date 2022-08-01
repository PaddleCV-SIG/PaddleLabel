import math

import numpy as np
from PIL import Image, ImageDraw
import connexion
from .util.polygon import mask2polygon

import matplotlib.pyplot as plt


def polygon2mask(poly):
    """Convert polygon to mask.

    Origion at top left, width height.

    Args:
        poly (list): - list of points: [(w, h), (w, h), ..., (w, h)]
                     - list of flattened points: [w, h, w, h, ..., w, h]
    """

    poly = np.array(poly)

    if poly.ndim == 1:
        poly = poly.reshape((-1, 2))

    wmin, hmin = poly.min(axis=0)
    wmax, hmax = poly.max(axis=0)
    width = wmax - wmin + 1
    height = hmax - hmin + 1

    poly[:, 0] -= wmin
    poly[:, 1] -= hmin

    poly = [(p[0], p[1]) for p in poly.tolist()]

    img = Image.new("L", [width, height], 0)
    ImageDraw.Draw(img).polygon(poly, outline=1, fill=1)  # col, row
    mask = np.array(img) == 1
    # plt.imshow(mask)
    # plt.show()
    # print("=-=-=-=-=-=", width, height, mask.shape)

    # plt.imshow(mask)
    # plt.show()
    # print(mask)

    return (wmin, hmin), mask


# polygon2mask([(1, 1), (2, 1), (3, 1), (2, 8)])
# polygon2mask([(0,0), (100, 0), (100, 20), (0, 30)])
# polygon2mask([0, 0, 100, 0, 100, 20, 0, 30])


"""
	{
		"annotation_id": 2,
		"created": "2022-06-11T11:24:42.484401",
		"data_id": 3,
		"frontend_id": null,
		"label": {
			"color": "#800000",
			"comment": null,
			"created": "2022-06-11T11:24:42.286857",
			"id": 1,
			"label_id": 1,
			"modified": "2022-06-11T11:24:42.286861",
			"name": "视盘",
			"project_id": 1,
			"super_category_id": null
		},
		"label_id": 1,
		"modified": "2022-06-11T11:24:42.484404",
		"project_id": 1,
		"result": "0,1,30,10,31,10,32,10,33,10,34,10,35,10,36,10,37,10,38,10,39,10,30,11,31,11,32,11,33,11,34,11,35,11,36,11,37,11,38,11,39,11,30,12,31,12,32,12,33,12,34,12,35,12,36,12,37,12,38,12,39,12,30,13,31,13,32,13,33,13,34,13,35,13,36,13,37,13,38,13,39,13,30,14,31,14,32,14,33,14,34,14,35,14,36,14,37,14,38,14,39,14,30,15,31,15,32,15,33,15,34,15,35,15,36,15,37,15,38,15,39,15,30,16,31,16,32,16,33,16,34,16,35,16,36,16,37,16,38,16,39,16,30,17,31,17,32,17,33,17,34,17,35,17,36,17,37,17,38,17,39,17,30,18,31,18,32,18,33,18,34,18,35,18,36,18,37,18,38,18,39,18,30,19,31,19,32,19,33,19,34,19,35,19,36,19,37,19,38,19,39,19",
		"task_id": 3,
		"type": "brush"
	},
"""


def polygon2points(poly):
    (wmin, hmin), mask = polygon2mask(poly)
    points = []
    for idh in range(mask.shape[0]):
        for idw in range(mask.shape[1]):
            if mask[idh][idw] == 1:
                points.append((wmin + idw, hmin + idh))

    return points


# print(polygon2points([(0, 1), (3, 2), (3, 3), (1, 3)]))
# print(polygon2points([0, 1, 3, 2, 3, 3, 1, 3]))


def polygon2points_str():
    poly = connexion.request.json["polygon"]
    # print(poly, type(poly), type(poly[0]))
    poly = poly.split(",")
    poly = [int(p) for p in poly]

    (wmin, hmin), mask = polygon2mask(poly)
    points = []
    for idw in range(mask.shape[0]):
        for idh in range(mask.shape[1]):
            if mask[idw][idh] == 1:
                points.append(str(wmin + idw))
                points.append(str(hmin + idh))

    return ",".join(points)


# print(polygon2points([(0, 1), (3, 2), (3, 3), (1, 3)]))
# print(polygon2points_str([0, 1, 3, 2, 3, 3, 1, 3]))


def points2polygon_str(ignore_first_two=False):
    points = connexion.request.json["points"]
    points = points.split(",")
    if ignore_first_two:
        points = points[2:]
    points = [int(p) for p in points]
    points = np.array(points)
    points = points.reshape((-1, 2))
    wmax, hmax = points.max(axis=0)
    mask = np.zeros((wmax + 1, hmax + 1), dtype="uint8")
    for p in points:
        mask[p[0], p[1]] = 255
    polygons = mask2polygon(mask)
    polygons = [[str(v) for point in poly for v in point] for poly in polygons]
    polygons = [",".join(poly) for poly in polygons]

    return polygons

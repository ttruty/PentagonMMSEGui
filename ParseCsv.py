
import pandas as pd
import re
import os
from collections import OrderedDict
from itertools import groupby
from operator import itemgetter
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import transforms
# from datetime import datetime, timedelta
import time
import math
import csv
import ast


# file = r'C:\Users\KinectProcessing\Documents\Anoto\Anotopgc\150.846.10.15_Anoto Forms ' \
#        r'Solution_27_11_2017_08.40.26.739.txt '
regex_sample_data = re.compile('\d+\.\d+\s\d+\.\d+\s\d+\s\d+')

# matplotlib defs
fig = plt.figure()

def rotation(rotation_degree):
    rot = transforms.Affine2D().rotate_deg(rotation_degree) # make sure this matches in GUI
    return rot

def draw_stroke(stroke_x, stroke_y):
    ##  plt.scatter(x,y, 0.1)
    plt.plot(stroke_x, stroke_y, color='b', linestyle='-', picker=True)
    # fig = plt.gcf()

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def plot_csv(path, rotation_degree):
    ''' this plots clock from raw data
    usage: plot_clock(path)
    '''

    base = plt.gca().transData
    ax = fig.add_subplot(1, 1, 1)
    count = 0
    with open(path) as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            count += 1
            if count > 7:
                strokeNum = row[0]
                startTime = row[2]
                DateTime = row[3]
                strokeLabel = row[4]
                strokeTime = row[5]
                SampleNum = row[6]
                strokePoints = row[7]
                force = row[8]
                strokeDistance = row[9]

                pointList = ast.literal_eval(strokePoints)
                stroke_count = 0
                coords = pointList
                strkX = []
                strkY = []
                if "Sentence" in strokeLabel:
                    for k in coords:
                        print(k)
                        point = (float(k[0]), float(k[1]))
                        # rotate around ordine counter clockwise 90%
                        origin = (0, 0)
                        angle = math.radians(0)  # 270 for the clock
                        stroke_x, stroke_y = rotate(origin, point, angle)
                        strkX.append(stroke_x)
                        strkY.append(stroke_y)

                    minX = min(strkX)
                    maxX = max(strkX)
                    minY = min(strkY)
                    maxY = max(strkY)
                    height = maxX - minX
                    width = maxY - minY
                    rect = patches.Rectangle((minX, minY), height, width, linewidth=1, edgecolor='r', facecolor='none')
                    rot = rotation(rotation_degree)
                    rect.set_transform(rot + base)
                    ax.plot(strkX, strkY, color='b', linestyle='-', picker=True, transform=rot + base)
                    ax.add_patch(rect)
                    #plt.show()
                    # currentAxis.add_patch(Rectangle((450,-200), 450, 200, fill=False))
                    plt.axis('off')
                    currentAxis = plt.gca()
                    currentAxis.invert_yaxis()
    return fig

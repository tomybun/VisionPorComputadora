#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import cv2

def translate(image, x, y):
    (h, w) = (image.shape[0], image.shape[1])
    M = np.float32([[1, 0, x],
                    [0, 1, y]])
    shifted = cv2.warpAffine(image, M, (w, h))
    return shifted


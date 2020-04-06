#! /usr/bin/env python3


import cv2
import sys
import os


# Change this to match your system's configuration
CASCADE_FILE_PATH = "/usr/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_alt2.xml"
MARGIN_PERCENT_H = 0.5
MARGIN_PERCENT_W = 0.2


def main(*imgs):

    cascade = cv2.CascadeClassifier(CASCADE_FILE_PATH)
    if cascade.empty():
        raise ValueError("Haar cascade file not found.")

    for img_name in imgs:
        img = cv2.imread(img_name)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        i = 0
        for i, (x, y, w, h) in enumerate(cascade.detectMultiScale(gray)):
            hmin = max(0, y - int(MARGIN_PERCENT_H * h))
            hmax = min(img.shape[0], y + h + int(MARGIN_PERCENT_H * h))
            wmin = max(0, x - int(MARGIN_PERCENT_W * w))
            wmax = min(img.shape[1], x + w + int(MARGIN_PERCENT_W * w))
            cropped = img[hmin: hmax, wmin: wmax]
            name, ext = os.path.splitext(img_name)
            cv2.imwrite(f"{name}-crop-{i:0=3d}.{ext}", cropped)

        print(f"Found {i + 1} faces in '{img_name}'", file=sys.stderr)


if __name__ == "__main__":
    main(*sys.argv[1:])


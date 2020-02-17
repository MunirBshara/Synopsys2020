import json

read_file = open("IMG_5198_000000000000_keypoints.json","r")

data = data = json.load(read_file)

xyc_25 = data['people'][0]['pose_keypoints_2d']

print(xyc_25)

print(len(xyc_25))

body_center_idx = 1
shoulder = 5
elbow = 6
hand = 7

import numpy as np

A = np.array(xyc_25)

B = np.reshape(A, (-1,3))

print(B[body_center_idx])


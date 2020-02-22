import json
import os
import numpy as np

body_center_idx = 1
shoulder = 5
elbow = 6
hand = 7
directory = r'.'
frame_num = 0
for filename in os.listdir(directory):
  if filename.endswith(".json"):
      read_file = open(filename, "r")
      data = json.load(read_file)
      xyc_25 = data['people'][0]['pose_keypoints_2d']
      A = np.array(xyc_25)
      B = np.reshape(A, (-1,3))
      B = np.delete(B,2,1)
      f = open("run1.csv", "a")
      f.write(format(frame_num,'03d') + ",")
      f.write(np.array2string(B[body_center_idx], precision=3, separator=',')+",")
      f.write(np.array2string(B[shoulder], precision=3, separator=',')+",")
      f.write(np.array2string(B[elbow], precision=3, separator=',')+",")
      f.write(np.array2string(B[hand], precision=3, separator=',')+"\n")
      f.close()
      frame_num = frame_num + 1
  else:
      continue

f = open("run1.csv", "r")
print(f.read())

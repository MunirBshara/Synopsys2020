# this python script takes all the frames of all the jsons
# select the frames needed per each video
# and collect all the x,y,frame triple into 3D matrix
# then unfold the 3rd matrix into single line in csv file
# this is different than time series
# because now time is part of the 3d input, while in time
# series, the i input a series of 2D positions

import json
import os
import numpy as np

# the body center is position one in BODY_25 model

body_center_idx = 1
directory = r'.'

# the meta data that describe good/bad, right/left player...
# at this point, i create this manually

src_metadata = open(directory + "/info.list", "r")
lines = src_metadata.readlines()


results = open(directory + "/to_s3/results.csv","w")
results.write("Shot\n")

f = open(directory + "/to_s3/3d_data.csv","w")

for fileNum in range(0,39): # len(lines)-1):
                mylines = lines[fileNum].split()
                results.write(mylines[2]+"\n")
                frame_num = 0
                if(lines[fileNum].find("R")):
                        shoulder = 2
                        elbow = 3
                        hand = 4
                else:
                        shoulder = 5
                        elbow = 6
                        hand = 7
                movie_name = mylines[0]
               frame_num = int(mylines[len(mylines)-2])
                while (frame_num <= int(mylines[len(mylines)-1])):
                        filename = movie_name+"/"+movie_name[0:8]+"_"+format(frame_num,'012d')+"_keypoints.json"
                        read_file = open(filename , "r")
                        data = json.load(read_file)
#                       print(filename)
                        if len(data['people'])==0 or len(data['people'][0])==0 or len(data['people'][0]['pose_keypoints_2d'])==0:
                                continue
                        xyc_25 = data['people'][0]['pose_keypoints_2d']
                        A = np.array(xyc_25)
                        B = np.reshape(A, (-1,3))
                        # if this is the first frame, i take the body center position
                        if (frame_num == int(mylines[len(mylines)-2])):
                                start_body_center=B[body_center_idx][0:2]
                        # check if the person picked up is close to the original
                        person_id=1
                        while ( abs(start_body_center[0] - B[body_center_idx][0]) > 80  or  abs(start_body_center[1] - B[body_center_idx][1]) > 80):
                                print("Video: " + filename + " switch to person: " + str(person_id) + "\n")
                                if len(data['people'])==0 or len(data['people'][person_id])==0 or len(data['people'][person_id]['pose_keypoints_2d'])==0:
                                        continue
                                xyc_25 = data['people'][person_id]['pose_keypoints_2d']
                                A = np.array(xyc_25)
                                B = np.reshape(A, (-1,3))
                                person_id = person_id + 1
                        f.write(np.array2string(B[body_center_idx][0], precision=3, separator=',')+",")
                        f.write(np.array2string(B[body_center_idx][1], precision=3, separator=',')+",")
                        if(shoulder==5):
                                f.write(np.array2string(2*B[body_center_idx][0]-B[shoulder][0], precision=3, separator=',')+",")
                                f.write(np.array2string(2*B[body_center_idx][1]-B[shoulder][1], precision=3, separator=',')+",")
                                f.write(np.array2string(2*B[body_center_idx][0]-B[elbow][0], precision=3, separator=',')+",")
                                f.write(np.array2string(2*B[body_center_idx][1]-B[elbow][1], precision=3, separator=',')+",")
                                f.write(np.array2string(2*B[body_center_idx][0]-B[hand][0], precision=3, separator=',')+",")
                                f.write(np.array2string(2*B[body_center_idx][1]-B[hand][1], precision=3, separator=','))
                        else:
                                f.write(np.array2string(B[shoulder][0], precision=3, separator=',')+",")
                                f.write(np.array2string(B[shoulder][1], precision=3, separator=',')+",")
                                f.write(np.array2string(B[elbow][0], precision=3, separator=',')+",")
                                f.write(np.array2string(B[elbow][1], precision=3, separator=',')+",")
                                f.write(np.array2string(B[hand][0], precision=3, separator=',')+",")
                                f.write(np.array2string(B[hand][1], precision=3, separator=','))
                                
                        frame_num = frame_num + 1
                        # even though this is last position in this frame, i add comma and not new line
                        ## adding new line only
                        if (frame_num>60):
                                f.write("\n")
                        else:
                                f.write(",")
f.close()

results.close()

# This python script will take all the json files for each video
# and extract the key body points from each frame, and building
# a time series between the min/max frame numbers as defined in info.list

import json
import os
import numpy as np

# index #1 in BODY_25 format is the body center
body_center_idx = 1
directory = r'.'

# the meta data for videos used for training
# at this point, this is manually entered

src_metadata = open(directory + "/info.list", "r")
lines = src_metadata.readlines()

# number of videos to run on is as many lines in src_metadata

num_of_videos = len(lines) 
metadata = open(directory + "/metadata.csv","w")

# the output file that include Good (1) and Bad (0) indication for each training video

results = open(directory + "/to_s3/results.csv","w")
results.write("Shot\n")

for fileNum in range(0,num_of_videos):
                mylines = lines[fileNum].split()
                metadata.write(str(fileNum) + " " + lines[fileNum])
                # translate G/B to 1/0 in results file
                if (mylines[2] == "G"):
                        results.write("1\n")
                else:
                        results.write("0\n")
                
                frame_num = 0
                
                # identify the 3 points to extract from BODY_25 model
                # based on Right or Left
                if(lines[fileNum].find("R")):
                        shoulder = 2
                        elbow = 3
                        hand = 4
                else:
                        shoulder = 5
                        elbow = 6
                        hand = 7
                movie_name = mylines[0]
                f = open(directory + "/to_s3/data_"+str(fileNum)+".csv", "w")
                f.write("body_center_x, body_center_y, shoulder_x, shoulder_y, elbow_x, elbow_y, hand_x, hand_y\n")

                # start the from the frame number mentioned in info.list file for this specific movied
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
                                f.write(np.array2string(2*B[body_center_idx][1]-B[hand][1], precision=3, separator=',')+"\n")
                        else:
                                f.write(np.array2string(B[shoulder][0], precision=3, separator=',')+",")
                                f.write(np.array2string(B[shoulder][1], precision=3, separator=',')+",")
                                f.write(np.array2string(B[elbow][0], precision=3, separator=',')+",")
                                f.write(np.array2string(B[elbow][1], precision=3, separator=',')+",")
                                f.write(np.array2string(B[hand][0], precision=3, separator=',')+",")
                                f.write(np.array2string(B[hand][1], precision=3, separator=',')+"\n")
                        frame_num = frame_num + 1
                f.close()

results.close()
metadata.close()

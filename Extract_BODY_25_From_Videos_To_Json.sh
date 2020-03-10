#!/bin/bash

# this scripts runs over all the available video files under $HOME/videos
# then calls openpose, without graphics output so i can run it from shell
# openpose will extract each video frame to different json file with the 25 coordinates,
# for each "person" identified by OpenPose

FILES=*.MOV
for f in $FILES
do
  echo "Processing $f file..."
  pushd $HOME/openpose
  ./examples/openpose/openpose.bin --display 0 --render_pose 0 --video $HOME/videos/$f --write_json $HOME/output_dir/$f
  # take action on each file. $f store current file name
  popd
done

1. Make sure to have a GPU instance, with Deep Learning AMI that comes pre-built with most tools needed

2. When you created the instance, you should have saves a private key with .pem

3. to connect via ssh:  

```ssh -i <Your PEM key> ubuntu@<EC2 instance name>```

4. Download VNC viewer

5. Connect to <EC2 instance name>::5901

6. Follow the instructions on OpenPose github to install it

7. to Analyze a video (assuming u already have VNC viewer set up)

~/openpose$ ./examples/openpose/openpose.bin --video ./examples/media/video.avi



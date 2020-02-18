``` EC2 machine: ec2-54-153-31-246.us-west-1.compute.amazonaws.com
```

private key:  MunirNorCal.pem

to connect via ssh:  

ssh -i MunirNorcal.pem ubuntu@ec2-54-153-31-246.us-west-1.compute.amazonaws.com


## For Desktop viewer access

* Download VNC viewer

* Connect to yourHostName::5901

~/openpose$ ./examples/openpose/openpose.bin --video ./examples/media/video.avi


# notes

From ML point of view, this is a binary classification problem:  good or bad

I will use Sage Maker,  AutoML or AutoPilot for choosing the right algorithm

Each input data is a time series with each time sample having [x1,x2,... xn] features, i.e. X,Y coordinates for each relevant part of the body for waterpolo shooting.    another way to look at this, is as n * t matrix with n is the relevant features and t is the number of samples

to train well, i need to normalize the samples to a common reference frame, adjusting for different camera distance and different humans



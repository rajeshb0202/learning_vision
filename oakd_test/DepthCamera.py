#!/usr/bin/env python3

import cv2
import depthai as dai



class DepthCamera:
    
    def __init__(self):
        #create pipeline
        self.pipeline = dai.Pipeline()
           
        
    def mono_left_right_camera_config(self, left_stream_name='left', right_stream_name='right'):
        #define sources and outputs
        self.monoLeft = self.pipeline.create(dai.node.MonoCamera)
        self.monoRight = self.pipeline.create(dai.node.MonoCamera)
        self.xoutLeft = self.pipeline.create(dai.node.XLinkOut)
        self.xoutRight = self.pipeline.create(dai.node.XLinkOut)
        
        #set streams
        self.xoutLeft.setStreamName(left_stream_name)
        self.xoutRight.setStreamName(right_stream_name)
        
        #properties
        self.monoLeft.setCamera("left")
        self.monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        self.monoRight.setCamera("right")
        self.monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        
        #linking
        self.monoRight.out.link(self.xoutRight.input)
        self.monoLeft.out.link(self.xoutLeft.input)
        
    
    def rgb_camera_config(self, rgb_stream_name='rgb', width = 640, height = 400):
        #define sources and outputs
        self.camRgb = self.pipeline.create(dai.node.ColorCamera)
        self.xoutRgb = self.pipeline.create(dai.node.XLinkOut)
        
        #set streams
        self.xoutRgb.setStreamName("rgb")
        
        #properties
        # self.camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_400_P)
        self.camRgb.setPreviewSize(width, height)
        self.camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
        self.camRgb.setInterleaved(True)
        
        #linking
        self.camRgb.preview.link(self.xoutRgb.input)
            
        
    def get_pipeline(self):
        return self.pipeline
    




# Create DepthCamera object
depth_camera = DepthCamera()
depth_camera.mono_left_right_camera_config()
depth_camera.rgb_camera_config()
pipeline = depth_camera.get_pipeline()


# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queues will be used to get the grayscale frames from the outputs defined above
    qLeft = device.getOutputQueue(name="left", maxSize=4, blocking=False)
    qRight = device.getOutputQueue(name="right", maxSize=4, blocking=False)
    qRGB = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

    while True:
        # Instead of get (blocking), we use tryGet (non-blocking) which will return the available data or None otherwise
        inLeft = qLeft.tryGet()
        inRight = qRight.tryGet()
        inRGB = qRGB.tryGet()

        if inLeft is not None:
            cv2.imshow("left", inLeft.getCvFrame())
            print("Left frame: ", inLeft.getCvFrame().shape)

        if inRight is not None:
            cv2.imshow("right", inRight.getCvFrame())
            print("Right frame: ", inRight.getCvFrame().shape)
            
        if inRGB is not None:
            cv2.imshow("rgb", inRGB.getCvFrame())
            print("RGB frame: ", inRGB.getCvFrame().shape)

        if cv2.waitKey(1) == ord('q'):
            break

"""Webcam utilities."""

import cv2

import gfx


KEY_ESC = 27#esc按键


def capture():
    vc = cv2.VideoCapture(0)
    if vc.isOpened():
        _, frame = vc.read()#返回true/false，帧数
        return gfx.Image(frame)#返回gfx的image类的一个实例


def display():
    vc = cv2.VideoCapture(0)
    key = 0
    success = True

    face_detector = gfx.FaceDetector()#创建gfx的FaceDetector类的一个实例

    while success and key != KEY_ESC:#esc和帧数共同控制
        success, frame = vc.read()
        face_detector.show(gfx.Image(frame), wait=False)
        key = cv2.waitKey(20)

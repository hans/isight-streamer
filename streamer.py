#!/usr/bin/env python2.7

import cv2
import zmq
import threading


# Time (in seconds) between frame publishes
INTERVAL = 0.1

QUEUE_URI = 'ipc:///tmp/robotData'
QUEUE_PUBLISH_CHANNEL = 'main'

CAMERA_INDEX = 0

# Set this to None to disable video frame resizing
RESIZE_TO = (100, 100)
RESIZE_INTERPOLATION = cv2.INTER_LANCZOS4


def queue_connect():
    ctx = zmq.Context()
    socket = ctx.socket(zmq.PUB)
    socket.bind(QUEUE_URI)

    return socket


def begin_capture():
    return cv2.VideoCapture(CAMERA_INDEX)


def publish_frame(capture, socket):
    if capture is None:
        return

    _, frame = capture.read()

    if RESIZE_TO is not None:
        frame = cv2.resize(frame, RESIZE_TO,
                           interpolation=RESIZE_INTERPOLATION)

    _, jpeg_data = cv2.imencode('.jpg', frame)

    socket.send('{} {}'.format(QUEUE_PUBLISH_CHANNEL, jpeg_data.tostring()))


def make_iter(capture, socket):
    """
    Build a function which will continuously launch frame captures.
    """

    def cycle():
        threading.Timer(INTERVAL, cycle).start()
        publish_frame(capture, socket)

    return cycle


if __name__ == '__main__':
    socket = queue_connect()
    capture = begin_capture()
    cycle = make_iter(capture, socket)

    cycle()

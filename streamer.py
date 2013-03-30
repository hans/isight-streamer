#!/usr/bin/env python2.7

import cv2
import pika
import threading


# Time (in seconds) between frame publishes
INTERVAL = 0.1

QUEUE_HOST = 'localhost'
QUEUE_PORT = 5672
QUEUE_NAME = 'robotData'

CAMERA_INDEX = 0

# Set this to None to disable video frame resizing
RESIZE_TO = (100, 100)
RESIZE_INTERPOLATION = cv2.INTER_LANCZOS4


def queue_connect():
    params = pika.ConnectionParameters(QUEUE_HOST, QUEUE_PORT)
    queue_connection = pika.BlockingConnection(params)
    queue_channel = queue_connection.channel()

    return queue_connection, queue_channel


def begin_capture():
    return cv2.VideoCapture(CAMERA_INDEX)


def publish_frame(capture, channel):
    if capture is None:
        return

    _, frame = capture.read()

    if RESIZE_TO is not None:
        frame = cv2.resize(frame, RESIZE_TO,
                           interpolation=RESIZE_INTERPOLATION)

    _, jpeg_data = cv2.imencode('.jpg', frame)

    channel.basic_publish(exchange='',
                          routing_key=QUEUE_NAME,
                          body=jpeg_data.tostring())


def make_iter(capture, channel):
    """
    Build a function which will continuously launch frame captures.
    """

    def cycle():
        threading.Timer(INTERVAL, cycle).start()
        publish_frame(capture, channel)

    return cycle


if __name__ == '__main__':
    conn, ch = queue_connect()
    capture = begin_capture()
    cycle = make_iter(capture, ch)

    cycle()

# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import colorsys
import random

import cv2
import numpy as np

from helper.config import INF_TIME_MSG, FONT, FPS_MSG

def generate_colors(labels):
    hsv_tuples = [(x / len(labels), 1., 1.) for x in range(len(labels))]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255),
                                 int(x[2] * 255)), colors))
    random.seed(10101)
    random.shuffle(colors)
    random.seed(None)
    return colors

def put_info_on_frame(frame, result, time, labels, model_name, source_file):
    colors = generate_colors(labels)
    inference_position = (3, 20)
    frame_height, frame_width, _ = frame.shape
    for obj in result:
        pos = obj['pos']
        _id = obj['_id']

        x1 = int(pos[1] * frame_width)
        x2 = int(pos[3] * frame_width)
        y1 = int(pos[0] * frame_height)
        y2 = int(pos[2] * frame_height)

        top = max(0, np.floor(y1 + 0.5).astype('int32'))
        left = max(0, np.floor(x1 + 0.5).astype('int32'))
        bottom = min(frame_height, np.floor(y2 + 0.5).astype('int32'))
        right = min(frame_width, np.floor(x2 + 0.5).astype('int32'))

        label_size = cv2.getTextSize(labels[_id], FONT['hershey'],
                                     FONT['size'], FONT['thickness'])[0]
        label_rect_left = int(left - 3)
        label_rect_top = int(top - 3)
        label_rect_right = int(left + 3 + label_size[0])
        label_rect_bottom = int(top - 5 - label_size[1])

        cv2.rectangle(frame, (left, top), (right, bottom),
                      colors[int(_id) % len(colors)], 6)
        cv2.rectangle(frame, (label_rect_left, label_rect_top),
                             (label_rect_right, label_rect_bottom),
                              colors[int(_id) % len(colors)], -1)
        cv2.putText(frame, labels[_id], (left, int(top - 4)), FONT['hershey'],
                    FONT['size'], FONT['color']['black'], FONT['thickness'])

    cv2.putText(frame, "{}: {}".format(INF_TIME_MSG, time),
                inference_position, FONT['hershey'], 0.5,
                FONT['color']['black'], 2, cv2.LINE_AA)
    cv2.putText(frame, "{}: {}".format(INF_TIME_MSG, time),
                inference_position, FONT['hershey'], 0.5,
                FONT['color']['white'], 1, cv2.LINE_AA)

    y_offset = frame.shape[0] - cv2.getTextSize(source_file,
                                                FONT['hershey'], 0.5, 2)[0][1]

    cv2.putText(frame, "{}: {}".format("source", source_file), (3, y_offset),
                FONT['hershey'], 0.5, FONT['color']['black'], 2, cv2.LINE_AA)
    cv2.putText(frame, "{}: {}".format("source", source_file), (3, y_offset),
                FONT['hershey'], 0.5, FONT['color']['white'], 1, cv2.LINE_AA)

    y_offset -= (cv2.getTextSize(model_name, FONT['hershey'], 0.5, 2)[0][1] + 3)

    cv2.putText(frame, "{}: {}".format("model", model_name), (3, y_offset),
                FONT['hershey'], 0.5, FONT['color']['black'], 2, cv2.LINE_AA)
    cv2.putText(frame, "{}: {}".format("model", model_name), (3, y_offset),
                FONT['hershey'], 0.5, FONT['color']['white'], 1, cv2.LINE_AA)
    return frame

def put_fps_on_frame(frame, fps):
    fps_msg = "{}: {}".format(FPS_MSG, int(fps))
    x_offset = frame.shape[1] - (cv2.getTextSize(fps_msg, FONT['hershey'],
                                                 0.8, 2)[0][0] + 10)
    cv2.putText(frame, fps_msg,
                (x_offset, 25), FONT['hershey'], 0.8,
                FONT['color']['black'], 2, cv2.LINE_AA)
    cv2.putText(frame, fps_msg,
                (x_offset, 25), FONT['hershey'], 0.8,
                FONT['color']['white'], 1, cv2.LINE_AA)
    return frame

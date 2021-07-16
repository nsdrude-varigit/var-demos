# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from contextlib import contextmanager
from datetime import timedelta
from time import monotonic

import cv2

from config import INF_TIME_MSG, FONT

class Timer:
    def __init__(self):
        self.time = 0

    @contextmanager
    def timeit(self):
        begin = monotonic()
        try:
            yield
        finally:
            end = monotonic()
            self.convert(end - begin)

    def convert(self, elapsed):
        self.time = str(timedelta(seconds=elapsed))

def load_labels(args):
    with open(args['label'], 'r') as f:
        return [line.strip() for line in f.readlines()]

def put_info_on_frame(frame, top_result, labels, inference_time, args):
    source_file = args['video']
    model_name = args['model']

    for idx, (i, score) in enumerate (top_result):
        labels_position = (3, 35 * idx + 60)
        inference_position = (3, 20)

        cv2.putText(frame, '{} - {:0.4f}'.format(labels[i], score),
                    labels_position, FONT['hershey'], FONT['size'],
                    FONT['color']['black'], FONT['thickness'] + 2)
        cv2.putText(frame, '{} - {:0.4f}'.format(labels[i], score),
                    labels_position, FONT['hershey'], FONT['size'],
                    FONT['color']['blue'], FONT['thickness'])

    cv2.putText(frame, "{}: {}".format(INF_TIME_MSG, inference_time),
                inference_position, FONT['hershey'], 0.5,
                FONT['color']['black'], 2, cv2.LINE_AA)
    cv2.putText(frame, "{}: {}".format(INF_TIME_MSG, inference_time),
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

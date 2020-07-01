import argparse
import logging
import time

import cv2
import numpy as np

from tf_pose import common
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0

# run.pyをAPI用に必要な部分だけ切り取ったもの
def run(image_name):
    w, h = model_wh('1280x720')
    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(w, h))

    logger.debug('image process+')
    image = common.read_imgfile('./img/' + image_name, None, None)
    if image is None:
        logger.error('Image can not be read, path=%s' % image_file)
        sys.exit(-1)
    humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)

    logger.debug('postprocess+')
    # ここから姿勢のポイントを画像に書き込み、点と線が追加された画像が返ってくる
    image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

    cv2.imwrite('./img/' + image_name, image)

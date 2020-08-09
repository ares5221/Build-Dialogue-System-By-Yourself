#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import argparse
import logging
import json
import sys
import os

import tensorflow as tf
from tensorflow.python.framework import graph_util

from utils import datafeeds
from utils import controler
from utils import utility
from utils import converter

_WORK_DIR = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(_WORK_DIR, '../../../common'))


def load_config(config_file):
    """
    导入配置文件数据
    """
    # 读取配置文件
    with open(config_file, "r") as f:
        try:
            conf = json.load(f)
        except Exception:
            logging.error("load json file %s error" % config_file)
    # 保存配置文件数据
    conf_dict = {}
    unused = [conf_dict.update(conf[k]) for k in conf]
    logging.debug("\n".join(
        ["%s=%s" % (u, conf_dict[u]) for u in conf_dict]))
    return conf_dict


def train(conf_dict):
    """
    训练网络
    """
    training_mode = conf_dict["training_mode"]
    net = utility.import_object(
        conf_dict["net_py"], conf_dict["net_class"])(conf_dict)
    # 采用pointwise模式
    if training_mode == "pointwise":
        # 获取pointwise训练数据
        datafeed = datafeeds.TFPointwisePaddingData(conf_dict)
        input_l, input_r, label_y = datafeed.ops()
        # 输出网络的预测值
        pred = net.predict(input_l, input_r)
        # 将softmax的概率值转换为0，1
        output_prob = tf.nn.softmax(pred, -1, name="output_prob")
        # 设置loss函数
        loss_layer = utility.import_object(
            conf_dict["loss_py"], conf_dict["loss_class"])()
        loss = loss_layer.ops(pred, label_y)
    # 采用pairwise模式
    elif training_mode == "pairwise":
        # 获取pairwise训练数据
        datafeed = datafeeds.TFPairwisePaddingData(conf_dict)
        input_l, input_r, neg_input = datafeed.ops()
        # 输出正向比较的预测结果
        pos_score = net.predict(input_l, input_r)
        output_prob = tf.identity(pos_score, name="output_prob")
        # 输出负向比较的预测结果
        neg_score = net.predict(input_l, neg_input)
        # 设置loss函数，使得正向结果大于负向结果
        loss_layer = utility.import_object(
            conf_dict["loss_py"], conf_dict["loss_class"])(conf_dict)
        loss = loss_layer.ops(pos_score, neg_score)
    else:
        print(sys.stderr, "training mode not supported")
        sys.exit(1)
    # 定义优化器
    lr = float(conf_dict["learning_rate"])
    optimizer = tf.train.AdamOptimizer(learning_rate=lr).minimize(loss)

    # 开始训练
    controler.run_trainer(loss, optimizer, conf_dict)


def predict(conf_dict):
    """
    predict
    """
    # 导入网络
    net = utility.import_object(
        conf_dict["net_py"], conf_dict["net_class"])(conf_dict)
    # 导入测试数据
    conf_dict.update({"num_epochs": "1", "batch_size": "1",
                      "shuffle": "0", "train_file": conf_dict["test_file"]})
    test_datafeed = datafeeds.TFPointwisePaddingData(conf_dict)
    test_l, test_r, test_y = test_datafeed.ops()
    # 预测结果
    pred = net.predict(test_l, test_r)
    controler.run_predict(pred, test_y, conf_dict)


def freeze(conf_dict):
    """
    freeze net for c api predict
    """
    model_path = conf_dict["save_path"]
    freeze_path = conf_dict["freeze_path"]
    training_mode = conf_dict["training_mode"]

    graph = tf.Graph()
    with graph.as_default():
        net = utility.import_object(
            conf_dict["net_py"], conf_dict["net_class"])(conf_dict)
        test_l = dict([(u, tf.placeholder(tf.int32, [None, v], name=u))
                       for (u, v) in dict(conf_dict["left_slots"]).iteritems()])
        test_r = dict([(u, tf.placeholder(tf.int32, [None, v], name=u))
                       for (u, v) in dict(conf_dict["right_slots"]).iteritems()])
        pred = net.predict(test_l, test_r)
        if training_mode == "pointwise":
            output_prob = tf.nn.softmax(pred, -1, name="output_prob")
        elif training_mode == "pairwise":
            output_prob = tf.identity(pred, name="output_prob")

        restore_saver = tf.train.Saver()
    with tf.Session(graph=graph) as sess:
        sess.run(tf.global_variables_initializer())
        restore_saver.restore(sess, model_path)
        output_graph_def = tf.graph_util. \
            convert_variables_to_constants(sess, sess.graph_def, ["output_prob"])
        tf.train.write_graph(output_graph_def, '.', freeze_path, as_text=False)


def convert(conf_dict):
    """
    convert
    """
    converter.run_convert(conf_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', default='train',
                        help='task: train/predict/freeze/convert, the default value is train.')
    parser.add_argument('--task_conf', default='./examples/cnn-pointwise.json',
                        help='task_conf: config file for this task')
    args = parser.parse_args()
    task_conf = args.task_conf
    config = load_config(task_conf)
    task = args.task
    if args.task == 'train':
        train(config)
    elif args.task == 'predict':
        predict(config)
    elif args.task == 'freeze':
        freeze(config)
    elif args.task == 'convert':
        convert(config)
    else:
        print(sys.stderr, 'task type error.')

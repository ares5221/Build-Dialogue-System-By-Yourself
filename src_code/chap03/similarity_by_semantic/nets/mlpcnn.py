#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import logging
import layers.tf_layers as layers


class MLPCnn(object):
    """
    设置网络结构
    """

    def __init__(self, config):
        self.vocab_size = int(config['vocabulary_size'])
        self.emb_size = int(config['embedding_dim'])
        self.kernel_size = int(config['num_filters'])
        self.win_size = int(config['window_size'])
        self.hidden_size = int(config['hidden_size'])
        self.left_name, self.seq_len = config['left_slots'][0]
        self.right_name, self.seq_len = config['right_slots'][0]
        self.task_mode = config['training_mode']
        # 设置网络嵌入层
        self.emb_layer = layers.EmbeddingLayer(self.vocab_size, self.emb_size)
        # 设置网络编码层为CNN
        self.cnn_layer = layers.CNNLayer(self.seq_len, self.emb_size,
                                         self.win_size, self.kernel_size)
        # 设置rule层
        self.relu_layer = layers.ReluLayer()
        self.concat_layer = layers.ConcatLayer()
        # 设置pointwise网络结构
        if self.task_mode == "pointwise":
            self.n_class = int(config['n_class'])
            # 连接两个全连接层
            self.fc1_layer = layers.FCLayer(2 * self.kernel_size, self.hidden_size)
            self.fc2_layer = layers.FCLayer(self.hidden_size, self.n_class)
        # 设置pairwise网络结构
        elif self.task_mode == "pairwise":
            # 设置一个全连接层与cosina层
            self.fc1_layer = layers.FCLayer(self.kernel_size, self.hidden_size)
            self.cos_layer = layers.CosineLayer()
        else:
            logging.error("training mode not supported")

    # 网络的预测函数
    def predict(self, left_slots, right_slots):
        """
        predict graph of this net
        """
        left = left_slots[self.left_name]
        right = right_slots[self.right_name]
        left_emb = self.emb_layer.ops(left)
        right_emb = self.emb_layer.ops(right)
        left_cnn = self.cnn_layer.ops(left_emb)
        right_cnn = self.cnn_layer.ops(right_emb)
        left_relu = self.relu_layer.ops(left_cnn)
        right_relu = self.relu_layer.ops(right_cnn)
        if self.task_mode == "pointwise":
            concat = self.concat_layer.ops([left_relu, right_relu], self.kernel_size * 2)
            concat_fc = self.fc1_layer.ops(concat)
            concat_relu = self.relu_layer.ops(concat_fc)
            pred = self.fc2_layer.ops(concat_relu)
        else:
            hid1_left = self.fc1_layer.ops(left_relu)
            hid1_right = self.fc1_layer.ops(right_relu)
            left_relu2 = self.relu_layer.ops(hid1_left)
            right_relu2 = self.relu_layer.ops(hid1_right)
            pred = self.cos_layer.ops(left_relu2, right_relu2)
        return pred

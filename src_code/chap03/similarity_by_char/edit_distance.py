#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import numpy as np


def edit_distance(str1, str2):
    '''
    利用动态规划计算编辑距离
    :param str1: 
    :param str2: 
    :return: 
    '''
    len1 = len(str1)
    len2 = len(str2)
    dp = np.zeros((len1 + 1, len2 + 1))
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j
    # 利用计算编辑距离的公式来计算
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if str1[i - 1] == str2[j - 1]:
                delta = 0
            else:
                delta = 1
            dp[i][j] = min(dp[i - 1][j - 1] + delta, min(dp[i - 1][j] + 1, dp[i][j - 1] + 1))
    return dp[len1][len2]


if __name__ == "__main__":
    str1 = 'hello'
    str2 = 'world'
    # 计算str1与str2之间的编辑距离
    ed = edit_distance(str1, str2)
    print(ed)

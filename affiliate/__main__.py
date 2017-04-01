#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: t.py
@time: 2017/3/30 下午4:43
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from multiprocessing import cpu_count
import multiprocessing

single_task_path = os.path.join(BASE_DIR, 'affiliate/single_task.py')
reset_path = os.path.join(BASE_DIR, 'affiliate/reset.py')


def task():
    os.system('python %s' % single_task_path)


if __name__ == '__main__':
    os.system('python %s' % reset_path)
    processes = cpu_count()  # 根据cpu核心数决定进程数量
    pool = multiprocessing.Pool(processes=processes)
    [pool.apply_async(task) for i in range(processes)]
    pool.close()
    pool.join()
print(123)

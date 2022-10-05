# -*- coding:utf-8 -*-
'''
@Time   :2022/9/29 07:32
@Author :huangzi
@File   :superns_split.py
'''

import os
import shutil
import exifread
import re

sceneType = {
    \
}

class ClassifyNS():
    """
    ClassifyNS()用于区分一批图中的正常图片和超夜图片
    """
    def __init__(self, img_path):
        self.img_path = img_path
        os.chdir(img_path)

    def read_module(self, img):
        f = open(img, 'rb')
        tags = exifread.process_file(f)
        if 'EXIF UserComment' in tags.keys():
            strexif = tags['EXIF UserComment'].values
            keywords = 'module'
            if keywords in strexif:
                module_type = re.findall(keywords + "(.*?)\;", strexif)[0]
                return module_type
            else:
                return ""
        else:
            return ""

    def classify(self, img):
        photo_module = self.read_module(img)
        photo_set = ""
        if "photo" in photo_module:
            photo_set = "基础"
            shutil.move(img, photo_set)
        elif "night" in photo_module:
            photo_set = "超级夜景"
            shutil.move(img, photo_set)

    def run(self):
        if not os.path.exists('基础'):
            os.makedirs('基础', mode=0o777)
        if not os.path.exists('超夜'):
            os.makedirs('超级夜景', mode=0o777)

        for img in os.listdir(self.img_path):
            self.classify(img)


class ClassifyHDR():
    """
    ClassifyHDR用于区分一批图中的HDR_auto和HDR_off的图
    """
    def __init__(self, module_type="实景"):
        self.test_module = module_type

    def read_sceneMode(self, img):
        f = open(img, 'rb')
        tags = exifread.process_file(f)
        if 'EXIF UserComment' in tags.keys():
            strexif = tags['EXIF UserComment'].values
            keywords = 'sceneMode'
            if keywords in strexif:
                sceneValue = int(re.findall(keywords + "(.*?)\;", strexif)[0])
                sceneMode = self.get_keys(sceneType, sceneValue)
                return sceneMode
            else:
                return ""
        else:
            return ""

    def get_keys(self, dic, value):
        key = ""
        for k, v in dic.items():
            if value == v:
                key = k
                break
        if key == "":
            print("{}无对应算法".format(value))
        return key

    def get_camera_names(self, cmr_info: str, module_type="实景"
                         ) -> str:
        """
        用于镜头判断，目前只写实景模块的镜头判断
        :param cmr_info:
        :param module_type: 图片模式（实景、实景CIS等）
        :return: 镜头信息
        """
        if module_type == "实景":
            cmr_list = ["主摄", "广角", "长焦", "潜望"]
            for i in range(len(cmr_list)):
                if cmr_list[i] in cmr_info:
                    cmr_info = cmr_list[i]
                    break
        return cmr_info


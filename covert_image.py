#! --*-- coding: utf-8 --*--
__author__ = 'gaoxingsheng'

import os
import sys
import json
from PIL import Image

input_image = sys.argv[1]

filepath = os.path.dirname(input_image)
filename = os.path.basename(input_image)

out_path = filepath + "/out"
basename = filename.split('.')[0]
out_image_file = out_path + "/" + filename
out_json_file = out_path + "/" + basename + ".json"

print filepath
print filename

padding = 2


# 简单的切图

def check_valid_space(size, space):
    """
    检查空间是否能够正好盛放
    :param size:
    :param space:
    :return: 是否可以，是否旋转
    """
    print "check_valid_space size == ", size
    print "check_valid_space space == ", space
    if size[0] <= space[0] and size[1] <= space[1]:
        return True, False
    elif size[0] <= space[1] and size[1] <= space[0]:
        return True, True
    else:
        return False, False


def get_right_size(size):
    """
    获取能够盛放图片需要的最下的尺寸
    :param size:
    :return:
    """
    area = size[0] * size[1]

    width = 1
    height = 1
    while width * height < area:
        if width > height:
            height = width
        else:
            width = width * 2
    return width, height


def save_json(name, data):
    """
    保存文件 用于保存生成的json文件
    :param name:
    :param data:
    :return:
    """
    out = open(name, 'w+')
    out.write(data)
    out.close()


input_im = Image.open(input_image)

out_width, out_height = get_right_size(input_im.size)

out_image = Image.new(input_im.mode, (out_width, out_height))

width = input_im.size[0]
height = input_im.size[1]
startx = 0

free = {
    "x": 0,
    "y": 0,
    "width": out_width,
    "height": out_height,
}

last = {
    "x": 0,
    "y": 0,
    "width": width,
    "height": height,
}

out_json = {"count": 0}

while width > 0:
    cut_width = out_width
    if width > out_width:
        width = width - out_width
    else:
        cut_width = width
        width = 0

    starty = 0
    temp_height = height
    while temp_height > 0:
        cut_height = out_height
        if temp_height > out_height:
            temp_height = temp_height - out_height
        else:
            cut_height = temp_height
            temp_height = 0

        print "free === ", free
        flag, rotate = check_valid_space((cut_width, cut_height), (free['width'], free['height']))
        assert(flag == True, "simple convert cannot convert this image")

        box = (startx, starty, startx + cut_width, starty + cut_height)
        region = input_im.crop(box)
        if rotate == True:
            region = region.transpose(Image.ROTATE_90)
            cut_height = cut_width

        rsize = region.size
        output_box = (free['x'], free['y'], free['x'] + rsize[0], free['y'] + rsize[1])

        out_image.paste(region, output_box)
        free['y'] = free['y'] + cut_height + padding
        free['height'] = free['height'] - cut_height - padding
        out_json['count'] = out_json['count'] + 1
        out_json[out_json['count']] = {"x": output_box[0], "y": output_box[1], "width": output_box[2], "height": output_box[3], "rotate": rotate}
        out_json[out_json['count'] + "_"] = {"x": box[0], "y": box[1], "width": box[3], "height": box[3],}
        starty = starty + cut_height


    startx = startx + cut_width
    # free['x'] = free['x'] + cut_height + padding
    # free['width'] = free['width'] - cut_height - padding


# if free['width'] > 0:
#     out_width = out_width - free['width']
# if free['y'] > 0:
#     out_height = free['y']
#
# print("real_size === ", (out_width, out_height))
# out_image.resize((out_width, out_height))

if not os.path.isdir(out_path):
    os.mkdir(out_path)

out_json['image'] = filename
data = json.dumps(out_json)
save_json(out_json_file, data)
out_image.save(out_image_file)


import os
from PIL import Image

im = Image.open("ui_jinjichang_beijing.png")


def get_right_size(size):
    area = size[0] * size[1]

    width = 1
    height = 1
    while width * height < area:
        if width > height:
            height = width
        else:
            width = width * 2
    return width, height

out_width, out_height = get_right_size(im.size)

# print out_width, out_height

width = im.size[0]
height = im.size[1]


# region = im.crop(box)

out_image = Image.new("RGB", (out_width, out_height))

startx = 0
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
        print cut_width, cut_height
        box = (startx, starty, startx + cut_width, starty + cut_height)
        print box
        region = im.copy().crop(box)
        region.save(str(startx) + ".png")
        out_image.paste(region, box)
        starty = starty + cut_height

    startx = startx + cut_width

out_image.save("out.png")


def check_valid_space(size, space):
    """
    检查空间是否能够正好盛放
    :param size: 
    :param space: 
    :return: 是否可以，是否旋转
    """

    if size[0] < space[0] and size[1] < space[1]:
        return True, 1
    else if size[0] < space[1] and size[1] < space[0]:
        return True, -1
    else:
        return False


def splitspr(input, out, last, free):

    # 检查是否有能盛放的空间
    for space in free:
        flag, rolate = check_valid_space(last, space)
        if flag:
            print "valid"
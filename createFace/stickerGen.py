import face_recognition
import numpy as np
import cv2
from PIL import Image, ImageDraw


def get_face_line(image):
    face_location = face_recognition.face_locations(image, model='cnn')
    face_landmarks_list = face_recognition.face_landmarks(image, face_locations=face_location)
    face_line = list()
    for face_landmarks in face_landmarks_list:
        chin = face_landmarks['chin']
        left_eyebrow = face_landmarks['left_eyebrow']
        right_eyebrow = face_landmarks['right_eyebrow']
        chin.reverse()
        list_all = left_eyebrow + right_eyebrow + chin + [left_eyebrow[0]]
        face_line.append(list_all)
    return face_line


def get_face_location(image):
    face_line = get_face_line(image)
    if len(face_line) == 0:
        return None
    pil_image = Image.fromarray(image)
    d = ImageDraw.Draw(pil_image)
    d.line(face_line[0], width=2)
    pil_image = np.array(pil_image)
    # pil_image = cv2.cvtColor(np.asarray(pil_image), cv2.COLOR_RGB2BGR)
    return pil_image


def create_expression(img, background):
    face_line = get_face_line(img)
    mask = np.ones(img.shape, dtype=np.uint8) * 255
    mask = Image.fromarray(mask)
    q = ImageDraw.Draw(mask)
    q.line(face_line[0], width=10, fill=(0, 0, 0))

    # 生成掩膜
    mask = np.array(mask)
    h, w = mask.shape[:2]  # 读取图像的宽和高
    mask_flood = np.zeros([h + 2, w + 2], np.uint8)  # 新建图像矩阵  +2是官方函数要求
    cv2.floodFill(mask, mask_flood, (1, 1), (0, 0, 0))  # 这里使用OpenCV的水漫填充，把轮廓外部涂成黑色，内部为白色

    # 用一个5*5的卷积核对掩膜进行闭运算，去掉噪声
    # erosion的迭代次数2次是我试出来的，感觉效果比较好
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=2)
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    mask = dilation

    # 重新读入原图，框出RIO，交给OpenCV处理
    image = img
    image[mask == 0] = 255
    # # 将处理过的图片变为灰度图
    GrayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # 二值化处理
    ret, image = cv2.threshold(GrayImage, 105, 255, cv2.THRESH_BINARY)

    # 用一个2*2的卷积核对RIO进行多次腐蚀膨胀处理，去掉噪声，这里进行多少次膨胀腐蚀要结合图片效果来进行
    kernel = np.ones((2, 2), np.uint8)
    dilation = cv2.dilate(image, kernel, iterations=3)
    erosion = cv2.erode(dilation, kernel, iterations=1)
    dilation = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(dilation, kernel, iterations=1)

    # 这是表情需要截取的部分，不同图这个地方的参数不同
    left = min(face_line[0], key=lambda x: x[0])[0]
    right = max(face_line[0], key=lambda x: x[0])[0]
    top = min(face_line[0], key=lambda x: x[1])[1]
    bottom = max(face_line[0], key=lambda x: x[1])[1]
    image = image[top:bottom, left:right]

    box = (160, 155, 460, 400)  # 背景图要被替换的部分
    base_img = Image.open(background)
    image = Image.fromarray(image)
    image = image.resize((box[2] - box[0], box[3] - box[1]))  # 缩放表情，贴入的表情必须和背景被替换的地方大小相同
    base_img.paste(image, box)

    # 这是为了让图片看起来更自然，而且本身表情就是黑白的，所以对图片再进行一次二值化处理
    image = np.array(base_img)
    GrayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_BINARY)

    # 这里继续膨胀腐蚀，让图片更好看一点
    erosion = cv2.erode(image, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    erosion = cv2.erode(dilation, kernel, iterations=1)
    image = erosion
    return image

"""Graphics utilities."""

import cv2

import numpy as np

from eigenfaces import EigenFaces


class Image:
    """Image manipulation class wrapping some opencv functions."""
    def __init__(self, ocv_image):
        """Wrap opencv image."""
        self._img = ocv_image
        self._face_cascade = 'haarcascade_frontalface_default.xml'

    def gray(self):
        """
        Returns:
            new grayscale image.
        """
        return Image(cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY))#_img不受影响

    def faces(self):
        return map(lambda rect: self.cut(rect[0], rect[1], rect[2], rect[3]),
            self.face_areas())

    def cut(self, x, y, width, height):## opencv中 图片左上角为原点 且x,y与实际相反即（y,x）
        return Image(self._img[y:y + height, x:x + width])

    def scale(self, width, height):
        return Image(cv2.resize(self._img, (width, height)))

    def draw_rect(self, x, y, width, height):# 根据左上角到右下角对角线画框
        cv2.rectangle(self._img, (x, y), (x + width, y + height), (0, 255, 0), 2)#作用于_img

    def save_to(self, path):
        cv2.imwrite(path, self._img)

    def to_numpy_array(self):
        return np.array(self._img, dtype=np.uint8).flatten()## numpy数组拼接

    def put_text(self, text, x, y):
        cv2.putText(self._img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 2,
            (0, 255, 0), 2)

    def face_areas(self):## 读取LBF特征检测器的xml文件用于检测 return(x, y, w, h)
        return cv2.CascadeClassifier('haarcascade_frontalface_default.xml') \
            .detectMultiScale(self._img, scaleFactor=1.2, minNeighbors=5,
                minSize=(50, 50), flags=cv2.CASCADE_SCALE_IMAGE)

    def show(self):
        cv2.imshow('', self._img)
        cv2.waitKey(0)


def load_image_from(path):
    return Image(cv2.imread(path))


class FaceDetector:
    def __init__(self):
        self.clf = EigenFaces()
        self.clf.train('training_images')# 训练

    def show(self, image, wait=True):
        for (x, y, w, h) in image.face_areas():
            image.draw_rect(x, y, w, h)

            face = image.cut(x, y, w, h).gray().scale(100, 100).to_numpy_array()
            predicted_name = self.clf.predict_face(face)# get 检测结果

            image.put_text(predicted_name, x + 20, y + h + 45)

        cv2.imshow('', image._img)
        if wait:
            cv2.waitKey(0)

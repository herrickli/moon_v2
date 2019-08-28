import cv2


class net:
    def __init__(self):
        pass

    def predict(self, path):
        obj = 'knife'
        score = 0.9
        bndbox = [1,1,100,100]
        return obj, score, bndbox
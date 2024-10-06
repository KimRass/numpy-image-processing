import cv2
import numpy as np
from PIL import Image


def round_half_up(x):
    return int(x + 0.5) if x > 0 else int(x - 0.5)


def show_image(x):
    Image.fromarray(cv2.cvtColor(x, cv2.COLOR_BGR2RGB)).show()


if __name__ == "__main__":
    img_path = "/Users/jongbeomkim/Downloads/golden_retriever_original.jpg"
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)

    kernel = np.ones((5, 5), np.uint8)
    dilated_img = cv2.dilate(img, kernel, iterations=1)
    Image.fromarray(cv2.cvtColor(dilated_img, cv2.COLOR_BGR2RGB)).show()

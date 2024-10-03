# References:
    # https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html

import cv2
import numpy as np


def bin_thresh(img, thresh, max_val, inv=False):
    """
    If `inv=False`, the output is same as `cv2.threshold(
        img, thresh=thresh, maxval=max_val, type=cv2.THRESH_BINARY,
    )[1]` and if else, `cv2.threshold(
        img, thresh=thresh, maxval=max_val, type=cv2.THRESH_BINARY_INV,
    )[1]`
    """
    if not inv:
        return np.where(img > thresh, max_val, 0).astype(np.uint8)
    else:
        return np.where(img > thresh, 0, max_val).astype(np.uint8)


def ada_thresh_mean(img, max_val, block_size, const, pad=False):
    """
    The threshold value is the mean of the neighborhood area minus the
    constant `const`.
    """
    assert block_size % 2 == 1 and block_size > 1

    new_img = np.zeros_like(img)
    if pad:
        padded_img = np.pad(
            # img, pad_width=block_size // 2, mode="symmetric",
        )
    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            if pad:
                loc_region = padded_img[
                    row: row + block_size, col: col + block_size, ...,
                ]
            else:
                loc_region = img[
                    max(0, row - block_size // 2): row + block_size // 2 + 1,
                    max(0, col - block_size // 2): col + block_size // 2 + 1,
                    ...,
                ]
            loc_thresh = np.mean(loc_region) - const
            if img[row, col, ...] > loc_thresh:
                new_img[row, col, ...] = max_val
            else:
                new_img[row, col, ...] = 0
    return new_img


if __name__ == "__main__":
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # img = img[: 10, : 7, ...]
    const = 2
    max_val = 255
    block_size = 5
    out1= ada_thresh_mean(
        img, max_val=max_val, block_size=block_size, const=const,
    )
    show_image(out1)

    out2 = cv2.adaptiveThreshold(
        src=img,
        maxValue=max_val,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=block_size,
        C=const,
    )
    out1
    out2
    np.array_equal(out1, out2)

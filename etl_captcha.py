import cv2
from PIL import Image

methods = [
    cv2.THRESH_BINARY
#    cv2.THRESH_BINARY_INV,
#    cv2.THRESH_TRUNC,
#    cv2.THRESH_TOZERO,
#    cv2.THRESH_TOZERO_INV
]

for i in range(10):

    image = cv2.imread(f'test_data/captcha_screenshot_{i+1}.png')

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    for method in methods:
        _, image_resolved = cv2.threshold(gray_image, 127, 255, method or cv2.THRESH_OTSU)

        cv2.imwrite(f'test_data/results_tests/captcha{i}.png', image_resolved)


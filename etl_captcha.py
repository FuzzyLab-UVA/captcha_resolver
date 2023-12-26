import cv2

DATA_SIZE = 1000


def remove_border(img, border_size):
    return img[border_size:-border_size, border_size:-border_size]

def etl_images(origin:str, destination:str):
    methods = [cv2.THRESH_BINARY] 

    for i in range(DATA_SIZE):
        image = cv2.imread(f'{origin}/captcha_screenshot_{i+1}.png')
        print(origin + f'{origin}/captcha_screenshot_{i+1}.png')

        image_without_border = remove_border(image, border_size=10) 

        gray_image = cv2.cvtColor(image_without_border, cv2.COLOR_BGR2GRAY)

        for method in methods:
            _, image_resolved = cv2.threshold(gray_image, 127, 255, method or cv2.THRESH_OTSU)
            cv2.imwrite(f'{destination}/captcha{i}.png', image_resolved)



etl_images('./data', './transformed_data')

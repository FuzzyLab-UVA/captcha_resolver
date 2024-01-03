import os

import cv2


def adjust_kernel_size(image_dim):
    size = max(1, int(min(image_dim) / 100)) 
    return (size, size)

def is_near_edge(x, y, w, h, img_width, img_height, edge_margin):
    return (x < edge_margin or x+w > img_width - edge_margin)

current_dir = os.getcwd()
print('Diretório de trabalho atual:', current_dir)

dir_path = os.path.join(current_dir, 'transformed_data')

if not os.path.exists(dir_path):
    print(f"O diretório não foi encontrado: {dir_path}")
else:
    files = os.listdir(dir_path)
    images = [os.path.join(dir_path, f) for f in files if f.endswith('.png')]

    if not os.path.exists('./letters'):
        os.makedirs('./letters')
    if not os.path.exists('./identify'):
        os.makedirs('./identify')

    for image in images:
        print(f"Processando imagem: {image}")
        img = cv2.imread(image)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
        img_thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        
        kernel_size = adjust_kernel_size(img.shape[:2])
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
        img_morph = cv2.morphologyEx(img_thresh, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(img_morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        img_height, img_width = img_morph.shape[:2]
        edge_margin = 10 

        letter_region = []

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            if area > 100 or is_near_edge(x, y, w, h, img_width, img_height, edge_margin):
                letter_region.append((x, y, w, h))

        print(f"Número de regiões encontradas: {len(letter_region)}")

        if len(letter_region) > 6: 
            print(f"Número incorreto de regiões encontradas: {len(letter_region)}")
            continue

        final_image = cv2.merge([img_morph] * 3)

        for i, rectangle in enumerate(sorted(letter_region, key=lambda x: x[0])):
            print(f"Retângulo: {rectangle}")
            print(f"Índice: {i}")
            x, y, w, h = rectangle
            img_letter = img_morph[y:y+h+2, x:x+w+2]
            archive_name = os.path.basename(image).replace('.png', f'_letra{i}.png')
            letter_image_path = os.path.join('./letters', archive_name)
            cv2.imwrite(letter_image_path, img_letter)
            cv2.rectangle(final_image, (x-2, y-2), (x+w+2, y+h+2), (0, 255, 0), 1)

        archive_name = os.path.basename(image)
        identify_image_path = os.path.join('./identify', archive_name)
        cv2.imwrite(identify_image_path, final_image)

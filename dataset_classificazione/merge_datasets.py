import cv2
import os
import ntpath
import json

def check_image_equal(path_image_1, path_image_2):
    image_1 = cv2.imread(path_image_1)
    image_2 = cv2.imread(path_image_2)

    if not(image_1.shape == image_2.shape):
        return False

    difference = cv2.subtract(image_1, image_2)
    b, g, r = cv2.split(difference)
    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        return True

    return False

def brand_and_materials_equal(file_path_1, file_path_2):
    head_1, file_name_1 = ntpath.split(file_path_1)
    head_2, file_name_2 = ntpath.split(file_path_2)
    if head_1 == head_2:
        return False

    split_1 = file_name_1.split('_')
    split_2 = file_name_2.split('_')

    brand_1 = split_1[1]
    brand_2 = split_2[1]
    if not brand_1 == brand_2:
        return False

    material_1 = split_1[2]
    material_2 = split_2[2]
    if not material_1 == material_2:
        return False

    return True

def create_dataset(paths):

    dataset_list = []

    for path in paths:
        images_list = os.listdir(path)
        for image_name in images_list:
            image_path = os.path.join(path, image_name)
            print(image_path)
            equals = False

            if len(dataset_list) == 0:
                dataset_list.append(image_path)

            for other_image_path in dataset_list:
                if brand_and_materials_equal(image_path, other_image_path):
                    if check_image_equal(image_path, other_image_path):
                        equals = True
                        break

            if not equals:
                dataset_list.append(image_path)

    return dataset_list

def save_dataset_list(dataset_list, path_where_save):
    with open(path_where_save, 'w') as file:
        json.dump(dataset_list, file)
        file.close()

if __name__ == "__main__":

    path_dataset_en_cn_men = "/dataset_mytheresa/en-cn/men/"
    path_dataset_en_cn_women = "/dataset_mytheresa/en-cn/women/"

    path_dataset_en_it_men = "/dataset_mytheresa/en-it/men/"
    path_dataset_en_it_women = "/dataset_mytheresa/en-it/women/"

    path_dataset_en_jp_men = "/dataset_mytheresa/en-jp/men/"
    path_dataset_en_jp_women = "/dataset_mytheresa/en-jp/women/"

    path_dataset_en_kr_men = "/dataset_mytheresa/en-kr/men/"
    path_dataset_en_kr_women = "/dataset_mytheresa/en-kr/women/"

    path_dataset_en_us_men = "/dataset_mytheresa/en-us/men/"
    path_dataset_en_us_women = "/dataset_mytheresa/en-us/women/"

    paths_men = [path_dataset_en_cn_men, path_dataset_en_it_men, path_dataset_en_jp_men, path_dataset_en_kr_men, path_dataset_en_us_men]
    paths_women = [path_dataset_en_cn_women, path_dataset_en_it_women, path_dataset_en_jp_women, path_dataset_en_kr_women, path_dataset_en_us_women]

    path_dataset_men = "/dataset_classificazione/men.json"
    path_dataset_women = "/dataset_classificazione/women.json"

    dataset_list = create_dataset(paths_women)
    save_dataset_list(dataset_list, path_dataset_women)

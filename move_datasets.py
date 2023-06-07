import os
import cv2
import ntpath
import json

if __name__ == "__main__":

    path_dataset_men = "/Users/andreacivitarese/PycharmProjects/CVandDL/dataset_classificazione/men.json"
    path_dataset_women = "/Users/andreacivitarese/PycharmProjects/CVandDL/dataset_classificazione/women.json"
    path_folder_men = "/Users/andreacivitarese/PycharmProjects/CVandDL/dataset_classificazione/men/"
    path_folder_women = "/Users/andreacivitarese/PycharmProjects/CVandDL/dataset_classificazione/women/"

    with open(path_dataset_men, 'r') as file_men:
        list_men_images = json.load(file_men)
        file_men.close()

    with open(path_dataset_women, 'r') as file_women:
        list_women_images = json.load(file_women)
        file_women.close()

    for index, file_path in enumerate(list_men_images):
        img_data = cv2.imread(file_path)
        head, image_name = ntpath.split(file_path)
        img_index, img_brand, img_materials = image_name.split('_')
        img_name = str(index) + '_' + img_brand+ '_' + img_materials
        image_path = os.path.join(path_folder_men, img_name)
        cv2.imwrite(image_path, img_data)
        #with open(image_path, 'wb') as handler:
         #   handler.write(img_data)
          #  handler.close()

    for index, file_path in enumerate(list_women_images):
        img_data = cv2.imread(file_path)
        head, image_name = ntpath.split(file_path)
        img_index, img_brand, img_materials = image_name.split('_')
        img_name = str(index+len(list_men_images)) + '_' + img_brand+ '_' + img_materials
        image_path = os.path.join(path_folder_women, img_name)
        cv2.imwrite(image_path, img_data)
        #with open(image_path, 'wb') as handler:
         #   handler.write(img_data)
          #  handler.close()
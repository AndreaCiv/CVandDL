import os
import shutil
from xml.etree import ElementTree as et

'''
    Il nostro dataset risulta essere l'unione di due dataset per la detection di loghi. In particolare:
    - LogoDet-3K (https://www.kaggle.com/datasets/lyly99/logodet3k)
    - QMUL-OpenLogo (https://hangsu0730.github.io/qmul-openlogo/) 
    La scelta e l'unione dei due dataset hann implicato una pre lavorazione al fine di avere un dataset con
    i dati a noi utili e soprattutto dati uniformi.
'''

'''
    Funzioni utilizzate per pulire dataset QMUL-OpenLogo
'''

def delete_annotations():
    annotations_path = "C:/Users/gioel/Desktop/openlogo(2)/openlogo/Annotations"
    annotations_list = os.listdir(annotations_path)
    for file in annotations_list:
        file_name = file.split(".")[0].lower()
        print(file_name)

        if "louisvuitton" not in file_name and "prada" not in file_name and "gucci" not in file_name and "hermes" not in file_name:
            os.remove(annotations_path + "/" + file)


def delete_images():
    images_path = "C:/Users/gioel/Desktop/openlogo(2)/openlogo/JPEGImages"
    images_list = os.listdir(images_path)
    print(images_list[0])
    for file in images_list:
        file_name = file.split(".")[0].lower()

        if "louisvuitton" not in file_name and "prada" not in file_name and "gucci" not in file_name and "hermes" not in file_name:
            os.remove(images_path + "/" + file)


def delete_class_sep():
    class_sep_path = "C:/Users/gioel/Desktop/openlogo(2)/openlogo/ImageSets/class_sep"
    class_sep_list = os.listdir(class_sep_path)
    print(class_sep_list[0])
    for file in class_sep_list:
        file_name = file.split("_")[0].lower()

        if "lv" not in file_name and "prada" not in file_name and "gucci" not in file_name and "hermes" not in file_name:
            os.remove(class_sep_path + "/" + file)


def create_dataset():
    images_path = "C:/Users/gioel/Desktop/openlogo(2)/openlogo/JPEGImages"
    annotations_path = "C:/Users/gioel/Desktop/openlogo(2)/openlogo/Annotations"

    gucci_train_path = "C:/Users/gioel/Desktop/openlogo(2)/openlogo/ImageSets/class_sep/gucci_train.txt"
    gucci_test_path = "C:/Users/gioel/Desktop/openlogo(2)/openlogo/ImageSets/class_sep/gucci_test.txt"

    hermes_train_path = "C:/Users/gioel/Desktop/openlogo(2)/openlogo/ImageSets/class_sep/hermes_train.txt"
    hermes_test_path = "C:/Users/gioel/Desktop/openlogo(2)/openlogo/ImageSets/class_sep/hermes_test.txt"

    prada_train_path = "C:/Users/gioel/Desktop/openlogo(2)/openlogo/ImageSets/class_sep/prada_train.txt"
    prada_test_path = "C:/Users/gioel/Desktop/openlogo(2)/openlogo/ImageSets/class_sep/prada_test.txt"

    lv_train_path = "C:/Users/gioel/Desktop/openlogo(2)/openlogo/ImageSets/class_sep/lv_train.txt"
    lv_test_path = "C:/Users/gioel/Desktop/openlogo(2)/openlogo/ImageSets/class_sep/lv_test.txt"

    destination_path = "C:/Users/gioel/Desktop/dataset"

    # Gucci
    gucci_train = open(gucci_train_path, 'r')
    gucci_train_images = gucci_train.read().splitlines()
    for image in gucci_train_images:
        shutil.move(images_path + "/" + image + ".jpg", destination_path + "/" + "gucci_train")
        shutil.move(annotations_path + "/" + image + ".xml", destination_path + "/" + "gucci_train")

    gucci_test = open(gucci_test_path, 'r')
    gucci_test_images = gucci_test.read().splitlines()
    for image in gucci_test_images:
        shutil.move(images_path + "/" + image + ".jpg", destination_path + "/" + "gucci_test")
        shutil.move(annotations_path + "/" + image + ".xml", destination_path + "/" + "gucci_test")

    # Prada
    prada_train = open(prada_train_path, 'r')
    prada_train_images = prada_train.read().splitlines()
    for image in prada_train_images:
        shutil.move(images_path + "/" + image + ".jpg", destination_path + "/" + "prada_train")
        shutil.move(annotations_path + "/" + image + ".xml", destination_path + "/" + "prada_train")

    prada_test = open(prada_test_path, 'r')
    prada_test_images = prada_test.read().splitlines()
    for image in prada_test_images:
        shutil.move(images_path + "/" + image + ".jpg", destination_path + "/" + "prada_test")
        shutil.move(annotations_path + "/" + image + ".xml", destination_path + "/" + "prada_test")

    # Hermes
    hermes_train = open(hermes_train_path, 'r')
    hermes_train_images = hermes_train.read().splitlines()
    for image in hermes_train_images:
        shutil.move(images_path + "/" + image + ".jpg", destination_path + "/" + "hermes_train")
        shutil.move(annotations_path + "/" + image + ".xml", destination_path + "/" + "hermes_train")

    hermes_test = open(hermes_test_path, 'r')
    hermes_test_images = hermes_test.read().splitlines()
    for image in hermes_test_images:
        shutil.move(images_path + "/" + image + ".jpg", destination_path + "/" + "hermes_test")
        shutil.move(annotations_path + "/" + image + ".xml", destination_path + "/" + "hermes_test")

    # Louis Vuitton
    lv_train = open(lv_train_path, 'r')
    lv_train_images = lv_train.read().splitlines()
    for image in lv_train_images:
        shutil.move(images_path + "/" + image + ".jpg", destination_path + "/" + "louisVuitton_train")
        shutil.move(annotations_path + "/" + image + ".xml", destination_path + "/" + "louisVuitton_train")

    lv_test = open(lv_test_path, 'r')
    lv_test_images = lv_test.read().splitlines()
    for image in lv_test_images:
        shutil.move(images_path + "/" + image + ".jpg", destination_path + "/" + "louisVuitton_test")
        shutil.move(annotations_path + "/" + image + ".xml", destination_path + "/" + "louisVuitton_test")

'''
    Funzioni per rinominare correttamente l'intero dataset (unione dei due precedenti), utilizzando la seguente 
    nomenclatura:
    "Idprogressivo_NOMEBRAND"
    In seguito è stato necessario modificare le etichette, in quanto sono cambiati nomi file e nomi delle cartelle che 
    contenevano questi ultimi.
'''

def change_names():
    dataset_path = "C:/Users/gioel/Desktop/dataset"
    brands_list = sorted(os.listdir(dataset_path))
    for brand in brands_list:
        index = 0
        for item in sorted(os.listdir(os.path.join(dataset_path, brand))):
            if item.split(".")[1].lower() in ["jpg", "jpeg"]:
                os.rename(dataset_path+"/"+brand+"/"+item, dataset_path+"/"+brand+"/"+str(index)+"_"+brand+".jpg")
                os.rename(dataset_path + "/" + brand + "/" + item.split(".")[0]+".xml",
                          dataset_path + "/" + brand + "/" + str(index) + "_" + brand + ".xml")
                tree = et.parse(dataset_path + "/" + brand + "/" + str(index) + "_" + brand + ".xml")
                root = tree.getroot()
                for child in root:
                    if child.tag == "filename":
                        child.text = str(index) + "_" + brand + ".jpg"
                    if child.tag == "object":
                        for child2 in child:
                            if child2.tag == "name":
                                child2.text = brand
                tree.write(dataset_path + "/" + brand + "/" + str(index) + "_" + brand + ".xml")
                index += 1

if __name__ == "__main__":
    #delete_annotations()
    #delete_images()
    #delete_class_sep()
    #create_dataset()
    change_names()

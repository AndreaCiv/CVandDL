import requests
import json


def get_data(file_name_json):
    with open(file_name_json, 'r') as file:
        json_data = json.load(file)
        file.close()
        data = []
        for index, item in enumerate(json_data):
            try:
                materiale = item['materials']['material']
                materiali = materiale.split(',')
                materials = ''
                for indice, mat in enumerate(materiali):
                    mat = mat.replace(' ', '', 1)
                    mat = mat.replace(' ', '-')
                    if indice == 0:
                        materials = materials + mat
                    else:
                        materials = materials + '+' + mat
                titolo = item['title']
                url_img = item['img']
                brand = item['brand']
                brand = brand.replace(' ', '+')
                bag = {'index': index, 'brand': brand, 'titolo': titolo, 'url_img': url_img, 'material': materials}
                data.append(bag)
            except:
                print('********************************************')
                print('numero '+ str(index)+ ' materiali non presenti')
                print('********************************************')
                print()
                continue
    return data

def download_images(path_dataset, data):
    for item in data:
        print(item['index'])
        img_data = requests.get(item['url_img']).content
        file_name = path_dataset + str(item['index']) + '_' + item['brand'] + '_' + item['material'] + '.jpg'
        file_name = file_name.replace(' ', '+')
        file_name = file_name.replace(',', '')
        print(file_name)
        with open(file_name, 'wb') as handler:
            handler.write(img_data)
            handler.close()


if __name__ == "__main__":

    file_name_en_it_men = "/Users/andreacivitarese/PycharmProjects/CVandDL/dataset_non_completo_cv/en-it/men/en-it_men_mytheresa.json"
    file_name_en_it_women = "/Users/andreacivitarese/PycharmProjects/CVandDL/dataset_non_completo_cv/en-it/women/en-it_women_mytheresa.json"

    path_dataset_en_it_men = "/Users/andreacivitarese/PycharmProjects/CVandDL/dataset_mytheresa/en-it/men/"
    path_dataset_en_it_women = "/Users/andreacivitarese/PycharmProjects/CVandDL/dataset_mytheresa/en-it/women/"

    data = get_data(file_name_en_it_men)
    download_images(path_dataset_en_it_men, data)


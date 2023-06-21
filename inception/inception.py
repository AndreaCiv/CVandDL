import ntpath
import os
import numpy as np
import tensorflow as tf
import sklearn
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.callbacks import ModelCheckpoint
import pandas as pd
from codecarbon import track_emissions

@track_emissions()
def train_and_test_model(X_train, X_valid, X_test, Y_train, Y_valid, Y_test, list_possible_materials, layers_to_not_freeze,
                         dropout, learning_rate, batch_size, number_of_epochs, pooling, weights_directory, results_directory, test_directory):
    # definizione del modello di rete neurale
    print("Modello con parametri:"+
          "\nlayers to not freeze = " + str(layers_to_not_freeze) +
          "\ndropout = " + str(dropout) +
          "\nlearning rate = " + str(learning_rate) +
          "\nbatch size = " + str(batch_size) +
          "\npooling = " + pooling
          )

    inception = tf.keras.applications.inception_v3.InceptionV3(
        input_shape=(224, 224, 3),  # Making the image into 3 Channel
        weights='imagenet',
        include_top=False,
        pooling=pooling
    )

    if layers_to_not_freeze == 0:
        for layer in inception.layers:
            layer.trainable = False
    else:
        for layer in inception.layers[:-layers_to_not_freeze]:
            layer.trainable = False

    model = tf.keras.Sequential()
    model.add(inception)
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(1024, activation='relu'))
    model.add(tf.keras.layers.Dropout(dropout))
    model.add(tf.keras.layers.Dense(512, activation='relu'))
    model.add(tf.keras.layers.Dropout(dropout))
    model.add(tf.keras.layers.Dense(10, activation='softmax'))
    model.summary()

    # definizione checkpoint per salvare pesi durante l'addestramento
    # ATTENZIONE AL NOME DEL FILE
    checkpoint = ModelCheckpoint(
        os.path.join(weights_directory, "weights_inception_notfrozen_" + str(layers_to_not_freeze) + "_lr_" + str(learning_rate) + "_dropout_" + str(dropout) + "_batch_size_" + str(batch_size) + "_pooling_" + pooling + ".h5"),
        verbose=1, monitor='val_loss', save_best_only=True)

    # compilazione del modello
    # ATTENZIONE AL LEARNING RATE
    model.compile(loss="categorical_crossentropy", metrics="Recall",
                  optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.9))

    # addestramento del modello
    # ATTENZIONE AL BATCH SIZE
    print("Inizio training")
    history = model.fit(np.asarray(X_train), np.asarray(Y_train), epochs=number_of_epochs, batch_size=batch_size,
                        validation_data=(X_valid, Y_valid), verbose=1, callbacks=[checkpoint], shuffle=True)

    # salvataggio della history dell'addestramento
    # ATTENZIONE AL NOME DEL FILE
    history_ = pd.DataFrame(history.history)
    with open(os.path.join(results_directory, "history_inception_notfrozen_" + str(layers_to_not_freeze) + "_lr_" + str(learning_rate) + "_dropout_" + str(dropout) + "_batch_size_" + str(batch_size) + "_pooling_" + pooling + ".json"),
              "w") as json_file:
        history_.to_json(json_file)

    # test del modello
    print("Inizio test")
    Y_pred = model.predict(X_test)
    Y_pred_class = np.argmax(Y_pred, 1)
    Y_pred_binary = []
    for prediction in Y_pred_class:
        array_prediction = np.zeros(10)
        array_prediction[prediction] = 1
        Y_pred_binary.append(array_prediction)

    classification_report = sklearn.metrics.classification_report(Y_test, np.asarray(Y_pred_binary), target_names=list_possible_materials)
    accuracy_score = "\naccuracy = " + str(sklearn.metrics.accuracy_score(Y_test, Y_pred_binary))
    text_file = open(os.path.join(test_directory, "test_inception_notfrozen_" + str(layers_to_not_freeze) + "_lr_" + str(learning_rate) + "_dropout_" + str(dropout) + "_batch_size_" + str(batch_size) + "_pooling_" + pooling + ".txt"), "w")
    n = text_file.write(classification_report + accuracy_score)
    text_file.close()


if __name__ == "__main__":
    input_shape = (224, 224)
    number_of_epochs = 50

    weights_directory = "/home/vrai/inception/weights"
    results_directory = "/home/vrai/inception/results"
    test_directory = "/home/vrai/inception/test"
    path_dataset_men = "/home/vrai/dataset_classificazione/men/"
    path_dataset_women = "/home/vrai/dataset_classificazione/women/"
    path_dataset_augmented_men = "/home/vrai/dataset_classificazione/augmented_men/"
    path_dataset_augmented_women = "/home/vrai/dataset_classificazione/augmented_women/"

    batch_sizes_to_try = [32]  # si potrebbe provare anche con 8
    learning_rates_to_try = [0.001]
    layers_not_freeze_to_try = [0]
    dropouts_to_try = [0.5]  # si potrebbe provare anche 0.3
    poolings_to_try = ['avg']



    # caricamento immagini per train, validation e test
    imgs_list_men = [os.path.join(path_dataset_men, img_name) for img_name in sorted(os.listdir(path_dataset_men))]
    imgs_list_women = [os.path.join(path_dataset_women, img_name) for img_name in
                       sorted(os.listdir(path_dataset_women))]
    imgs_list = imgs_list_men + imgs_list_women

    # caricamento dei files augmentati
    imgs_list_augmented_men = [os.path.join(path_dataset_augmented_men, img_name) for img_name in
                               sorted(os.listdir(path_dataset_augmented_men))]
    imgs_list_augmented_women = [os.path.join(path_dataset_augmented_women, img_name) for img_name in
                                 sorted(os.listdir(path_dataset_augmented_women))]
    imgs_list_augmented = imgs_list_augmented_men + imgs_list_augmented_women

    print("Numero totale immagini: " + str(len(imgs_list) + len(imgs_list_augmented)))
    print("Di cui augmentate: " + str(len(imgs_list_augmented)))

    imgs_array = []
    for file_path in imgs_list:
        img = cv2.imread(file_path)
        img = cv2.resize(img, input_shape)
        # preprocessing
        img = tf.keras.applications.inception_v3.preprocess_input(img)
        imgs_array.append(img)

    # caricamento immagini aumentate
    imgs_array_augmented = []
    for file_path in imgs_list_augmented:
        img = cv2.imread(file_path)
        img = cv2.resize(img, input_shape)
        # preprocessing
        img = tf.keras.applications.vgg16.preprocess_input(img)
        imgs_array_augmented.append(img)


    # creazione delle etichette delle immagini
    possible_materials = set()
    for image_path in imgs_list:
        head, image_name = ntpath.split(image_path)
        index, brand, material = image_name.split('_')
        possible_materials.add(material.split('.')[0])
    list_possible_materials = list(possible_materials)
    print("Numero possibili materiali: " + str(len(possible_materials)))
    print(list_possible_materials)

    labels = []
    for image_path in imgs_list:
        head, image_name = ntpath.split(image_path)
        index, brand, material = image_name.split('_')
        label = np.zeros(shape=len(possible_materials), dtype=float)
        materiale = material.split('.')[0]
        indice = list_possible_materials.index(materiale)
        label[indice] = 1
        labels.append(label)

    # label per le immagini augmentate
    labels_augmented = []
    for image_path in imgs_list_augmented:
        head, image_name = ntpath.split(image_path)
        index, brand, material = image_name.split('_')
        label = np.zeros(shape=len(possible_materials), dtype=float)
        materiale = material.split('.')[0]
        indice = list_possible_materials.index(materiale)
        label[indice] = 1
        labels_augmented.append(label)

    # print supporto per ogni classe
    supports_for_dataset = {}
    for vector in labels:
        label = ''
        for index, number in enumerate(vector):
            if number == 1:
                if label == '':
                    label = label + list_possible_materials[index]
                else:
                    label = label + '+' + list_possible_materials[index]
        try:
            supports_for_dataset[label] = supports_for_dataset[label] + 1
        except:
            supports_for_dataset[label] = 1
    for vector in labels_augmented:
        label = ''
        for index, number in enumerate(vector):
            if number == 1:
                if label == '':
                    label = label + list_possible_materials[index]
                else:
                    label = label + '+' + list_possible_materials[index]
        try:
            supports_for_dataset[label] = supports_for_dataset[label] + 1
        except:
            supports_for_dataset[label] = 1
    print(supports_for_dataset)

    # divisione dataset e label in train, validation e test
    images_array, labels_array = sklearn.utils.shuffle(imgs_array, labels, random_state=15)
    images_array_augmented, labels_array_augmented = sklearn.utils.shuffle(imgs_array_augmented, labels_augmented, random_state=15)
    Xtrain, X_test, Ytrain, Y_test = train_test_split(images_array, labels_array, test_size=0.10, random_state=15, stratify=labels_array)
    X_train, X_valid, Y_train, Y_valid = train_test_split(Xtrain, Ytrain, test_size=0.2, random_state=15, stratify=Ytrain)
    X_train = np.asarray(X_train + imgs_array_augmented)
    X_valid = np.asarray(X_valid)
    X_test = np.asarray(X_test)
    Y_train = np.asarray(Y_train + labels_array_augmented)
    Y_valid = np.asarray(Y_valid)
    Y_test = np.asarray(Y_test)

    for batch_size in batch_sizes_to_try:
        for learning_rate in learning_rates_to_try:
            for layers_to_not_freeze in layers_not_freeze_to_try:
                for dropout in dropouts_to_try:
                    for pooling in poolings_to_try:
                        train_and_test_model(X_train=X_train, X_valid=X_valid, X_test=X_test, Y_train=Y_train, Y_valid=Y_valid,
                                         Y_test=Y_test, list_possible_materials=list_possible_materials, layers_to_not_freeze=layers_to_not_freeze,
                                         dropout=dropout, learning_rate=learning_rate, batch_size=batch_size, number_of_epochs=number_of_epochs, pooling=pooling,
                                         weights_directory=weights_directory, results_directory=results_directory, test_directory=test_directory)

import urllib.request

import matplotlib.pyplot as plt
import numpy as np
import yaml
from PIL import Image
from keras_preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.python.keras.layers import AveragePooling2D, Flatten, Dense, Dropout
from tensorflow.python.keras.optimizer_v2.adam import Adam

from an_connector import ANConnector
from assets.messages import Messages
from database_connector import DatabaseConnector
from utils.image_utility import ImageUtility

an_connector = ANConnector()
config = yaml.load(open('config.yml'), Loader=yaml.FullLoader).get('attendanceboard')
database_connector = DatabaseConnector()


class Trainer:
    DATA_FILE = 'train-dump.yml'
    INIT_LR = 1e-4
    EPOCHS = 20
    BS = 32

    @staticmethod
    def train():
        print(Messages.TRAINER_START)

        data = []
        labels = []

        Trainer.insert_base_images()

        for person in an_connector.persons:
            for entry in database_connector.get(person.objectGUID):
                image = ImageUtility.bin_to_np_arr(entry['data'])
                data.append(image)
                labels.append(person.objectGUID)

        data = np.array(data, dtype='float32')
        labels = np.array(labels)

        lb = LabelBinarizer()
        labels = lb.fit_transform(labels)

        (trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.25, random_state=42)

        # If SSL exception occurs, run `Install Certificates.command` inside Applications/Python X
        aug = ImageDataGenerator(rotation_range=20, zoom_range=0.15, width_shift_range=0.2, height_shift_range=0.2,
                                 shear_range=0.15, horizontal_flip=True, fill_mode='nearest')
        base_model = MobileNetV2(weights='imagenet', include_top=False, input_tensor=Input(shape=(224, 224, 3)))

        head_model = base_model.output
        head_model = AveragePooling2D(pool_size=(7, 7))(head_model)
        head_model = Flatten(name='flatten')(head_model)
        head_model = Dense(128, activation='relu')(head_model)
        head_model = Dropout(0.5)(head_model)
        head_model = Dense(len(labels), activation='softmax')(head_model)

        model = Model(inputs=base_model.input, outputs=head_model)
        # print(model.summary())

        for layer in base_model.layers:
            layer.trainable = False

        print('Compiling model ... \n')
        opt = Adam(lr=Trainer.INIT_LR, decay=Trainer.INIT_LR / Trainer.EPOCHS)
        model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

        # Needs depth of 3, received 1
        print('Training head ... \n')
        head = model.fit(x=aug.flow(trainX, trainY, batch_size=Trainer.BS), validation_data=(testX, testY),
                         steps_per_epoch=len(trainX) // Trainer.BS, epochs=Trainer.EPOCHS)

        print('Evaluating network ... \n')
        pred_idxs = model.predict(testX, batch_size=Trainer.BS)
        pred_idxs = np.argmax(pred_idxs, axis=1)

        # print(classification_report(testY.argmax(axis=1), pred_idxs, target_names=lb.classes_))

        print('Saving mask detector model ... \n')
        model.save('mask_detector.model', save_format='h5')

        plt.style.use('ggplot')
        plt.figure()
        plt.plot(np.arange(0, Trainer.EPOCHS), head.history['loss'], label='train_loss')
        plt.plot(np.arange(0, Trainer.EPOCHS), head.history['val_loss'], label='valuation_loss')
        plt.plot(np.arange(0, Trainer.EPOCHS), head.history['accuracy'], label='train_acc')
        plt.plot(np.arange(0, Trainer.EPOCHS), head.history['val_accuracy'], label='valuation_acc')
        plt.title('Training Loss and Accuracy')
        plt.xlabel('Epoch #')
        plt.ylabel('Loss/Accuracy')
        plt.legend(loc='lower left')
        plt.savefig('plot.png')

        print(Messages.TRAINER_FINISH)

    @staticmethod
    def insert_base_images():
        for person in an_connector.persons:
            if person.imagePresent and database_connector.count(person.objectGUID) == 0:
                url = config.get('api') + '/person-images/' + person.objectGUID + '.jpg'
                image = Image.open(urllib.request.urlopen(url))

                # w, h = image.size
                # image = image.crop((w - h, 0, w, h))
                binary = ImageUtility.img_to_bin(image)

                if binary is not None:
                    database_connector.insert({'guid': person.objectGUID, 'data': binary})

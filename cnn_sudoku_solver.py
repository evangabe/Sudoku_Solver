import copy
import keras
from keras.layers import Activation
from keras.layers import Conv2D, BatchNormalization, Dense, Flatten, Reshape
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def get_model():
    model = keras.models.Sequential()

    model.add(Conv2D(64, kernel_size=(3,3), activation='relu', padding='same', input_shape=(9,9,1)))
    model.add(BatchNormalization())
    model.add(Conv2D(64, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(128, kernel_size=(1,1), activation='relu', padding='same'))

    model.add(Flatten())
    model.add(Dense(81*9))
    model.add(Reshape((-1, 9)))
    model.add(Activation('softmax'))

    return model


def get_data(file):

    data = pd.read_csv(file)

    feat_raw = data['quizzes']
    label_raw = data['solutions']

    feat = []
    label = []

    for i in feat_raw:

        x = np.array([int(j) for j in i]).reshape((9,9,1))
        feat.append(x)

    feat = np.array(feat)
    feat = feat/9
    feat -= .5

    for i in label_raw:

        x = np.array([int(j) for j in i]).reshape((81,1)) - 1
        label.append(x)

    label = np.array(label)

    del(feat_raw)
    del(label_raw)

    x_train, x_test, y_train, y_test = train_test_split(feat, label, test_size=0.2, random_state=42)

    return x_train, x_test, y_train, y_test

x_train, x_test, y_train, y_test = get_data("sudoku.csv")

model = get_model()
adam = keras.optimizers.Adam(lr=0.001)
model.compile(loss='sparse_categorical_crossentropy', optimizer=adam)
model.fit(x_train, y_train, batch_size=32, epochs=2)

sample = np.array([
    [0, 8, 0, 0, 3, 2, 0, 0, 1],
    [7, 0, 3, 0, 8, 0, 0, 0, 2],
    [5, 0, 0, 0, 0, 7, 0, 3, 0],
    [0, 5, 0, 0, 0, 1, 9, 7, 0],
    [6, 0, 0, 7, 0, 9, 0, 0, 8],
    [0, 4, 7, 2, 0, 0, 0, 5, 0],
    [0, 2, 0, 6, 0, 0, 0, 0, 9],
    [8, 0, 0, 0, 9, 0, 3, 0, 5],
    [3, 0, 0, 8, 2, 0, 0, 1, 0],
])

def map_forward(num):
    return (num/9) - 0.5

def map_back(num):
    return (num+0.5) * 9

def cnn_predict(arr):
    arr = map_forward(arr)
    arr_copy = np.copy(arr)

    while(1):
        out = model.predict(arr_copy.reshape((1, 9, 9, 1)))
        out = out.squeeze()

        pred = np.argmax(out, axis=1).reshape((9,9)) + 1
        prob = np.around(np.max(out, axis=1).reshape((9,9)), 2)

        arr_copy = map_back(arr_copy).reshape((9,9))
        mask = (arr_copy == 0)

        if mask.sum() == 0:
            break

        prob_new = prob*mask
        idx = np.argmax(prob_new)
        x, y = (idx//9), (idx%9)

        val = pred[x][y]
        arr_copy[x][y] = val
        arr_copy = map_forward(arr_copy)
    return pred

game = cnn_predict(sample)
print(game)

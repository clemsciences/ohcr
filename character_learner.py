"""
Experimental script
"""

import os

from learning import get_training_data

import skimage.io as skio
from sklearn import svm
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD


__author__ = 'Clément Besnier'


def learn_svm():
    training_data, x, y = get_training_data()
    clf = svm.SVC(decision_function_shape='ovo')
    clf.fit(x, y)
    im = skio.imread(os.path.join("test", "norm_100.jpg"))
    print(clf.predict([im.flatten()]))


def trial_nn():
    model = Sequential()
    # Dense(64) is a fully-connected layer with 64 hidden units.
    # in the first layer, you must specify the expected input data shape:
    # here, 20-dimensional vectors.
    model.add(Dense(64, input_dim=20, init='uniform'))
    model.add(Activation('tanh'))
    model.add(Dropout(0.5))
    model.add(Dense(64, init='uniform'))
    model.add(Activation('tanh'))
    model.add(Dropout(0.5))
    model.add(Dense(10, init='uniform'))
    model.add(Activation('softmax'))

    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy',
                  optimizer=sgd,
                  metrics=['accuracy'])
    # TODO load X_train, y_train, X_test and y_test
    l_training_data, x_train, y_train = get_training_data()
    model.fit(x_train, y_train, nb_epoch=20, batch_size=16)
    # score = model.evaluate(x_test, y_test, batch_size=16)


if __name__ == "__main__":
    learn_svm()

import tensorflow.keras as tf
import numpy as np
import os


class LSTM:

    def __init__(self, dataset):
        self.dataset = dataset

    def create(self):
        train_shape = (self.dataset.x_train.shape[1], self.dataset.x_train.shape[2])

        model = tf.models.Sequential()

        model.add(tf.layers.LSTM(128, input_shape=train_shape, return_sequences=True))
        model.add(tf.layers.LSTM(64, input_shape=train_shape))
        model.add(tf.layers.Dense(16, activation='relu'))
        model.add(tf.layers.Dense(1, activation='linear'))

        model.compile(loss='mean_squared_error', optimizer='rmsprop')

        return model

    def train(self, epochs, name):
        filename = 'model/' + name + '.h5'

        if os.path.exists(filename):
            print('LSTM: a trained model already exists with the name \'%s\'' % name)
            return

        model = self.create()
        model.fit(self.dataset.x_train,
                  self.dataset.y_train,
                  epochs=epochs,
                  batch_size=32,
                  shuffle=False)
        model.save(filename)

    def predict(self, name):
        filename = 'model/' + name + '.h5'

        if not os.path.exists(filename):
            print('LSTM: error locating model at %s' % filename)
            return

        model = tf.models.load_model(filename)

        print('LSTM: successfully loaded \'%s\'' % filename)

        y_pred = model.predict(self.dataset.x_test)

        rmse = np.sqrt(np.mean((y_pred - self.dataset.y_test)**2))
        print('rmse: %s' % rmse)

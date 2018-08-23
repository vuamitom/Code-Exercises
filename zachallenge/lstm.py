from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from keras.optimizers import Adam
import keras
from keras.callbacks import ModelCheckpoint
import numpy as np
import common
import constants

def create_model(n_classes, batch_size, stateful):
    model = Sequential()
    # model.add(Embedding(52, 128))
    params = dict(dropout=0.2, recurrent_dropout=0.2, 
        stateful=stateful)
    if stateful:
        params['batch_input_shape']=(batch_size, constants.NO_FRAME, constants.FEATURE_SIZE)
    model.add(LSTM(256, **params))
    model.add(Dense(n_classes, activation='sigmoid'))
    return model


def reshape_input(train_input):
    # to be (samples, time frame, features)
    shape = train_input.shape
    new_input = np.ndarray(shape=(shape[0], shape[2], shape[1]),
                         dtype=np.float64)
    for r in range(0, shape[0]):
        new_input[r,:,:] = train_input[r].T 
    return new_input

def train_and_predict(train_input, train_labels, test_input, test_labels):

    train_input, train_labels, valid_input, valid_labels = common.get_validation_data(train_input, train_labels)

    n_classes = common.get_n_classes('combined')
    train_labels = keras.utils.to_categorical(train_labels, n_classes)
    test_labels = keras.utils.to_categorical(test_labels, n_classes)
    valid_labels = keras.utils.to_categorical(valid_labels, n_classes)

    batch_size = 32
    stateful = False
    if stateful:
        train_size = int(batch_size * int(train_labels.shape[0] / batch_size))
        train_input = train_input[0:train_size, :,:]
        train_labels = train_labels[0:train_size]

        valid_size = int(batch_size * int(valid_labels.shape[0] / batch_size))
        valid_input = valid_input[0:valid_size, :,:]
        valid_labels = valid_labels[0:valid_size] 
    
    m = create_model(n_classes, batch_size, stateful)
    m.compile(loss='categorical_crossentropy',
              optimizer=Adam(lr=0.001),
              metrics=['accuracy'])
    m.fit(train_input, train_labels,
            batch_size=batch_size,
          epochs=15,
          verbose=1,
          validation_data=(valid_input, valid_labels))
    score, acc = m.evaluate(test_input, test_labels)
    print ('test score: ', score)
    print ('test accu : ', acc)

if __name__ == '__main__':
    train_input, train_labels, test_input, test_labels = common.get_combined_data()
    train_input = reshape_input(train_input)
    test_input = reshape_input(test_input)
    
    train_and_predict(train_input, train_labels, test_input, test_labels)

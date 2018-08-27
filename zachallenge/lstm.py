from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from keras.optimizers import Adam, RMSprop, Nadam, Adagrad
import keras
from keras.callbacks import ModelCheckpoint
from keras import regularizers
import numpy as np
import common
import constants
import os

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

def create_model_2(n_classes, batch_size, stateful):
    model = Sequential()
    # model.add(Embedding(52, 128))
    params = dict(dropout=0.4, recurrent_dropout=0.4, 
        stateful=stateful)
    if stateful:
        params['batch_input_shape']=(batch_size, constants.NO_FRAME, constants.FEATURE_SIZE)
    model.add(LSTM(256, **params))
    model.add(Dense(n_classes, activation='sigmoid', kernel_regularizer=regularizers.l1(0.01), activity_regularizer=regularizers.l1(0.01)))
    return model

def reshape_input(train_input):
    # to be (samples, time frame, features)
    shape = train_input.shape
    new_input = np.ndarray(shape=(shape[0], shape[2], 26),
                         dtype=np.float64)
    for r in range(0, shape[0]):
        new_input[r,:,:] = train_input[r][26:,:].T 
    return new_input

def reshape_input_var_length(train_input):
    # to be (samples, time frame, features)
    shape = train_input.shape
    new_input = np.ndarray(shape=(shape[0], shape[2], 26),
                         dtype=np.float64)
    for r in range(0, shape[0]):
        new_input[r,:,:] = train_input[r][26:,:].T 
    return new_input

def train_and_predict(train_input, train_labels, test_input, test_labels, checkpoint_filepath, model=None):

    train_input, train_labels, valid_input, valid_labels = common.get_validation_data(train_input, train_labels)

    n_classes = common.get_n_classes('combined')
    train_labels = keras.utils.to_categorical(train_labels, n_classes)
    test_labels = keras.utils.to_categorical(test_labels, n_classes)
    valid_labels = keras.utils.to_categorical(valid_labels, n_classes)

    batch_size = 16
    stateful = False
    if stateful:
        train_size = int(batch_size * int(train_labels.shape[0] / batch_size))
        train_input = train_input[0:train_size, :,:]
        train_labels = train_labels[0:train_size]

        valid_size = int(batch_size * int(valid_labels.shape[0] / batch_size))
        valid_input = valid_input[0:valid_size, :,:]
        valid_labels = valid_labels[0:valid_size] 
    
    m = model
    if m is None:
        m = create_model_2(n_classes, batch_size, stateful)
        m.compile(loss='categorical_crossentropy',
                  optimizer=Adam(),
                  metrics=['accuracy'])

    checkpoint = ModelCheckpoint(checkpoint_filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint] 

    m.fit(train_input, train_labels,
            batch_size=batch_size,
          epochs=30,
          verbose=1,
          callbacks=callbacks_list,
          validation_data=(valid_input, valid_labels))
    score, acc = m.evaluate(test_input, test_labels)
    print ('test score: ', score)
    print ('test accu : ', acc)

if __name__ == '__main__':
    train_input, train_labels, test_input, test_labels = common.get_combined_data()
    train_input = reshape_input(train_input)
    test_input = reshape_input(test_input)
    
    checkpoint_filepath = os.path.join(os.path.dirname(__file__), 'lstm_256_mfccs_delta_04dropout_run2.h5')
    start_over = False
    if start_over:
        train_and_predict(train_input, train_labels, test_input, test_labels, checkpoint_filepath, None)
    else:
        print ('retrain existing model ', checkpoint_filepath)
        model = keras.models.load_model(checkpoint_filepath)
        model.optimizer = Adagrad(lr=0.0001)#.lr.set_value(0.0005)
        # model.compile(loss='categorical_crossentropy',
        #           optimizer=Adam(lr=0.0005),
        #           metrics=['accuracy'])
        print (model.summary())
        # lstm = model.get_layer('dense_1')
        # # lstm.dropout = 0.5
        # # lstm.recurrent_dropout = 0.5
        # lstm.activity_regularizer=regularizers.l1_l2(l1=0.09, l2=0.09)
        # lstm.kernel_regularizer=regularizers.l1_l2(l1=0.01, l2=0.01)
        # print (lstm.get_config())
        
        # assert False


        # m = create_model_2(common.get_n_classes('combined'), 32, False)
        # m.compile(loss='categorical_crossentropy',
        #           optimizer=Adagrad(),
        #           metrics=['accuracy'])
        # for i in range(0, 2):
        #     print (m.layers[i])
        #     m.layers[i].trainable_weights = model.layers[i].trainable_weights
        #     m.layers[i].set_weights(model.layers[i].get_weights())

        checkpoint_filepath = os.path.join(os.path.dirname(__file__), 'lstm_256_mfccs_delta_04dropout_run3.h5')
        train_and_predict(train_input, train_labels, test_input, test_labels, checkpoint_filepath, model)

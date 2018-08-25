from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras import backend as K
from keras.optimizers import Adam, RMSprop
import keras
import common
import constants
import time
import os
from keras import regularizers
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
BATCH_SIZE = 32


def get_input_shape():
    feature_size = constants.FEATURE_SIZE
    frame_size = constants.NO_FRAME
    input_shape = None
    if K.image_data_format() == 'channels_first':
        input_shape = (1, feature_size, frame_size)
    else:
        input_shape = (feature_size, frame_size, 1)
    return input_shape

def reshape_input(x_train):
    feature_size = constants.FEATURE_SIZE
    frame_size = constants.NO_FRAME

    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, feature_size, frame_size)        
    else:
        x_train = x_train.reshape(x_train.shape[0], feature_size, frame_size, 1)
    return x_train

def create_model(input_shape, n_classes):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=input_shape))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
 
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_regularizer=regularizers.l1(0.001)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    # model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    # model.add(Conv2D(32, (3, 3), activation='relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.25))
 
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.01, l2=0.001)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
 
    model.add(Flatten())
    model.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l1(0.01)))
    model.add(Dropout(0.25))
    model.add(Dense(n_classes, activation='softmax', activity_regularizer=regularizers.l2(0.01)))
     
    return model

def create_model_4(input_shape, n_classes):
    model = Sequential()
    model.add(Conv2D(32, (5, 5), padding='same', activation='relu', input_shape=input_shape))
    model.add(Conv2D(32, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
 
    model.add(Conv2D(64, (5, 5), padding='same', activation='relu'))
    model.add(Conv2D(64, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    # model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    # model.add(Conv2D(32, (3, 3), activation='relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.25))
 
    model.add(Conv2D(64, (5, 5), padding='same', activation='relu'))
    model.add(Conv2D(64, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
 
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(n_classes, activation='softmax'))
     
    return model

def create_model_2(input_shape, n_classes):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=input_shape))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
 
    model.add(Conv2D(32, (5, 5), padding='same', activation='relu'))
    model.add(Conv2D(32, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    # model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    # model.add(Conv2D(32, (3, 3), activation='relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.25))
 
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))
 
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(n_classes, activation='softmax'))
     
    return model

def create_model_3(input_shape, n_classes):
    model = Sequential()
    model.add(Conv2D(64, (5, 5), padding='same', activation='relu', input_shape=input_shape))
    model.add(Conv2D(64, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
 
    model.add(Conv2D(64, (5, 5), padding='same', activation='relu'))
    model.add(Conv2D(64, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    # model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    # model.add(Conv2D(32, (3, 3), activation='relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.25))
 
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(n_classes, activation='softmax'))
    return model


def save_model(model, dtype='accent', name=None):
    name = name if name is not None else 'cnn_' + dtype + '_' + str(time.time()) + '.h5'
    of = os.path.join(os.path.dirname(__file__), name)
    model.save(of)


def plot_and_show_history(history):
    # Loss Curves
    plt.figure(figsize=[8,6])
    plt.plot(history.history['loss'],'r',linewidth=3.0)
    plt.plot(history.history['val_loss'],'b',linewidth=3.0)
    plt.legend(['Training loss', 'Validation Loss'],fontsize=18)
    plt.xlabel('Epochs ',fontsize=16)
    plt.ylabel('Loss',fontsize=16)
    plt.title('Loss Curves',fontsize=16)
     
    # Accuracy Curves
    plt.figure(figsize=[8,6])
    plt.plot(history.history['acc'],'r',linewidth=3.0)
    plt.plot(history.history['val_acc'],'b',linewidth=3.0)
    plt.legend(['Training Accuracy', 'Validation Accuracy'],fontsize=18)
    plt.xlabel('Epochs ',fontsize=16)
    plt.ylabel('Accuracy',fontsize=16)
    plt.title('Accuracy Curves',fontsize=16)
    plt.show()

def train_and_predict(m, checkpoint_filepath, train_input, train_labels, test_input, test_labels, dtype='accent'):
    train_input, train_labels, valid_input, valid_labels = common.get_validation_data(train_input, train_labels)
    train_input  = reshape_input(train_input)
    test_input  = reshape_input(test_input)
    valid_input  = reshape_input(valid_input)
    n_classes = common.get_n_classes(dtype)
    train_labels = keras.utils.to_categorical(train_labels, n_classes)
    test_labels = keras.utils.to_categorical(test_labels, n_classes)
    valid_labels = keras.utils.to_categorical(valid_labels, n_classes)
    batch_size = BATCH_SIZE
    epochs = 15
    if m is None:
        m = create_model(get_input_shape(), n_classes)    
        m.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy']) 
    checkpoint = ModelCheckpoint(checkpoint_filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint]       
    history = m.fit(train_input, train_labels, batch_size=batch_size, epochs=epochs, verbose=1, 
                    callbacks=callbacks_list,
                    validation_data=(valid_input, valid_labels))    
    # write model to file
    # save_model(m, dtype, checkpoint_filepath)
    # m.save(checkpoint_filepath)
    score, acc = m.evaluate(test_input, test_labels)
    print ('test score: ', score)
    print ('test accu : ', acc)
    # plot_and_show_history(history)

def load_model_and_predict(model_path, test_input):
    model = keras.models.load_model(model_path)
    test_input = reshape_input(test_input)
    model.predict_classes(test_input, batch_size=BATCH_SIZE, verbose=1)


if __name__ == '__main__':
    train_input, train_labels, test_input, test_labels = common.get_combined_data()
    start_over = False
    
    if start_over:
        checkpoint_filepath = os.path.join(os.path.dirname(__file__), 'cnn_3x3_3layers_001lr_256.h5')
        print ('=============== begining to write to ', checkpoint_filepath)
        model = create_model(get_input_shape(), common.get_n_classes('combined'))
        model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])  
        existing = keras.models.load_model(os.path.join(os.path.dirname(__file__), 'model_3x3_3layers_001lr_256.h5'))
        temp_weights = [layer.get_weights() for layer in existing.layers]
        for i in range(len(temp_weights)):
            model.layers[i].set_weights(temp_weights[i])
        train_and_predict(model, checkpoint_filepath, train_input, train_labels, test_input, test_labels, 'combined')

        # checkpoint_filepath = os.path.join(os.path.dirname(__file__), 'model_5x5_3layers_001lr_512.h5')
        # print ('=============== begining to write to ', checkpoint_filepath)
        # model = create_model_4(get_input_shape(), common.get_n_classes('combined'))
        # model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])        
        # train_and_predict(model, checkpoint_filepath, train_input, train_labels, test_input, test_labels, 'combined')

        # checkpoint_filepath = os.path.join(os.path.dirname(__file__), 'model_3x3_4layers_001lr_256.h5')
        # print ('=============== begining to write to ', checkpoint_filepath)
        # model = create_model_2(get_input_shape(), common.get_n_classes('combined'))
        # model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
        # train_and_predict(model, checkpoint_filepath, train_input, train_labels, test_input, test_labels, 'combined')

        # checkpoint_filepath = os.path.join(os.path.dirname(__file__), 'model_5x5_2layers_001lr_512.h5')
        # print ('=============== begining to write to ', checkpoint_filepath)
        # model = create_model_3(get_input_shape(), common.get_n_classes('combined'))
        # model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
        # train_and_predict(model, checkpoint_filepath, train_input, train_labels, test_input, test_labels, 'combined')
    else:
        # m = keras.models.load_model(os.path.join(os.path.dirname(__file__), 'cnn_combined_acc063_7epocs.h5'))
        m = keras.models.load_model(os.path.join(os.path.dirname(__file__), 'cnn_3x3_3layers_001lr_256_run2.h5'))
        print (m.summary())
        # print (m.get_layer('dropout_5'))
        m.optimizer = RMSprop(lr=0.00004)
        # dense_1 = m.get_layer('dense_3')
        # dense_1.kernel_regularizer=regularizers.l1(0.01)
        # dense_2 = m.get_layer('dense_4')
        # dense_2.activity_regularizer=regularizers.l2(0.01) 
        # m.lr.set_value(0.0005)
        checkpoint_filepath = os.path.join(os.path.dirname(__file__), 'cnn_3x3_3layers_001lr_256_run3.h5')
        train_and_predict(m, checkpoint_filepath, train_input, train_labels, test_input, test_labels, 'combined')
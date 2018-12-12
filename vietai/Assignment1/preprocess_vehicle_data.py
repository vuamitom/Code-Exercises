import numpy as np
import scipy.misc
import glob
import pdb
import matplotlib.pyplot as plt
from util import save_list


def process_vehicle_image():
    imw = 64
    imh = 64
    data_path = '/home/kien/PycharmProjects/data/vietai-assignment-data/vehicles/'
    car_paths = sorted(glob.glob(data_path + 'car*.jpg'))
    motorbike_paths = sorted(glob.glob(data_path + 'motorbike*.jpg'))
    train_x_car = np.zeros((imh, imw, 1500))
    train_y_car = np.zeros((1500, 1))

    for i, car_path in enumerate(car_paths):
        img = scipy.misc.imread(car_path)
        img = scipy.misc.imresize(img, (imh, imw), interp='bicubic')
        img = np.mean(img, axis=2)
        train_x_car[:,:,i] = img

    test_x_car = train_x_car[:,:,1200:]
    test_y_car = train_y_car[1200:]
    train_x_car = train_x_car[:,:,:1200]
    train_y_car = train_y_car[:1200]

    train_x_mo = np.zeros((imh, imw, 1500))
    train_y_mo = np.ones((1500, 1))

    for i, motorbike_path in enumerate(motorbike_paths):
        img = scipy.misc.imread(motorbike_path)
        img = scipy.misc.imresize(img, (imh, imw), interp='bicubic')
        img = np.mean(img, axis=2)
        train_x_mo[:,:,i] = img

    test_x_mo = train_x_mo[:,:,1200:]
    test_y_mo = train_y_mo[1200:]
    train_x_mo = train_x_mo[:,:,:1200]
    train_y_mo = train_y_mo[:1200]

    train_x = np.concatenate((train_x_car, train_x_mo), axis=2)
    train_y = np.concatenate((train_y_car, train_y_mo), axis=0)
    test_x = np.concatenate((test_x_car, test_x_mo), axis=2)
    test_y = np.concatenate((test_y_car, test_y_mo), axis=0)
    
    #plt.ion()
    #for i in range(0,600,24):
    #    plt.clf()
    #    plt.imshow(test_x[:,:,i], cmap='gray')
    #    plt.show()
    #    plt.pause(0.2)
    #    print("%d %d" % (i, test_y[i, 0]))

    #pdb.set_trace()
    save_list([train_x, train_y, test_x, test_y], './data/vehicles.dat')


if __name__ == '__main__':
    process_vehicle_image()

from __future__ import absolute_import
from keras.datasets.cifar import load_batch
from keras.datasets.data_utils import get_file
import numpy as np
import os
import json
from random import shuffle
import cPickle as pickle
import collections
import csv
from PIL import Image

IMG_SIZE=128
sketch_path='single_characters_10000'#'sketch'
real_path='real'

def load_test_images(img_paths, ids):
    imgs=[]
    # Load img arrays
    for idx, img_path in enumerate(img_paths):
        if ids[idx] == 0:
            original = Image.open(img_path)
            resized = original.resize((IMG_SIZE, IMG_SIZE))
            final_img_arr = np.asarray(resized).flatten().tolist()
            imgs.append(final_img_arr)
        elif ids[idx] == 1:
            original = Image.open('sketch/'+img_path)
            resized = original.resize((IMG_SIZE, IMG_SIZE))
            # Convert grayscale to RGB, since it's read as a grayscale image
            rgbimg = Image.new("RGB", resized.size)
            rgbimg.paste(resized)
            ### transform image to a list of numbers for easy storage.
            final_img_arr = np.asarray(rgbimg).flatten().tolist()
            imgs.append(final_img_arr)

    return  change_img_array_shape(imgs)


#FILE='nn_train_data.json'
FILE='nn_train_data_paths.json'

# reshape img array to (rgb, location(1D))
def change_img_array_shape(imgs):
    result=[]#result=np.array([])

    i=0
    for img in imgs:
        # img = 64,64,3
        index=0
        new_img = [[],[],[]]
        #new_img = np.array([np.array([]),np.array([]),np.array([])])
        for col in img:
            if index % 3 == 0:#R
                #print col

                new_img[0].append(col)
                #print index
                #print new_img[0]
                #np.append(new_img[0], col)

            elif index % 3 == 1:#G
                new_img[1].append(col)
                #np.append(new_img[1], col)
            elif index % 3 == 2:#B
                new_img[2].append(col)
                #np.append(new_img[2], col)
            index += 1

        new_img = np.array(new_img)
        result.append(new_img.reshape(3,IMG_SIZE,IMG_SIZE))
        #print new_img.shape# => (3, 4096)
        #print new_img.reshape(3,64,64)
        #np.append(result, new_img.reshape(3,64,64))
        i+=1
        if i % 100==0: print i
    return np.array(result)


def load_file():
    illust=[]
    real=[]
    with open(FILE) as data_file:
        org = json.load(data_file)

    train = np.array(org['imgs'])
    print train[0].shape
    print train[0][0]
    print train[0][1]
    # read image paths, not img itself since it's too large
    #train = change_img_array_shape(train)
    print train.shape

    labels = org['ids']
    return train, labels


def load_data():
    imgs, labels = load_file()
    print len(imgs)

    # Ceate a dict for labels
    #classes = get_all_labels()
    #classMap = dict(zip(classes.iterkeys(),xrange(len(classes))))
    #index = 0
    #labels = [ classMap[label] for label in labels ]
    #with open('label_map.bin','w') as fid:
    #    pickle.dump(labels, fid)

    data = zip(imgs, labels) # => ([(...img array..., label), (...), ...])
    shuffle(data)

    # unzip it
    imgs, labels = zip(*data)

    nb_test_samples = 1000#10000
    nb_train_samples = len(data)-nb_test_samples

    #X_train = np.zeros((nb_train_samples, 50, 50, 3), dtype="uint8")
    X_test = imgs[:nb_test_samples]
    y_test = labels[:nb_test_samples]
    X_train = imgs[nb_test_samples+1:]
    y_train = labels[nb_test_samples+1:]#np.zeros((nb_train_samples,), dtype="uint8")


    # Convert to ndarray
    X_train = np.array(list(X_train))
    y_train = np.array(list(y_train))
    X_test = np.array(list(X_test))
    y_test = np.array(list(y_test))
    print 'dataset debug'
    print len(X_train)
    print len(X_test)
    print type(X_train)
    print type(y_train)
    print type(X_test)
    #print X_train[0]
    #print y_train[0]

    """for i in range(1, 6):
        fpath = os.path.join(path, 'data_batch_' + str(i))
        data, labels = load_batch(fpath)
        X_train[(i-1)*10000:i*10000, :, :, :] = data
        y_train[(i-1)*10000:i*10000] = labels

    fpath = os.path.join(path, 'test_batch')
    X_test, y_test = load_batch(fpath)

    y_train = np.reshape(y_train, (len(y_train), 1))
    y_test = np.reshape(y_test, (len(y_test), 1))"""

    #print 'debug dataset'
    #print type(X_train)
    #print X_train.dtype
    #print type(y_train)


    return (X_train, y_train), (X_test, y_test)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from utils.constants import UNIVARIATE_ARCHIVE_NAMES  as ARCHIVE_NAMES
from utils.constants import CLASSIFIERS
from utils.constants import UNIVARIATE_DATASET_NAMES as DATASET_NAMES
from utils.constants import ITERATIONS
from MLDataCollector import MlDataCollector

from utils.utils import read_all_datasets
from utils.utils import transform_labels
from utils.utils import create_directory

import pandas as pd
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import numpy as np
import sklearn 
from MLMain import MlMain
from keras.utils import to_categorical

def prepare_data():
    #dataSet = np.load('saveFile_D40_V2/dataset_.npy',allow_pickle=True)
    #X = np.load('saveFile_D40_V2/valuesSave.npy')
    #y = np.load('saveFile_D40_V2/targetSave.npy')
    #print("x:",X,"y:", y)
    #y = to_categorical(y)
    #y= np.argmax(y, axis=1)
    Main = MlMain()
    print("main type",type(Main))
    Main.getDataset()
    #X, y = Main.valuesCollection, Main.targetCollection
    #y = np.reshape(y, (1,np.product(y.shape)))[0]
    #df= pd.DataFrame(dataCollector,)
    sys.exit(0)
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    print("xtrain",x_train,"xtest", x_test,"ytrain", y_train,"ytest", y_test)
            
   # from sklearn.model_selection import LeaveOneOut 
   # X = np.array([[1, 2], [3, 4]])
   # y = np.array([1, 2])
   # loo = LeaveOneOut()
   # loo.get_n_splits(X)
         
   # for train_index, test_index in loo.split(X):
   #     print("TRAIN:", train_index, "TEST:", test_index)
   #     x_train, x_test = X[train_index], X[test_index]
   #     y_train, y_test = y[train_index], y[test_index]
   #     print("xtrain",x_train,"xtest", x_test,"ytrain", y_train,"ytest", y_test) 
    
    #x_train = datasets_dict[dataset_name][0]
    #y_train = datasets_dict[dataset_name][1]
    #x_test = datasets_dict[dataset_name][2]
    #y_test = datasets_dict[dataset_name][3]

    nb_classes = len(np.unique(np.concatenate((y_train, y_test), axis=0)))
    y_train= np.argmax(y_train, axis=1)
    y_test= np.argmax(y_test, axis=1)
    # make the min to zero of labels
    y_train, y_test = transform_labels(y_train, y_test)

    # save orignal y because later we will use binary
    y_true = y_test.astype(np.int64)
    y_true_train = y_train.astype(np.int64)
    print("y_true", y_true)
    print("ytrueTrain", y_true_train)
    # transform the labels from integers to one hot vectors
    enc = sklearn.preprocessing.OneHotEncoder()
    enc.fit(np.concatenate((y_train, y_test), axis=0).reshape(-1, 1))
    y_train = enc.transform(y_train.reshape(-1, 1)).toarray()
    y_test = enc.transform(y_test.reshape(-1, 1)).toarray()

    if len(x_train.shape) == 2:  # if univariate
        # add a dimension to make it multivariate with one dimension
        x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], 1))
        x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], 1))

    return x_train, y_train, x_test, y_test,y_true, nb_classes,y_true_train, enc

def fit_classifier(load_weights=False):

    input_shape = x_train.shape[1:]

    classifier = create_classifier(classifier_name,input_shape, nb_classes, output_directory
                                   ,load_weights=load_weights)

    classifier.fit(x_train,y_train,x_test,y_test, y_true)

def create_classifier(classifier_name, input_shape, nb_classes, output_directory, verbose = False,
                      build=True,load_weights=False):
    if classifier_name=='fcn': 
        from classifiers import fcn        
        return fcn.Classifier_FCN(output_directory,input_shape, nb_classes, verbose,build=build)
    if classifier_name=='mlp':
        from  classifiers import  mlp 
        return mlp.Classifier_MLP(output_directory,input_shape, nb_classes, verbose,build=build)
    if classifier_name=='resnet':
        from  classifiers import resnet 
        return resnet.Classifier_RESNET(output_directory,input_shape, nb_classes, verbose,
                                        build=build,load_weights=load_weights)
    if classifier_name=='encoder':
        from classifiers import encoder
        return encoder.Classifier_ENCODER(output_directory,input_shape, nb_classes, verbose,build=build)
    if classifier_name=='mcdcnn':
        from classifiers import mcdcnn
        return mcdcnn.Classifier_MCDCNN(output_directory,input_shape, nb_classes, verbose,build=build)
    if classifier_name=='cnn':
        from classifiers import cnn
        return cnn.Classifier_CNN(output_directory,input_shape, nb_classes, verbose,build=build)
    if classifier_name=='ensembletransfer':
        from classifiers import ensembletransfer
        return ensembletransfer.Classifier_ENSEMBLETRANSFER(output_directory,input_shape,
                                                            nb_classes, verbose)
    if classifier_name=='nne':
        from classifiers import nne
        return nne.Classifier_NNE(output_directory,input_shape,
                                                            nb_classes, verbose)

root_dir = 'C:/Users/Legion/src/PyMLServer-Local1'
    
for classifier_name in CLASSIFIERS:
    print('classifier_name',classifier_name)

    for archive_name in ARCHIVE_NAMES:
        print('\tarchive_name',archive_name)

        #datasets_dict = read_all_datasets(root_dir, archive_name)

        for iter in range(ITERATIONS):
            print('\t\titer',iter)

            trr = ''
            if iter!=0:
                trr = '_itr_'+str(iter)

            tmp_output_directory = root_dir+'/results/'+classifier_name+'/'+archive_name+trr+'/'

            for dataset_name in DATASET_NAMES:
                print('\t\t\tdataset_name: ', dataset_name)

                x_train, y_train, x_test, y_test, y_true, nb_classes,y_true_train,enc = prepare_data()

                output_directory = tmp_output_directory+dataset_name+'/'

                if classifier_name!='nne' and classifier_name!='ensembletransfer':

                    temp_output_directory = create_directory(output_directory)

                    if temp_output_directory  is None:
                        print('Already_done',tmp_output_directory,dataset_name)
                        continue

                fit_classifier()

                print('\t\t\t\tDONE')

                if classifier_name!='nne' and classifier_name!='ensembletransfer':

                    # the creation of this directory means
                    create_directory(output_directory + '/DONE')

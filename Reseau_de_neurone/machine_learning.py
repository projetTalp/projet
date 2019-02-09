# -*- coding: utf-8 -*-
'''
Function to train and evaluate neural networks using Keras

Organization:
    IRISA/Expression
'''

import sys
from keras.utils import np_utils
from keras.models import Sequential, save_model, load_model
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, RMSprop
from keras.layers.advanced_activations import LeakyReLU, PReLU ## , ParametricSoftplus
from keras.callbacks import Callback, EarlyStopping
import pandas as pd
import numpy as np
from keras import backend as K
import math
from keras.callbacks import TensorBoard
from keras import regularizers
from keras.models import model_from_json
import json
import utils
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib import cm
#from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense


seed=0
np.random.seed(seed)
'''
Set random seed for reproducibility
'''


model_param={
            'loss':'mean_squared_error',
            'optimizer':'sgd',
            'nb_epoch':500,
            'batch_size':10,
            'verbose':1
}
'''
Keras model default paramaters
'''


def train_neural_network(output_file,
                         train_input,
                         train_output,
                         dev_input=None,
                         dev_output=None):
    '''
    Create a deep neural network
    
    Arg:
        output_file: file where the model will be saved
        train_input: training data input
        train_output: ground truth for the training data
        dev_input: dev data input if desired
        dev_output: dev data ground truth if desired (needed if dev_input is provided)
    
    Return:
        A neural network model
    '''
    assert len(train_input) != 0, "dataset must not be empty"

    np_input = np.asarray(train_input)
    np_output = np.asarray(train_output)
    np.random.seed(0)

    # Logging utils
    class TrainingHistory(Callback):
        def on_train_begin(self, logs={}):
            self.losses = []
            self.predictions = []
            self.i = 0
            self.save_every = 50

        def on_epoch_end(self, batch, logs={}):
            self.losses.append(logs.get('loss'))
            self.i += 1        
            if self.i % self.save_every == 0:        
                pred = self.model.predict(np_input)
                self.predictions.append(pred)
                
    class WeightHistory(Callback):
        def on_train_begin(self, logs={}):
            self.losses = []
            self.predictions = []
            self.i = 0
            self.save_every = 50

        def on_epoch_end(self, batch, logs={}):
            print self.model.get_weights()
    
    history = TrainingHistory()
    weights = WeightHistory()
    early_stopping = EarlyStopping(monitor="val_loss", patience=30, verbose=0)

    # Create neural network
    ## model = Sequential()
    ## model.add(Dense(output_dim=64, activation='linear', input_dim=2))
   	## model.add(Dense(output_dim=1, activation='sigmoid'))
    
    ##question2 
    ##model = Sequential()
    ##model.add(Dense(output_dim=64, activation='linear', input_dim=2))
    ##model.add(Dense(output_dim=64, activation='linear', input_dim=64))
    ##model.add(Dense(output_dim=64, activation='linear', input_dim=64))
    ##model.add(Dense(output_dim=1, activation='sigmoid'))"""
    
    ## Question4
    ## model = Sequential()
    ## model.add(Dense(output_dim=64, activation='linear', input_dim=2))
    ## model.add(Dense(output_dim=1, activation='linear', input_dim=64))
    
    #Question 5
    ## model = Sequential()
    ## model.add(Dense(output_dim=64, activation='elu', input_dim=2))
    ## model.add(Dense(output_dim=1, activation='linear', input_dim=64))
    #Question 6
    
    print("ok ?")
    
    model = Sequential()
    model.add(Dense(output_dim=1000, activation='elu', input_dim=13214))
    model.add(Dense(output_dim=100, activation='elu', input_dim=1000))
    model.add(Dense(output_dim=1, activation='sigmoid', input_dim=100))
    
    # Compile model
    model.compile(loss=model_param['loss'],
                  optimizer=model_param['optimizer'])
    

    print "Training..."
    #print np_input
    #print "--"
    #print np_output

    if dev_input and dev_output:
        np_v_input = np.asarray(dev_input)
        np_v_output = np.asarray(dev_output)
        hist = model.fit(np_input,
                         np_output,
                         validation_data=(np_v_input, np_v_output),
                         nb_epoch=model_param['nb_epoch'],
                         batch_size=model_param['batch_size'],
                         verbose=model_param['verbose'],
                         callbacks=[history, weights, early_stopping])
    else:
        hist = model.fit(np_input,
                         np_output,
                         nb_epoch=model_param['nb_epoch'],
                         batch_size=model_param['batch_size'],
                         verbose=model_param['verbose'],
                         callbacks=[history, weights, early_stopping])
    
    print "Saving..."
    save_model(model, output_file)
    
    model.summary()
    
    return model




def evaluate(model,
            q_input,
            q_output):
    '''
    Evaluate the model accuracity
    
    Args:
        model: Model to evaluate
        q_input: data input
        q_output: ground truth for the the data input
    '''
    np_input = np.asarray(q_input)
    np_output = np.asarray(q_output)
    try:
        print "Evaluating..."
        assert len(q_input) != 0, "Query list must not be empty"
        scores = model.evaluate(np_input,
                                np_output,
                                batch_size=model_param['batch_size'],
                                verbose=model_param['verbose'])
        print "\nModel acurracy:", scores
        
        np_predictions = model.predict(np_input)
        
        for j in range(len(np_output.T)):
            for i in range(len(np_input.T)):
                plt.figure()
                plt.plot(np_input.T[i].T, np_output.T[j], 'bo', label='Ground truth')
                plt.plot(np_input.T[i].T, np_predictions.T[j], 'ro', label='Prediction')
                plt.legend(loc='upper left')
                t = "Input %i -> Output %i" % (i, j)
                plt.title(t)
        plt.show()

        
    except ValueError, e:
        print 'Wrong keras model or model parameters'



import pandas as pd
import numpy as np
#matplotlib inline
#import matplotlib.pyplot as plt
from os import listdir

from keras.preprocessing import sequence
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

from keras.optimizers import Adam
from keras.models import load_model
from keras.callbacks import ModelCheckpoint

pip install sagemaker

import sagemaker
import boto3
import pandas as pd
from sagemaker import get_execution_role

pip install s3fs

import s3sf

    
sequences = list()
for i in range(0,29):
    data_key = "data_"+str(i)+".csv"
    data_location = 's3://{}/{}'.format(bucket, data_key)
    df = pd.read_csv(data_location, header=0)
    values = df.values
    sequences.append(values)

arget_location = 's3://{}/{}'.format(bucket, "results.csv")
targets = pd.read_csv(target_location, header=0)
targets = targets.values[:,0]
for i in range(0,len(targets)):
    if (targets[i]=='G'):
        targets[i]=1
    else:
        targets[i]=0
print(targets)

def normalize(df):
    result = df.transpose()
    for i in (0,len(result)-1):
        max_value = result[i].max()
        min_value = result[i].min()
        result[i] = (result[i] - min_value) / (max_value - min_value)
    result2 = result.transpose()
    return result2

to_pad = 62
new_seq = []
for one_seq in sequences:
    #len_one_seq = len(one_seq)
    #last_val = one_seq[-1]
    #n = to_pad - len_one_seq
    #   
    #to_concat = np.repeat(one_seq[-1], n).reshape(8, n).transpose()
    #new_one_seq = np.concatenate([one_seq, to_concat])
    new_one_seq=normalize(one_seq)
    new_seq.append(new_one_seq)
    
final_seq = new_seq

#truncate the sequence to length 60
#from keras.preprocessing import sequence
#seq_len = 61
#final_seq=sequence.pad_sequences(final_seq, maxlen=seq_len, padding='post', dtype='float', truncating='post')

train = final_seq[0:28]
validation = final_seq[0:28]
test = final_seq[20:28]

train_target = targets[0:28]
validation_target = targets[0:28]
test_target = targets[20:28]

train = np.array(train)
validation = np.array(validation)
test = np.array(test)

train_target = np.array(train_target)
train_target = (train_target+1)/2

validation_target = np.array(validation_target)
validation_target = (validation_target+1)/2

test_target = np.array(test_target)
test_target = (test_target+1)/2

model = Sequential()
model.add(LSTM(256, input_shape=(seq_len, 8)))
model.add(Dense(1, activation='sigmoid'))

adam = Adam(lr=0.001)
chk = ModelCheckpoint('best_model.pkl', monitor='val_acc', save_best_only=True, mode='max', verbose=1)
model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])
model.fit(train, train_target, epochs=200, batch_size=4, callbacks=[chk], validation_data=(validation,validation_target))

#loading the model and checking accuracy on the test data
model = load_model('best_model.pkl')
test = [final_seq[0:28]]



from sklearn.metrics import accuracy_score
test_preds = model.predict_classes(test)
#accuracy_score(test_target, test_preds)
print(test_preds)


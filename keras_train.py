from keras_common import *

from scipy.integrate import odeint
from matplotlib import pyplot as plt
import numpy as np
from random import random

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def gen_dataset(arange,brange,pop,n,T,size):
    data,labels = gen_data(arange,brange,pop,n,T,size)
    return tf.data.Dataset.from_tensor_slices((data,labels))

def gen_data(arange,brange,pop,n,T,size):
    data = []
    labels = []
    for i in range(size):
        a = arange[0] + (arange[1]-arange[0])*random()
        b = brange[0] + (brange[1]-brange[0])*random()
        dp = np.array(odeintI(a,b,pop,n,T)[0]).reshape(1,1000)
        data.append(dp)
        labels.append((a,b))
    data = np.array(data)
    labels = np.array(labels)
    labels = np.squeeze(labels)
    return (data,labels)

arange = (2e-5,5e-5) #Intervalle de valeurs de alpha pour la génération des courbes
brange = (0.05,0.1) #Intervalle pour beta
pop = 10000 #Population
n = 1000 #nombre de points sur une courbe
T = 365 #durée représentée sur une courbe

data,labels = gen_data(arange,brange,pop,n,T,10000) #Dataset d'apprentissage
train_ds =  tf.data.Dataset.from_tensor_slices((data,labels))
val_ds = gen_dataset(arange,brange,pop,n,T,5) #Validation
test_ds = gen_dataset(arange,brange,pop,n,T,5) #Test
print("DATA READY")
a,b = random_ab(arange,brange)
x = np.array(odeintI(a,b,pop,n,T)[0]).reshape(1,1000)
"""
print("data.shape : ", data.shape)
print("\n".join(["{},{}".format(*label) for label in labels]))
t = np.linspace(0,T,n)
for dp in data[:10]:
    plt.plot(t,dp.squeeze())
plt.show()
"""
model = keras.Sequential([
    layers.Dense(100,activation="sigmoid"),
    layers.Dense(100,activation="sigmoid"),
    layers.Dense(100,activation="sigmoid"),
    layers.Dense(2,activation="sigmoid")
])
model.compile(optimizer="rmsprop", loss="mean_squared_error")
model.build(input_shape=(1,1000))
print("MODEL READY")
print(model.summary())
results1 = model.evaluate(val_ds) #Première évaluation de la performance du modèle (avant l'apprentissage)
y1 = model.predict(x)
model.fit(train_ds,batch_size=16,epochs=5,validation_data=val_ds)
results2 = model.evaluate(val_ds) #Deuxième évalution (après l'apprentissage)
y2 = model.predict(x)
print("Evaluation before training : {}".format(results1))
print("Evaluation after training : {}".format(results2))
model.save("model") #Sauvegarde du modèle dans un fichier

print("a = {}, b = {}, prediction1 = {}, prediction2 = {}".format(a,b,y1,y2))

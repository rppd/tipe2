from scipy.integrate import odeint
from matplotlib import pyplot as plt
import numpy as np
from random import random

import tensorflow as tf
from tensorflow import keras

def odeintI(a,b,pop,n,T):
    """Génération d'une courbe d'infectés solution du système différentiel SIR avec odeint"""
    t = np.linspace(0,T,n)
    solution = odeint(fct,[0,pop-1,1],t,args=(a,b))
    return solution[:,2],t

def fct(y, t, a, b): #pour odeint
    R,S,I = y
    return [b*I,-a*S*I,a*S*I-b*I]

def random_ab(arange,brange):
    """Choix aléatoire de coefficients a et b dans des intervalles arange=(amin,amax) brange=(bmin,bmax)"""
    a = arange[0] + (arange[1]-arange[0])*random()
    b = brange[0] + (brange[1]-brange[0])*random()
    return (a,b)

def gen_dataset(arange,brange,pop,n,T,size):
    """Génération d'un dataset tensorflow à partir de gen_data"""
    data,labels = gen_data(arange,brange,pop,n,T,size)
    return tf.data.Dataset.from_tensor_slices((data,labels))

def gen_data(arange,brange,pop,n,T,size):
    """Génération d'une de size courbes d'infectés, chacune à n valeurs sur une durée T, avec des coefficients dans arange et brange"""
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

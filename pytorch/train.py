import torch
from second import gen_data, preprocessing
from net import Net

from matplotlib import pyplot as plt

net = Net()
print("Net ready, creating training set")

epochs = 5000
train_size = 5000
val_size = 50

#VALEURS
arange = (1e-5,1e-4) #Intervalle de valeurs de alpha pour la génération des courbes
brange = (0.02,0.1) #Intervalle pour beta
pop = 10000 #Population
n = 1000 #nombre de points sur une courbe
T = 365 #durée représentée sur une courbe


#TRAINING SET
train_data,train_labels = gen_data(arange,brange,pop,n,T,train_size) #data,labels = infected curve(array), (a,b)
p_train_data, p_train_labels = preprocessing(train_data,train_labels) #p_data, p_labels = preprocesed data/labels : (max,max position,max delta,average) and normalized a and b
train_inputs, train_targets = torch.tensor(p_train_data).float(), torch.tensor(p_train_labels).float() #inputs, labels = pytroch tensors for p_data and p_labels
print("Train set ready")

#VALIDATION SET
val_data,val_labels = gen_data(arange,brange,pop,n,T,val_size)
p_val_data, p_val_labels = preprocessing(val_data,val_labels)
val_inputs, val_targets = torch.tensor(p_val_data).float(), torch.tensor(p_val_labels).float()
print("Validation set ready.")

criterion = torch.nn.MSELoss() #Loss function

lr = 0.2
opt = torch.optim.SGD(net.parameters(), lr=lr)
print("Starting training")
for i in range(epochs):
    opt.zero_grad()
    outputs=net(train_inputs)
    loss = criterion(outputs,train_targets)
    loss.backward()
    opt.step()
    if (i+1)%10 == 0:
        loss = criterion(net(val_inputs),val_targets).item()
        print("{}/{} : {}".format(i+1,epochs,loss))
print("Training finished.")
torch.save(net.state_dict(), "model")
print("Model saved.")
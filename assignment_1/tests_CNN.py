from assignment_1.train_mlp_pytorch import *
import torch
import torch.nn as nn
import torch.optim as optim
from assignment_1 import cifar10_utils
import time

torch.manual_seed(42)
np.random.seed(42)

class Net(nn.Module):

    def __init__(self, n_inputs, n_classes):
        super(Net, self).__init__()

        layers = []
        layers.extend(self.conv_batch_relu(n_inputs, 64, 3, 1, 1))
        layers.append(nn.MaxPool2d(kernel_size=3, stride=2, padding=1))

        layers.extend(self.conv_batch_relu(64, 128, 3, 1, 1))
        layers.append(nn.MaxPool2d(kernel_size=3, stride=2, padding=1))

        layers.extend(self.conv_batch_relu(128, 256, 3, 1, 1))
        layers.extend(self.conv_batch_relu(256, 256, 3, 1, 1))
        layers.append(nn.MaxPool2d(kernel_size=3, stride=2, padding=1))

        layers.extend(self.conv_batch_relu(256, 512, 3, 1, 1))
        layers.extend(self.conv_batch_relu(512, 512, 3, 1, 1))
        layers.append(nn.MaxPool2d(kernel_size=3, stride=2, padding=1))

        layers.extend(self.conv_batch_relu(512, 512, 3, 1, 1))
        layers.extend(self.conv_batch_relu(512, 512, 3, 1, 1))
        layers.append(nn.MaxPool2d(kernel_size=3, stride=2, padding=1))
        layers.append(nn.AvgPool2d(kernel_size=1, stride=1, padding=0))

        self.lin = nn.Linear(512, n_classes)

        self.layers = nn.Sequential(*layers)

    # specify input, output, kernel_size, stride and padding for each conv, batch, relu combi
    def conv_batch_relu(self, input, output, kernel_size, stride, padding):
        conv = nn.Conv2d(input, output, kernel_size, stride, padding)
        norm = nn.BatchNorm2d(output)
        relu = nn.ReLU()
        return [conv, norm, relu]

    def forward(self, x):
        x = self.layers(x)
        x = x.view(x.shape[0], -1)
        x = self.lin(x)
        return x


# Initialization
batch_size = 32
cifar10 = cifar10_utils.get_cifar10('./cifar10/cifar-10-batches-py')
x, y = cifar10['train'].next_batch(batch_size)
print(x.shape)
# n_inputs = x.shape[1]
n_inputs = 3
n_classes = y.shape[1]
l_rate = 1e-4
network = Net(n_inputs, n_classes)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(network.parameters(), l_rate)

# Training
start = time.time()
for i in range(100):
    x_train, y_train = cifar10['train'].next_batch(batch_size)
    # x = x_train.reshape(batch_size, -1)
    x = torch.from_numpy(x_train)
    y = np.argmax(y_train, axis=1)
    y = torch.from_numpy(y)

    optimizer.zero_grad()
    pred = network(x)
    loss = criterion(pred, y)
    loss.backward()
    optimizer.step()
    if i % 10 == 9:
        print(loss.item())

end = time.time()
print(end - start)
# Get test set
x_test, y_test = cifar10['test'].images, cifar10['test'].labels
x_test = torch.from_numpy(x_test)
x_test = x_test[0:10,:,:,:]
y_test = y_test[0:10, :]
print(y_test.shape)
pred = network(x_test)
pred = pred.data.numpy()
acc = accuracy(pred, y_test)
print(acc)

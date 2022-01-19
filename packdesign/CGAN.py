from typing import Dict

import torch.nn as nn
import torch.nn.functional as F
import torch

class Generator(nn.Module):
    # initializers
    def __init__(self, C, latent_dim, n_class, d=128):
        super(Generator, self).__init__()
        self.deconv1_1 = nn.ConvTranspose2d(latent_dim, d*2, 4, 1, 0)
        self.deconv1_1_bn = nn.BatchNorm2d(d*2)
        # self.deconv1_2 = nn.ConvTranspose2d(n_class, d*2, 4, 1, 0)  # label nums
        # self.deconv1_2_bn = nn.BatchNorm2d(d*2)
        self.deconv2 = nn.ConvTranspose2d(d*2, d*2, 4, 2, 1) 
        self.deconv2_bn = nn.BatchNorm2d(d*2)
        self.deconv3 = nn.ConvTranspose2d(d*2, d*2, 4, 2, 1)
        self.deconv3_bn = nn.BatchNorm2d(d*2)
        self.deconv4 = nn.ConvTranspose2d(d*2, d*4, 4, 2, 1)
        self.deconv4_bn = nn.BatchNorm2d(d*4)
        self.deconv5 = nn.ConvTranspose2d(d*4, d*8, 4, 2, 1)
        self.deconv5_bn = nn.BatchNorm2d(d*8)
        self.deconv6 = nn.ConvTranspose2d(d*8, d*4, 4, 2, 1)
        self.deconv6_bn = nn.BatchNorm2d(d*4)
        self.deconv7 = nn.ConvTranspose2d(d*4, d, 4, 2, 1)
        self.deconv7_bn = nn.BatchNorm2d(d)
        self.deconv8 = nn.ConvTranspose2d(d, C, 4, 2, 1)


    # forward method
    def forward(self, input, label):
        x = F.relu(self.deconv1_1_bn(self.deconv1_1(input)))
        # y = F.relu(self.deconv1_2_bn(self.deconv1_2(label)))
        # x = torch.cat([x, y], 1)
        x = F.relu(self.deconv2_bn(self.deconv2(x)))
        x = F.relu(self.deconv3_bn(self.deconv3(x)))
        x = F.relu(self.deconv4_bn(self.deconv4(x)))
        x = F.relu(self.deconv5_bn(self.deconv5(x)))
        x = F.relu(self.deconv6_bn(self.deconv6(x)))
        x = F.relu(self.deconv7_bn(self.deconv7(x)))
        x = F.tanh(self.deconv8(x))
        return x

class Discriminator(nn.Module):
    # initializers
    def __init__(self, C, n_class, d=128):
        super(Discriminator, self).__init__()
        self.conv1_1 = nn.Conv2d(C, d, 4, 2, 1)
        self.conv1_bn = nn.BatchNorm2d(d)
        # self.conv1_2 = nn.Conv2d(n_class, d//2, 4, 2, 1) # label nums
        self.conv2 = nn.Conv2d(d, d*2, 4, 2, 1)
        self.conv2_bn = nn.BatchNorm2d(d*2)
        self.conv3 = nn.Conv2d(d*2, d*2, 4, 2, 1)
        self.conv3_bn = nn.BatchNorm2d(d*2)
        self.conv4 = nn.Conv2d(d*2, d*4, 4, 2, 1)
        self.conv4_bn = nn.BatchNorm2d(d*4)
        self.conv5 = nn.Conv2d(d*4, d*8, 4, 2, 1)
        self.conv5_bn = nn.BatchNorm2d(d*8)
        self.conv6 = nn.Conv2d(d*8, d*4, 4, 2, 1)
        self.conv6_bn = nn.BatchNorm2d(d*4)
        self.conv7 = nn.Conv2d(d*4, 1, 4, 1, 0)
        self.fc1 = nn.Linear(5*5, 1)


    # def forward(self, input):
    def forward(self, input, label):
        x = F.leaky_relu(self.conv1_bn(self.conv1_1(input)), 0.2)
        # y = F.leaky_relu(self.conv1_2(label), 0.2)
        # x = torch.cat([x, y], 1)
        x = F.leaky_relu(self.conv2_bn(self.conv2(x)), 0.2)
        x = F.leaky_relu(self.conv3_bn(self.conv3(x)), 0.2)
        x = F.leaky_relu(self.conv4_bn(self.conv4(x)), 0.2)
        x = F.leaky_relu(self.conv5_bn(self.conv5(x)), 0.2)
        x = F.leaky_relu(self.conv6_bn(self.conv6(x)), 0.2)
        x = F.sigmoid(self.fc1(torch.flatten(self.conv7(x), start_dim=1)))
        return x
import warnings
warnings.filterwarnings('ignore')

from glob import glob
import pandas as pd
import numpy as np 
from tqdm import tqdm

import os
import random
import matplotlib as plt
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torchvision.transforms as transforms
from sklearn.metrics import f1_score, accuracy_score
import time
from typing import Tuple, Sequence, Callable
from PIL import Image
import cv2
from torchvision import models


def img_load(path):
    img = cv2.resize(path, (16, 16))
    return img


class Custom_dataset(Dataset):
    def __init__(self, 
                 img_paths, 
                 labels, 
                 mode='train',
                 transforms= Sequence[Callable]
            ) -> None:
        self.img_paths = img_paths
        self.labels = labels
        self.mode=mode
        self.transforms = transforms

    def __len__(self):
        return len(self.img_paths)
    def __getitem__(self, idx):
        img = self.img_paths[idx]
        if self.mode=='train':
            augmentation = random.randint(0,2)
            if augmentation==1:
                img = img[::-1].copy()
            elif augmentation==2:
                img = img[:,::-1].copy()
        if self.mode=='test':
            pass
#tv.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        img = Image.fromarray(img) # NumPy array to PIL image
        img = img.convert("RGB")

        if self.transforms is not None:
            img = self.transforms(img)        
        label = self.labels[idx]
        return img, label
        
class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.model = models.mobilenet_v2(pretrained=False)
        self.linear=nn.Linear(in_features=1000,out_features=88)
        self.softmax=nn.Softmax(dim=1)
    def forward(self, x):
        x = self.model(x)
        x = self.linear(x)
        x = self.softmax(x)
        return x


class PredictModel():
    def predict(self,file_name=None):
        if file_name==None:
            return { "answer" : "error" }
        else:
            device = torch.device('cuda')
            path="/workspace/drf_disease/media/uploads/{}".format(file_name)
            test_png = cv2.imread(path)
            test_imgs = img_load(test_png)

            transforms_test = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(
                    [0.485, 0.456, 0.406],
                    [0.229, 0.224, 0.225]
                )
            ])

            train_y = pd.read_csv('/workspace/drf_disease/product/input/train_df.csv')

            train_labels = train_y["label"]

            label_unique = sorted(np.unique(train_labels))
            label_unique = {key:value for key,value in zip(label_unique, range(len(label_unique)))}

            # Test
            batch_size = 1

            test_dataset = Custom_dataset(np.array(test_imgs), np.array(["tmp"]*len(test_imgs)), mode='test',transforms=transforms_test)
            test_loader = DataLoader(test_dataset, shuffle=False, batch_size=1)

            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            model = Network().to(device)
            #model.load_state_dict(torch.load('./input/models/test_model.pth'), strict=False)

            model.eval()
            f_pred = []

            with torch.no_grad():
                for batch in (test_loader):
                    x = torch.tensor(batch[0], dtype = torch.float32, device = device)
                    pred = model(x)
                    f_pred.extend(pred.argmax(1).detach().cpu().numpy().tolist())


            label_decoder = {val:key for key, val in label_unique.items()}
            f_result = [label_decoder[result] for result in f_pred]
            
            
            
            sort_pred=sorted(pred[0].detach().cpu().numpy().tolist(),reverse=True)
            
            index_list=[0,0,0,0,0]
            sub_pred=['','','','','',]

            for i in range(0,5):
                index_list[i],sub_pred[i]=pred[0].detach().cpu().numpy().tolist().index(sort_pred[i]),sort_pred[i]*100.0
            
            sub_result = [label_decoder[result] for result in index_list]
            
            return {"answer" : f_result,"sub_pred":sub_pred,"sub_result":sub_result}
        # pred에서 가장 큰 값 5개를 뽑아 index와 크기순으로 하기
# https://urliveblogger.blogspot.com/2021/01/html-progress.html
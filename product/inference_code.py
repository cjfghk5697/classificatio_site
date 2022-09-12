import warnings
warnings.filterwarnings('ignore')

from glob import glob
import pandas as pd
import numpy as np 
from tqdm import tqdm
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image
import os
import random
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torchvision
from torchvision.models import mobilenet_v2
import torchvision.transforms as transforms
from sklearn.metrics import f1_score, accuracy_score
import time
from typing import Tuple, Sequence, Callable
from PIL import Image
import cv2
from torchvision import models
import matplotlib.pyplot as plt 


def img_load(path):
    img = cv2.resize(path, (16, 16))
    return img

def get_img_tensor(img_path):
    img = cv2.imread(img_path)
    img = Image.fromarray(img)
    img = torchvision.transforms.Resize((256, 256))(img)
    img = torchvision.transforms.ToTensor()(img)
    img = torchvision.transforms.Normalize(mean = (0.485, 0.456, 0.406), std = (0.229, 0.224, 0.225))(img)
    img = img.unsqueeze(0)
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

    def forward(self, x):
        x = self.model(x)

        return x


class PredictModel():
    def predict(self,file_name=None):
        if file_name==None:
            return { "answer" : "error" }
        else:
            device = torch.device('cuda')
            path="/workspaces/classification_site/media/uploads/{}".format(file_name)
            test_png = cv2.imread(path)
            test_imgs = img_load(test_png)

            transforms_test = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(
                    [0.485, 0.456, 0.406],
                    [0.229, 0.224, 0.225]
                )
            ])

            train_y = pd.read_csv('/workspaces/classification_site/product/input/train_df.csv')

            train_labels = train_y["label"]

            label_unique = sorted(np.unique(train_labels))
            label_unique = {key:value for key,value in zip(label_unique, range(len(label_unique)))}

            # Test
            batch_size = 1

            test_dataset = Custom_dataset(np.array(test_imgs), np.array(["tmp"]*len(test_imgs)), mode='test',transforms=transforms_test)
            test_loader = DataLoader(test_dataset, shuffle=False, batch_size=1)

            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            model = Network().to(device)
            model.load_state_dict(torch.load("/workspaces/classification_site/product/model/mobilenetv2.pth",map_location=device) ,strict=False)

            model.eval()
            f_pred = []

            with torch.no_grad():
                for batch in (test_loader):
                    x = torch.tensor(batch[0], dtype = torch.float32, device = device)
                    pred = model(x)
                    f_pred.extend(pred.argmax(1).detach().cpu().numpy().tolist())


            label_decoder = {val:key for key, val in label_unique.items()}
            f_result = [label_decoder[result] for result in f_pred]
            
            # grad cam
            target_layers = [model.model.features[-1]]
            cam = GradCAM(model=model, target_layers=target_layers, use_cuda=False)

            img_path_grad = path
            img = get_img_tensor(img_path_grad).to(device)
            image = cv2.imread(img_path_grad, cv2.IMREAD_COLOR)

            image = cv2.normalize(image, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

            image=cv2.resize(image, dsize=(256, 256))

            predict = int(torch.argmax(torch.nn.Softmax()(model(img))).item())
            targets = [ClassifierOutputTarget(predict)]

            grayscale_cam = cam(input_tensor=img, targets=targets)
            grayscale_cam = grayscale_cam[0, :]
            visualization = show_cam_on_image(image, grayscale_cam, use_rgb=True)
            
            plt.imshow(visualization)
            plt.savefig('/workspaces/classification_site/media/uploads/grad_cam/gradcam_{}.jpg'.format(file_name))
            grad_cam_url='https://cjfghk5697-classification-site-5764gqr4w724pp7-8000.githubpreview.dev/media/uploads/grad_cam/gradcam_{}.jpg'.format(file_name)
            
            sort_pred=sorted(pred[0].detach().cpu().numpy().tolist(),reverse=True)
            
            index_list=[0,0,0,0,0]
            sub_pred=['','','','','',]

            for i in range(0,5):
                index_list[i],sub_pred[i]=pred[0].detach().cpu().numpy().tolist().index(sort_pred[i]),int(sort_pred[i]*10)
            
            sub_result = [label_decoder[result] for result in index_list]
            
            return {"answer" : f_result[0],"sub_pred":sub_pred,"sub_result":sub_result,"grad_cam":grad_cam_url}

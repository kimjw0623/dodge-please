import torch 
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import csv

class EmbeddedDataset(torch.utils.data.Dataset):
    def __init__(self, file_name):
        # self.img_labels = pd.read_csv(annotations_file, names=['file_name', 'label'])
        self.file_name = file_name
        self.match_info_list, self.match_result_list = self._load_match_list()
        
    def __len__(self):
        with open(self.file_name, mode='r', encoding='utf-8-sig') as inp:
            reader = csv.reader(inp)
            dataset_length = len(reader)
        return dataset_length

    def __getitem__(self, idx):
        single_match_info = self.match_info_list[idx]
        single_match_result = self.match_result_list[idx]
        return single_match_info, single_match_result
    
    def _load_match_list(self):
        match_info_list = []
        match_result_list = []
        with open(self.file_name, mode='r', encoding='utf-8-sig') as inp:
            reader = csv.reader(inp)
            for rows in reader:
                match_info = rows[0]
                match_result = 0
                if rows[0][0]:
                    match_result = 1
                
                match_info_list.append(match_info)
                match_result_list.append(match_result)

        return match_info_list, match_result_list
        
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(60, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def binary_acc(y_pred, y_test):
    y_pred_tag = torch.round(torch.sigmoid(y_pred))

    correct_results_sum = (y_pred_tag == y_test).sum().float()
    acc = correct_results_sum/y_test.shape[0]
    acc = torch.round(acc * 100)
    
    return acc

train_file_name = ''
test_file_name = ''
batch_size = 32
total_epoch = 100

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

train_dataset = EmbeddedDataset(file_name=train_file_name) 
test_dataset = EmbeddedDataset(file_name=test_file_name) 

training_generator = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=False)
testing_generator = torch.utils.data.DataLoader(test_dataset, batch_size=1, shuffle=False, drop_last=False)

model = Net()

criterion = nn.BCEWithLogitsLoss()#nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

model.train()
for e in range(1, total_epoch):
    epoch_loss = 0
    epoch_acc = 0
    for X_batch, y_batch in training_generator:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        optimizer.zero_grad()
        
        y_pred = model(X_batch)
        
        loss = criterion(y_pred, y_batch)#.unsqueeze(1))
        acc = binary_acc(y_pred, y_batch)#.unsqueeze(1))
        
        loss.backward()
        optimizer.step()
        
        epoch_loss += loss.item()
        epoch_acc += acc.item()
        
    avg_loss = epoch_loss/len(training_generator)
    avg_acc = epoch_acc/len(training_generator)
    print(f'epoch {e}: | Loss: {avg_loss:.5f} | Acc: {avg_acc:.3f}')
from app.data.Repositories.CrudRepository import Repository
from app.Tools import DbUtil as dbUtil
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from Model import NeuralNet

# Get data
connectionString = dbUtil.constructConnectionString('OutdoorFusion')
dataRepository = Repository(connectionString)

order_details = dataRepository.findAll('Order_Details')
product = dataRepository.findAll('Product')
customer = dataRepository.findAll('Customer')
employee = dataRepository.findAll('Employee')
dayDate = dataRepository.findAll('Order_Date')

# Merge Data
mergedData = pd.merge(order_details, product, on='PRODUCT_id')
mergedData = pd.merge(mergedData, customer, on='CUSTOMER_id')
mergedData = pd.merge(mergedData, employee, on='EMPLOYEE_id')
mergedData = pd.merge(mergedData, dayDate, on='DAY_date')

# Select relevant columns
selectedColumns = ['CUSTOMER_country', 'PRODUCT_name', 'PRODUCT_category', 'PRODUCT_sub_category',
                   'ORDER_DETAIL_unit_price', 'DAY_QUARTER_nr', 'DAY_MONTH_nr']
selectedData = mergedData[selectedColumns]

selectedData = selectedData.dropna()

# Encode date into numeric values
typeFix = {'DAY_QUARTER_nr': 'string', 'DAY_MONTH_nr': 'string'}
selectedData = selectedData.astype(typeFix)

encodedData = pd.get_dummies(selectedData)

X = encodedData.drop('ORDER_DETAIL_unit_price', axis=1)
Y = encodedData['ORDER_DETAIL_unit_price']

X = torch.from_numpy(X.to_numpy())
Y = torch.from_numpy(Y.to_numpy())

# Create training set
randomState = 42
testSize = 0.2

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=testSize, random_state=randomState)

# Hyper parameters
batch_size = 12
hidden_size = 8
output_size = 1
input_size = X_train.shape[1]
learning_rate = 0.01
num_epochs = 100


class TestSet(Dataset):
    def __init__(self, X, y):
        self.n_samples = X.shape[0]
        self.x_data = torch.tensor(X, dtype=torch.float32)
        self.y_data = torch.tensor(y, dtype=torch.float32).view(-1, 1)

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


dataset = TestSet(X_train, y_train)
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Backward propagation loop
print('START LOOP')
for epoch in range(num_epochs):
    print(f'EPOCH : {epoch}')

    for features, labels in train_loader:
        features = features.to(device)
        labels = labels.to(device)

        outputs = model(features)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

print(f'final loss: {loss.item():.4f}')

# Save trained dataset
data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": y_train,
    "tags": X_train
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'Training complete. File save to {FILE}')

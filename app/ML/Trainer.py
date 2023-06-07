import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader

from Model import NeuralNet
from OutdoorFusionDataset import Data


class TestSet(Dataset):
    def __init__(self, X, y):
        self.n_samples = X.shape[0]
        self.x_data = torch.tensor(X, dtype=torch.float32)
        self.y_data = torch.tensor(y, dtype=torch.float32).view(-1, 1)

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


class Trainer:
    def __init__(self, X, Y, batchSize, hiddenSize, learningRate, numEpochs):
        self.X, self.Y = X, Y

        self.X = torch.from_numpy(self.X.to_numpy())
        self.Y = torch.from_numpy(self.Y.to_numpy())

        # Create training set
        self.randomState = 42
        self.testSize = 0.2

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.Y, test_size=self.testSize, random_state=self.randomState
        )

        # Hyper parameters
        self.batch_size = batchSize
        self.hidden_size = hiddenSize
        self.output_size = 1
        self.input_size = self.X_train.shape[1]
        self.learning_rate = learningRate
        self.num_epochs = numEpochs

        self.dataset = TestSet(self.X_test, self.y_test)
        self.train_loader = DataLoader(
            dataset=self.dataset, batch_size=self.batch_size, shuffle=True, num_workers=0
        )

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(self.device)

        self.model = NeuralNet(
            self.input_size, self.hidden_size, self.output_size
        ).to(self.device)

        self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.Adam(
            self.model.parameters(), lr=self.learning_rate
        )

    def train(self):
        print("START LOOP")
        for epoch in range(self.num_epochs):
            print(f"EPOCH : {epoch}")

            for features, labels in self.train_loader:
                features = features.to(self.device)
                labels = labels.to(self.device)

                outputs = self.model(features)
                loss = self.criterion(outputs, labels)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

            print(f"Epoch [{epoch + 1}/{self.num_epochs}], Loss: {loss.item():.4f}")

        print(f"final loss: {loss.item():.4f}")

    def getTrainedData(self):
        # Save trained dataset
        data = {
            "model_state": self.model.state_dict(),
            "input_size": self.input_size,
            "output_size": self.output_size,
            "hidden_size": self.hidden_size,
            "columns": self.Y,
            "tags": self.X,
        }

        return data


# Relatively low MSE
def createOrderQuantityDataset():
    data = Data()
    X, Y = data.getOrderQuantityXY()
    trainer = Trainer(X, Y, 64, 8, 0.01, 1000)

    trainer.train()
    data = trainer.getTrainedData()

    FILE = "orderquantity_data.pth"
    torch.save(data, FILE)

    print(f"Training complete. File saved to {FILE}")


# High MSE
def createUnitPriceDataset():
    data = Data()
    X, Y = data.getUnitPriceXY()
    trainer = Trainer(X, Y, 64, 8, 0.01, 1000)

    trainer.train()
    data = trainer.getTrainedData()

    FILE = "unitprice_data.pth"
    torch.save(data, FILE)

    print(f"Training complete. File saved to {FILE}")


createOrderQuantityDataset()

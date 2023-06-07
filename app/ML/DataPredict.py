import sys
sys.path.append('../')

import numpy as np
import torch
import pandas as pd
from ML.Model import NeuralNet


class Predictor:

    def __init__(self, path, columns):
        saved_data = torch.load(path)

        model_state = saved_data["model_state"]
        input_size = saved_data["input_size"]
        output_size = saved_data["output_size"]
        hidden_size = saved_data["hidden_size"]

        # Initialize the model
        self.model = NeuralNet(input_size, hidden_size, output_size)
        self.model.load_state_dict(model_state)

        # Dataset columns / maybe try to find other way to get x amount of columns
        self.XColumns = columns

    # Data should be an object like below
    # mock_data = {
    #     "CUSTOMER_country": ["USA"],
    #     "PRODUCT_name": ["LL Crankset"],
    #     "PRODUCT_category": ["Components"],
    #     "PRODUCT_sub_category": ["Cranksets"],
    #     "DAY_QUARTER_nr": ["1"],
    #     "DAY_MONTH_nr": ["1"],
    # }
    def predict(self, data, predictedValueName):
        dataFrame = pd.DataFrame(data)

        dataTensor = self.prepareValue(dataFrame)

        self.model.eval()  # Set the model to evaluation mode

        with torch.no_grad():
            predictions = self.model(dataTensor)

        # Convert the predictions to a NumPy array or DataFrame
        predictions_array = predictions.numpy()

        # Combine the input Data with the predictions (if desired)
        result_df = pd.concat([dataFrame, pd.DataFrame(predictions_array, columns=[predictedValueName])], axis=1)

        return result_df

    def prepareValue(self, dataFrame):
        dataFrame = dataFrame.astype({"DAY_QUARTER_nr": "string", "DAY_MONTH_nr": "string"})

        # One-hot encode the categorical columns
        encoded_data = pd.get_dummies(dataFrame)

        # Reorder the columns to match the model's input order
        encoded_data = encoded_data.reindex(columns=self.XColumns, fill_value=0)

        # Convert pandas DataFrame to NumPy array
        numpy_array = encoded_data.values
        numpy_array = numpy_array.astype(np.float32)

        return torch.from_numpy(numpy_array)

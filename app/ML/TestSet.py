import torch
import pandas as pd
from Model import NeuralNet
from UnitPriceData import Data

# Load the saved model
saved_data = torch.load("data.pth")
model_state = saved_data["model_state"]
input_size = saved_data["input_size"]
output_size = saved_data["output_size"]
hidden_size = saved_data["hidden_size"]

# Initialize the model
model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)

# Create mock input data
mock_data = {
    "CUSTOMER_country": ["USA", "Canada", "UK"],
    "PRODUCT_name": ["LL Crankset", "LL Road Pedal", "ML Mountain Frame-W - Silver, 38"],
    "PRODUCT_category": ["Components", "Components", "Components"],
    "PRODUCT_sub_category": ["Cranksets", "Pedals", "Mountain Frames"],
    "DAY_QUARTER_nr": ["1", "2", "3"],
    "DAY_MONTH_nr": ["1", "2", "3"],
    "DAY_date": ["2023-06-06", "2023-06-07", "2023-06-08"]
}

# Convert mock data to a DataFrame
mock_df = pd.DataFrame(mock_data)

# Preprocess the mock data
# Apply the same preprocessing steps as in the getXYTensor method
mock_df = mock_df.astype({"DAY_QUARTER_nr": "string", "DAY_MONTH_nr": "string"})

# One-hot encode the categorical columns
encoded_data = pd.get_dummies(mock_df)

d = Data()
X, Y = d.getXYTensor()

# Reorder the columns to match the model's input order
encoded_data = encoded_data.reindex(columns=X.columns, fill_value=0)
encoded_data = pd.get_dummies(encoded_data)

# Convert the preprocessed data to tensors
mock_data_tensor = torch.tensor(encoded_data.values, dtype=torch.float32)

# Make predictions
model.eval()  # Set the model to evaluation mode
with torch.no_grad():
    predictions = model(mock_data_tensor)

# Convert the predictions to a NumPy array or DataFrame
predictions_array = predictions.numpy()

# Combine the input data with the predictions (if desired)
result_df = pd.concat([mock_df, pd.DataFrame(predictions_array, columns=["Predicted_price"])], axis=1)

# Print the result
print('RESULTS')
print(result_df)

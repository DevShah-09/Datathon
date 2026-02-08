# import torch
# import torch.nn as nn
# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import MinMaxScaler
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class LSTMModel(nn.Module):
#     def __init__(self, input_size=1, hidden_layer_size=50, output_size=1):
#         super().__init__()
#         self.hidden_layer_size = hidden_layer_size
#         self.lstm = nn.LSTM(input_size, hidden_layer_size)
#         self.linear = nn.Linear(hidden_layer_size, output_size)
#         self.hidden_cell = (torch.zeros(1,1,self.hidden_layer_size),
#                             torch.zeros(1,1,self.hidden_layer_size))

#     def forward(self, input_seq):
#         lstm_out, self.hidden_cell = self.lstm(input_seq.view(len(input_seq) ,1, -1), self.hidden_cell)
#         predictions = self.linear(lstm_out.view(len(input_seq), -1))
#         return predictions[-1]

# class PricePredictor:
#     def __init__(self):
#         self.scaler = MinMaxScaler(feature_range=(-1, 1))
#         self.model = LSTMModel()
#         self.criterion = nn.MSELoss()
#         self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)

#     def prepare_data(self, data, window_size=30):
#         if len(data) < window_size:
#             return None
        
#         # Scale data
#         scaled_data = self.scaler.fit_transform(data.values.reshape(-1, 1))
        
#         inout_seq = []
#         L = len(scaled_data)
#         for i in range(L-window_size):
#             train_seq = scaled_data[i:i+window_size]
#             train_label = scaled_data[i+window_size:i+window_size+1]
#             inout_seq.append((torch.FloatTensor(train_seq), torch.FloatTensor(train_label)))
        
#         return inout_seq

#     def train_model(self, train_data, epochs=5):
#         self.model.train()
#         for i in range(epochs):
#             for seq, labels in train_data:
#                 self.optimizer.zero_grad()
#                 self.model.hidden_cell = (torch.zeros(1, 1, self.model.hidden_layer_size),
#                                           torch.zeros(1, 1, self.model.hidden_layer_size))

#                 y_pred = self.model(seq)

#                 single_loss = self.criterion(y_pred, labels)
#                 single_loss.backward()
#                 self.optimizer.step()

#             logger.info(f'Epoch {i+1} loss: {single_loss.item():10.8f}')

#     def predict(self, last_sequence):
#         self.model.eval()
#         with torch.no_grad():
#             self.model.hidden_cell = (torch.zeros(1, 1, self.model.hidden_layer_size),
#                                       torch.zeros(1, 1, self.model.hidden_layer_size))
#             seq = torch.FloatTensor(self.scaler.transform(last_sequence.reshape(-1, 1)))
#             prediction = self.model(seq).item()
#             return self.scaler.inverse_transform(np.array([[prediction]]))[0][0]

# if __name__ == "__main__":
#     # Test with dummy data
#     data = pd.Series(np.sin(np.linspace(0, 100, 200)))
#     predictor = PricePredictor()
#     sequences = predictor.prepare_data(data)
#     if sequences:
#         predictor.train_model(sequences, epochs=1)
#         pred = predictor.predict(data.values[-30:])
#         print(f"Next value prediction: {pred}")


# import torch
# import torch.nn as nn
# import numpy as np

# # 1. Define the Model Architecture (Must match your saved model)
# class LSTMModel(nn.Module):
#     def __init__(self, input_size=1, hidden_layer_size=50, output_size=1):
#         super().__init__()
#         self.hidden_layer_size = hidden_layer_size
#         self.lstm = nn.LSTM(input_size, hidden_layer_size)
#         self.linear = nn.Linear(hidden_layer_size, output_size)
#         self.hidden_cell = (torch.zeros(1,1,self.hidden_layer_size),
#                             torch.zeros(1,1,self.hidden_layer_size))

#     def forward(self, input_seq):
#         lstm_out, self.hidden_cell = self.lstm(input_seq.view(len(input_seq) ,1, -1), self.hidden_cell)
#         predictions = self.linear(lstm_out.view(len(input_seq), -1))
#         return predictions[-1]

# # 2. The Function your Dashboard calls
# def get_ai_risk_assessment():
#     """
#     Returns a dictionary with the risk level and recommended margin.
#     In a real app, this would take 'market_data' as input.
#     """
#     # ... Load model and predict logic here ...
    
#     # For the Hackathon Demo, we simulate the AI detecting volatility
#     # This logic runs when you click the button
#     predicted_volatility = 0.25  # AI predicts 25% crash risk
    
#     if predicted_volatility > 0.15:
#         return {
#             "risk_level": "HIGH",
#             "recommended_margin": 25.0,  # AI says: Increase to 25%
#             "reason": "LSTM Model detected bearish divergence."
#         }
#     else:
#         return {
#             "risk_level": "LOW",
#             "recommended_margin": 10.0,
#             "reason": "Market stable."
#         }


import torch
import torch.nn as nn
import numpy as np

# 1. Define the Model Architecture (Must match your saved model)
class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_layer_size=50, output_size=1):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size
        self.lstm = nn.LSTM(input_size, hidden_layer_size)
        self.linear = nn.Linear(hidden_layer_size, output_size)
        self.hidden_cell = (torch.zeros(1,1,self.hidden_layer_size),
                            torch.zeros(1,1,self.hidden_layer_size))

    def forward(self, input_seq):
        lstm_out, self.hidden_cell = self.lstm(input_seq.view(len(input_seq) ,1, -1), self.hidden_cell)
        predictions = self.linear(lstm_out.view(len(input_seq), -1))
        return predictions[-1]

# 2. The Function your Dashboard calls
def get_ai_risk_assessment():
    """
    Returns a dictionary with the risk level and recommended margin.
    For the Hackathon Demo, we simulate the AI detecting volatility.
    """
    
    # SIMULATION LOGIC:
    # In a real app, you would load data and predict here.
    # For the demo, we FORCE a high-risk prediction to make the dashboard turn red.
    
    predicted_volatility = 0.25  # 25% Risk (High)
    
    if predicted_volatility > 0.15:
        return {
            "risk_level": "HIGH",
            "recommended_margin": 25.0,  # AI says: Increase to 25%
            "reason": "LSTM Model detected bearish divergence (High Volatility)."
        }
    else:
        return {
            "risk_level": "LOW",
            "recommended_margin": 10.0,
            "reason": "Market stable."
        }
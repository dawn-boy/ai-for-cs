import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class GNNModel(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = GCNConv(num_features, 16)
        self.conv2 = GCNConv(16, num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)

def train_synthetic_model():
    """
    Trains a dummy model on synthetic data to be used for inference.
    In a real scenario, this would be pre-trained on a large dataset.
    """
    model = GNNModel(num_features=5, num_classes=3)
    # 0: Safe, 1: Vulnerable, 2: Critical Exploit Path
    
    # Synthetic data
    x = torch.tensor([
        [0, 0, 2, 0, 0], # App (Safe)
        [1, 1, 1, 0, 0], # Lib A (Safe)
        [1, 1, 0, 1, 1], # Lib B (Vulnerable, Leaf)
        [2, 1, 0, 1, 1], # Lib C (Critical, deep)
    ], dtype=torch.float)
    
    edge_index = torch.tensor([
        [0, 0, 1],
        [1, 2, 3]
    ], dtype=torch.long)
    
    y = torch.tensor([0, 0, 1, 2], dtype=torch.long)
    
    from torch_geometric.data import Data
    data = Data(x=x, edge_index=edge_index, y=y)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    
    model.train()
    for epoch in range(50):
        optimizer.zero_grad()
        out = model(data)
        loss = F.nll_loss(out, data.y)
        loss.backward()
        optimizer.step()
        
    return model

def predict_risk(model, data):
    model.eval()
    with torch.no_grad():
        out = model(data)
        pred = out.argmax(dim=1)
        probs = torch.exp(out)
    return pred, probs

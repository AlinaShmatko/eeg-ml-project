import copy
import torch

from torch import nn
from torch.utils.data import TensorDataset, DataLoader
from braindecode.models import EEGNet, Deep4Net, ATCNet
from sklearn.metrics import balanced_accuracy_score


def train_model(X_train, y_train, X_val, y_val, architecture="EEGNet",
                sfreq=160, max_epochs=60, patience=10, batch_size=32, seed=42):
    torch.manual_seed(seed)

    architectures = {"EEGNet": EEGNet, "Deep4Net": Deep4Net, "ATCNet": ATCNet}
    if architecture not in architectures:
        raise ValueError(f"Unknown architecture: {architecture}")

    model_class = architectures[architecture]
    model = model_class(n_chans=X_train.shape[1], n_outputs=2,
                        n_times=X_train.shape[-1], sfreq=sfreq)

    train_dataset = TensorDataset(torch.from_numpy(X_train),
                                  torch.tensor(y_train, dtype=torch.long))
    val_dataset = TensorDataset(torch.from_numpy(X_val),
                                torch.tensor(y_val, dtype=torch.long))

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True,
                              generator=torch.Generator().manual_seed(seed))
    val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=0.0001)

    best_val_loss = float("inf")
    best_epoch = 0
    best_weights = None
    epochs_without_improvement = 0
    history = []

    for epoch in range(1, max_epochs + 1):
        model.train()
        train_loss = 0.0

        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            loss = criterion(model(X_batch), y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * len(y_batch)

        model.eval()
        val_loss = 0.0
        val_predictions = []

        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                output = model(X_batch)
                val_loss += criterion(output, y_batch).item() * len(y_batch)
                val_predictions.extend(output.argmax(dim=1).cpu().numpy())

        train_loss /= len(train_dataset)
        val_loss /= len(val_dataset)
        val_ba = balanced_accuracy_score(y_val, val_predictions)

        history.append({"Epoch": epoch, "Train Loss": train_loss,
                        "Val Loss": val_loss, "Val BA": val_ba})

        if val_loss < best_val_loss - 1e-4:
            best_val_loss = val_loss
            best_epoch = epoch
            best_weights = copy.deepcopy(model.state_dict())
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1

        if epochs_without_improvement >= patience:
            break

    model.load_state_dict(best_weights)

    return model, history, best_epoch, best_val_loss


def train_eegnet(X_train, y_train, X_val, y_val, sfreq=160, max_epochs=60,
                 patience=10, batch_size=32, seed=42):
    return train_model(X_train, y_train, X_val, y_val, architecture="EEGNet",
                       sfreq=sfreq, max_epochs=max_epochs, patience=patience,
                       batch_size=batch_size, seed=seed)
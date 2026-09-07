"""Reproducible CPU linear-regression training for Week 3 q12."""

import torch
from torch import nn


def train(steps: int = 200) -> tuple[nn.Linear, float]:
    """Fit y = 3x - 1 and return the model and final loss."""
    torch.manual_seed(20260907)
    x = torch.linspace(-1, 1, 101).reshape(-1, 1)
    y = 3 * x - 1

    model = nn.Linear(1, 1)
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

    model.train()
    for _ in range(steps):
        prediction = model(x)
        loss = loss_fn(prediction, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        final_loss = loss_fn(model(x), y).item()
    return model, final_loss


def main() -> None:
    model, final_loss = train()
    print(f"final_loss={final_loss:.8f}")
    print(f"weight={model.weight.item():.6f}")
    print(f"bias={model.bias.item():.6f}")


if __name__ == "__main__":
    main()


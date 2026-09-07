"""Run the same training twice and compare every learned tensor."""

import json

import torch
from torch import nn


def train_once(seed: int) -> tuple[dict[str, torch.Tensor], float]:
    torch.manual_seed(seed)
    x = torch.linspace(-1, 1, 101).reshape(-1, 1)
    y = 3 * x - 1
    model = nn.Linear(1, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    loss_fn = nn.MSELoss()
    for _ in range(120):
        optimizer.zero_grad()
        loss = loss_fn(model(x), y)
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        final_loss = loss_fn(model(x), y).item()
    return {name: value.detach().clone() for name, value in model.state_dict().items()}, final_loss


def audit(seed: int = 20260907) -> dict[str, object]:
    first, first_loss = train_once(seed)
    second, second_loss = train_once(seed)
    exact = all(torch.equal(first[name], second[name]) for name in first)
    return {
        "seed": seed,
        "exact_state_match": exact,
        "loss_match": first_loss == second_loss,
        "final_loss": first_loss,
    }


if __name__ == "__main__":
    report = audit()
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["exact_state_match"] and report["loss_match"] else 1)


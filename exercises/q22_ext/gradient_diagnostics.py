"""Record gradient norms and apply clipping during a stable training run."""

import json
import math

import torch
from torch import nn


def train_with_diagnostics(steps: int = 180, max_norm: float = 1.0) -> dict[str, float]:
    torch.manual_seed(20260907)
    x = torch.linspace(-2, 2, 201).reshape(-1, 1)
    y = 5 * x + 2
    model = nn.Linear(1, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.08)
    loss_fn = nn.MSELoss()
    observed = []
    for _ in range(steps):
        optimizer.zero_grad()
        loss = loss_fn(model(x), y)
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=max_norm)
        observed.append(float(norm))
        optimizer.step()
    with torch.no_grad():
        final_loss = float(loss_fn(model(x), y))
    if not all(math.isfinite(value) for value in observed + [final_loss]):
        raise RuntimeError("non-finite training value detected")
    return {
        "initial_grad_norm": observed[0],
        "maximum_grad_norm": max(observed),
        "final_grad_norm": observed[-1],
        "final_loss": final_loss,
        "weight": float(model.weight.item()),
        "bias": float(model.bias.item()),
    }


if __name__ == "__main__":
    report = train_with_diagnostics()
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["final_loss"] < 0.001 else 1)


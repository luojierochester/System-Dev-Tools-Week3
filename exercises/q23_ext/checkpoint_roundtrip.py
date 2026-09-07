"""Save and reload a training checkpoint, then verify identical predictions."""

import json
from pathlib import Path
import tempfile

import torch
from torch import nn


def roundtrip() -> dict[str, object]:
    torch.manual_seed(20260907)
    x = torch.linspace(-1, 1, 101).reshape(-1, 1)
    y = 3 * x - 1
    model = nn.Linear(1, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    loss_fn = nn.MSELoss()
    for step in range(100):
        optimizer.zero_grad()
        loss = loss_fn(model(x), y)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        before = model(x)

    with tempfile.TemporaryDirectory(prefix="checkpoint-") as directory:
        checkpoint = Path(directory) / "model.pt"
        torch.save(
            {"model": model.state_dict(), "optimizer": optimizer.state_dict(), "step": step + 1},
            checkpoint,
        )
        restored = nn.Linear(1, 1)
        payload = torch.load(checkpoint, map_location="cpu", weights_only=True)
        restored.load_state_dict(payload["model"])
        restored.eval()
        with torch.no_grad():
            after = restored(x)
        return {
            "step": payload["step"],
            "exact_prediction_match": torch.equal(before, after),
            "max_absolute_difference": float((before - after).abs().max()),
            "checkpoint_bytes": checkpoint.stat().st_size,
        }


if __name__ == "__main__":
    report = roundtrip()
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["exact_prediction_match"] else 1)


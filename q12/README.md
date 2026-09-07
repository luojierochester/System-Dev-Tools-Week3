# q12 - 可复现的 PyTorch 线性回归训练

`train.py` 使用固定随机种子 `20260907`，在 CPU 上拟合 `y = 3x - 1`。
每轮执行 `zero_grad()`、`backward()` 和 `step()`；训练结束后调用 `model.eval()`，
并在 `torch.no_grad()` 中计算最终指标。

```bash
python train.py
python -m unittest -v test_train.py
```

实现从随机初始化开始通过梯度下降学习参数，没有直接把权重和偏置赋值为 3 和 -1。
验证要求：最终损失小于 0.001，且学习到的参数接近目标值。

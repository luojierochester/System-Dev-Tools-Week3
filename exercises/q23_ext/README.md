# Ex11 - PyTorch 检查点往返验证

脚本保存模型参数、优化器状态和训练步数，在一个全新模型中加载检查点，然后逐元素比较
加载前后的预测。使用 `map_location="cpu"` 和 `weights_only=True`，兼顾可移植性与安全性。

```bash
python checkpoint_roundtrip.py
python -m unittest -v test_checkpoint_roundtrip.py
```

# Ex10 - 梯度诊断与裁剪

训练循环在 `backward()` 后记录梯度范数，并通过 `clip_grad_norm_` 把实际更新限制在阈值内。
脚本检查所有指标有限、最终梯度收敛且损失达标，适合定位梯度爆炸或训练停滞。

```bash
python gradient_diagnostics.py
```

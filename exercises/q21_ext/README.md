# Ex09 - PyTorch 可复现性审计

脚本在 CPU 上用相同随机种子独立训练两次，逐张量比较 `state_dict`，并核对最终损失。
这比只观察“损失差不多”更严格，可发现随机种子遗漏或非确定性路径。

```bash
python reproducibility_audit.py
python -m unittest -v test_reproducibility_audit.py
```


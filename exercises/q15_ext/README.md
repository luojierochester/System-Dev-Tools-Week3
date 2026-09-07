# Ex03 - 公共 API 兼容性门禁

`api_guard.py` 通过 AST 提取两个 Python 模块的公共函数和类，报告新增、删除符号；若存在删除，
返回状态码 1。它可在发布新 Wheel 前阻止无意的破坏性 API 变更。

```bash
python api_guard.py old.py new.py
python -m unittest -v test_api_guard.py
```


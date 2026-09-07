# q09 - 从源码构建并安装 Wheel

项目采用 `src/` 布局，发布名为 `greetlab-24020007086`，命令行入口为 `sdt-greet`。

```bash
python -m build
python -m venv .clean-venv
.clean-venv/Scripts/python -m pip install --no-index --find-links dist greetlab-24020007086
cd ..
q09/.clean-venv/Scripts/sdt-greet --name 24020007086
```

期望输出：`Hello, 24020007086!`。最后一步在 `q09` 目录之外执行，证明命令来自已安装的 Wheel，
而不是直接从源码目录导入。

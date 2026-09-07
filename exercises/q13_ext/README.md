# Ex01 - Wheel 元数据检查器

`wheel_inspector.py` 直接读取 Wheel 的 ZIP 结构，核对发行名、版本、兼容标签和控制台入口，
无需先安装包。它能在发布前发现错包、漏入口和错误平台标签。

```bash
python wheel_inspector.py ../../q09/dist/*.whl
python -m unittest -v test_wheel_inspector.py
```


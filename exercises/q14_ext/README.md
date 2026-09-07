# Ex02 - 一次性环境 Wheel 冒烟测试

工具创建临时虚拟环境，使用 `--no-index --no-deps` 只安装指定 Wheel，并在临时目录中运行
`sdt-greet`。上下文结束时临时环境自动清理，避免本机已有源码或依赖掩盖打包错误。

```bash
python verify_wheel.py ../../q09/dist/greetlab_24020007086-0.1.0-py3-none-any.whl
```

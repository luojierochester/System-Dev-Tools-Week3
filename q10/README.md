# q10 - 可验证的智能体修复循环

先把 q09 的实现复制到本目录，再添加“纯空白姓名必须以状态码 2 退出”的失败测试。
提交 `test(q10): reproduce blank-name CLI defect` 保存红灯阶段；随后只修改姓名校验逻辑并复测。

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -m pytest -q
```

最终 2 项测试通过：正常姓名在去除两端空白后输出问候语，纯空白姓名由 argparse 写入 stderr 并退出 2。

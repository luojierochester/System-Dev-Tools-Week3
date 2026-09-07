# Ex05 - 编程智能体任务契约

`prompt_contract.py` 要求任务明确给出目标、约束、测试命令和可修改文件，并拒绝绝对路径或
`..` 越界路径。结构化契约让“修一下”变成可验证、有限范围的工作单。

```bash
python prompt_contract.py example_contract.json
```


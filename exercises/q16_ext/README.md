# Ex04 - 智能体补丁范围门禁

`patch_scope_guard.py` 对照允许的目录前缀检查修改文件列表。智能体完成小修复后，可把
`git diff --name-only` 的结果交给该工具，防止无关 README、配置或其他模块被一起改动。

```bash
python patch_scope_guard.py --allow q10 q10/src/greetlab/cli.py q10/tests/test_cli.py
```

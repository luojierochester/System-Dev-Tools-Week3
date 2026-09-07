1. 核心提示：仅修复纯空白姓名，保持 CLI 入口与正常输出兼容，并运行 `pytest -q`。
2. 红灯验证：原实现输出 `Hello,    !`，测试以 “DID NOT RAISE SystemExit” 失败。
3. 智能体改动：对姓名执行 `strip()`，空值调用 `parser.error()`，并补充正常姓名回归测试。
4. 人工验证：检查 diff 仅涉及 CLI、测试与记录；2 项测试通过，无无关修改。

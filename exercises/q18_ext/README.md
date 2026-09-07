# Ex06 - 有界验证循环

`verified_loop.py` 重复运行明确的验证命令，记录每次退出码、耗时和输出；成功立即停止，
单次超时记为 124，最大尝试次数限制死循环。JSON 记录适合交给人工复核或 CI 归档。

```bash
python verified_loop.py --attempts 2 -- python -c "print('verified')"
```

# Issue：拒绝纯空白姓名参数

**环境**：Windows，Python 与 greetlab 版本待确认。  
**复现**：运行 `sdt-greet --name " "`。  
**期望**：stderr 提示姓名不能为空，并以状态码 2 退出。  
**实际**：输出 `Hello,  !`，状态码为 0。

## 提交信息

**Reject blank names in the greeting CLI**

纯空白参数会生成无意义问候且错误地表示成功。现对参数去除首尾空白，空值通过 argparse 报错并退出 2，同时保留正常姓名行为。

## 评审意见

**Blocking**：当前实现未校验 `name.strip()`，纯空白输入仍返回成功，调用方会把无效数据当作有效结果。请在输出前拒绝空值，补充退出码 2 和 stderr 内容的自动化测试后再合并。


# 使用 TestClaw 配置项、验证点与业务命令映射

本文件描述 `testclaw-cli` 在 `testclaw-cli` 主路径下需要关注的配置项、验证点和业务命令映射。

## 核心对象

- `TestClaw Server`
  - TestClaw 平台后端与前端访问地址
  - 通常作为 `testclaw config set base_url` 的值
- `testclaw-cli`
  - 本地命令行工具，可执行命令是 `testclaw`
  - 负责登录、查询设备、占用设备、应用操作、套件执行与结果查询
- `TestClaw Agent`
  - 真正连接设备、执行 case、采集录屏/日志/抓包/性能/截图的执行端

## CLI 配置

检查环境：

```bash
testclaw --json doctor
```

设置服务地址：

```bash
testclaw config set base_url https://testclaw.dev.ad2.cc
```

登录：

```bash
testclaw login
```

验证当前用户：

```bash
testclaw --json whoami
```

推荐在更新 skill 内容后同步重打包：

```bash
python3 testclaw-skills/testclaw-cli/scripts/package_skill.py
```

更新 skill 资料后，建议先做引用检查：

```bash
python3 testclaw-skills/testclaw-cli/scripts/lint_skill_refs.py
```

打包完成后，建议做完整性检查：

```bash
python3 testclaw-skills/testclaw-cli/scripts/check_skill_integrity.py
```

## 服务端验证点

### TestClaw Server 访问

```bash
curl -I https://testclaw.dev.ad2.cc
```

用途：

- 确认 TestClaw Server 可访问
- 区分“服务端不可达”和“CLI 登录态有问题”

### TestClaw 当前用户

```bash
testclaw --json whoami
```

用途：

- 验证 OAuth 登录态
- 验证当前用户权限基础可用

## 业务命令映射

| 用户意图 | 常见表达 | 优先命令 |
| --- | --- | --- |
| 环境检查 | doctor、检查 TestClaw | `testclaw --json doctor` |
| 查询当前用户 | 当前连的是谁、登录用户是谁 | `testclaw --json whoami` |
| 查询项目 | 查看项目、列出项目 | `testclaw --json project list` |
| 查询设备 | 查看空闲设备、在线设备、设备状态 | `testclaw --json device list` |
| 设备占用与调试准备 | 占用设备、准备 Android 调试 | `testclaw --json device prepare-android-debug` |
| 释放设备 | 释放设备、结束占用 | `testclaw --json device release` |
| 查看应用 | 看设备装了什么 app | `testclaw --json app list-installed` |
| 应用安装 | 上传 apk、安装应用 | `testclaw --json package upload`、`testclaw --json app install` |
| 应用控制 | 打开 app、停止 app、卸载 app | `testclaw --json app open`、`testclaw --json app kill`、`testclaw --json app uninstall` |
| 创建测试资产 | 创建模块、用例、步骤、套件 | `testclaw --json module create`、`testclaw --json case create`、`testclaw --json step create`、`testclaw --json suite create` |
| 套件执行与结果 | 执行套件、查看执行结果 | `testclaw --json suite run`、`testclaw --json result get` |
| 原始接口读取 | CLI 高层命令不覆盖 | `testclaw --json raw request --method GET --path ...` |

## 业务阶段不应优先做的事

- 把所有请求都退回“先配置 TestClaw”
- 直接写裸 `adb` 脚本替代 `testclaw-cli`
- 用 web 搜索代替真机验证
- 只给测试建议，不真正调用 TestClaw CLI 命令
- 把 evidence workflow 当成可选项

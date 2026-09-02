# 使用 TestClaw 流程

## CLI 自举安装流程

适用于“用户已命中 TestClaw skill，但当前环境还没有安装 `testclaw-cli`”。

### 1. 先检查 CLI 是否存在

优先检查：

```bash
command -v testclaw
```

如果已经存在，再执行：

```bash
testclaw --json doctor
```

### 2. 缺失时自动安装 CLI

如果 `testclaw` 不存在，且当前 Agent 环境允许运行 shell、联网并安装全局 npm 包，优先执行：

```bash
npm install -g git+https://github.com/liam798/testclaw-cli.git
```

### 3. 安装后立即回检

安装成功后至少验证：

```bash
testclaw --help
testclaw --json doctor
```

### 4. 再进入配置与登录

CLI 可用后，再继续：

```bash
testclaw config set base_url https://testclaw.vvicat.dev
testclaw login
testclaw --json whoami
```

### 5. 无法自动安装时的处理

如果遇到下面任一情况，不要假装 CLI 已就绪：

- 没有 `npm`
- 没有网络权限
- 当前 Agent 禁止执行安装命令
- 全局安装失败

此时要明确告诉用户阻塞点，并给出最短补救命令。

## CLI 登录流程

适用于“用户需要通过 `testclaw-cli` 连接 TestClaw Server 并完成浏览器 OAuth 登录”。

### 1. 明确 TestClaw Server 地址

常见形态：

```text
http://127.0.0.1:3002
https://testclaw.dev.ad2.cc
```

如果用户给的是前端访问地址，通常可直接作为 `base_url`；API 前缀由 CLI 配置或默认值处理。

### 2. 配置 CLI

优先执行：

```bash
testclaw config set base_url https://testclaw.vvicat.dev
```

配置后检查：

```bash
testclaw --json doctor
```

### 3. 执行登录

指导用户执行：

```bash
testclaw login
```

该命令会打开浏览器完成 OAuth / TestClaw 登录，并在本地保存登录态。

### 4. 验证登录

登录后至少确认：

```bash
testclaw --json whoami
```

如果能返回当前用户信息，说明 CLI 登录闭环完成。

## 业务执行流程

适用于“用户已经明确要用 TestClaw 做设备、应用、执行或 UI 校对”。

### 1. 先识别业务目标

- 设备类：查看设备、占用设备、释放设备、准备调试
- 应用类：查看应用、上传安装包、安装、打开、停止、卸载
- 执行类：创建模块/用例/步骤/套件、执行套件、查结果
- 巡检类：APK/App 冒烟、UI 校对、真机打开页面、截图取证
- 证据类：录屏、日志、网络抓包、性能采集、报告归档

### 2. 直接走 testclaw-cli

如果当前 `testclaw` 可用，不要优先退回本地裸 `adb`、web 或纯文本建议。

优先原则：

- 用户说 `TestClaw + 设备动作` -> 先列设备候选，再根据用户指定或确认执行设备命令
- 用户说 `TestClaw + 应用动作` -> 直接选 TestClaw 应用命令
- 用户说 `TestClaw + 执行动作` -> 直接选 TestClaw 资产/执行命令
- 用户说 `TestClaw + UI 校对/冒烟/自动化测试` -> 先列设备候选；用户指定或确认后，再走设备准备 + evidence workflow

### 3. 标准设备流

1. 先列出空闲或在线设备
2. 把候选设备列给用户，等待用户指定 `deviceId` / `udid` / 设备名称；用户明确授权时才可自动选择
3. 对指定或确认的设备执行占用并准备 Android 调试
4. 执行应用操作、页面检查或套件执行
5. 结束后释放设备

### 4. 标准应用流

1. 列出设备
2. 等待用户指定设备或确认自动选择
3. 对指定或确认的设备占用并准备调试
4. 按需执行上传包、安装、打开、停止、卸载
5. 返回结果与设备状态
6. 结束后释放设备

### 5. 标准 UI / APK 冒烟流

1. 查空闲设备
2. 列出候选并等待用户指定设备或确认自动选择
3. 对指定或确认的设备占用并准备调试
4. 启动 evidence workflow
5. 安装或打开目标应用
6. 检查布局、文案、错位、遮挡、截断、空状态、弹窗、崩溃
7. 输出问题清单、录屏、日志、抓包、截图、性能数据和结论
8. 释放设备

### 6. 标准执行流

1. 先查现有项目、模块、用例、步骤、套件
2. 资产不足时补齐
3. 列出候选设备，等待用户指定或确认自动选择
4. 使用指定或确认的设备运行 suite，并确保平台 evidence workflow 开启
5. 拉取执行结果
6. 需要时继续进入失败分析、结果整理或缺陷闭环

## 登录失效处理

如果调用阶段遇到：

- 未登录
- token 过期或刷新失败
- `401` / `403`
- 当前用户查询失败

不要继续分析业务逻辑，先判断为“当前 CLI 登录态不可用”。

处理顺序：

1. 保留当前 `base_url` 配置不动
2. 重新执行 `testclaw login`
3. 登录成功后用 `testclaw --json whoami` 重新验证
4. 再回到业务流程

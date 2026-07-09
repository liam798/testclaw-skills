# 使用 TestClaw 流程

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
testclaw config set base_url https://testclaw.dev.ad2.cc
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

- 用户说 `TestClaw + 设备动作` -> 直接选 TestClaw 设备命令
- 用户说 `TestClaw + 应用动作` -> 直接选 TestClaw 应用命令
- 用户说 `TestClaw + 执行动作` -> 直接选 TestClaw 资产/执行命令
- 用户说 `TestClaw + UI 校对/冒烟/自动化测试` -> 直接走设备准备 + evidence workflow

### 3. 标准设备流

1. 先列出空闲或在线设备
2. 选择可用设备
3. 占用设备并准备 Android 调试
4. 执行应用操作、页面检查或套件执行
5. 结束后释放设备

### 4. 标准应用流

1. 列出设备
2. 占用并准备调试
3. 按需执行上传包、安装、打开、停止、卸载
4. 返回结果与设备状态
5. 结束后释放设备

### 5. 标准 UI / APK 冒烟流

1. 查空闲设备
2. 占用并准备调试
3. 启动 evidence workflow
4. 安装或打开目标应用
5. 检查布局、文案、错位、遮挡、截断、空状态、弹窗、崩溃
6. 输出问题清单、录屏、日志、抓包、截图、性能数据和结论
7. 释放设备

### 6. 标准执行流

1. 先查现有项目、模块、用例、步骤、套件
2. 资产不足时补齐
3. 选择设备执行
4. 运行 suite，并确保平台 evidence workflow 开启
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

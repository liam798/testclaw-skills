# 使用 TestClaw 触发样例与回归样例

## 应命中：登录配置类

```text
帮我配置 TestClaw CLI 并登录。
```

期望：

- 命中 `testclaw-cli`
- 走 CLI 登录流程
- 引导 `testclaw config set base_url ...` 和 `testclaw login`

## 应命中：设备类

```text
用 TestClaw 帮我找一台空闲 Android 设备。
```

期望：

- 命中 `testclaw-cli`
- 优先执行 `testclaw --json device list`

## 应命中：应用类

```text
帮我把 apk 上传到 TestClaw 然后安装到空闲设备上。
```

期望：

- 命中 `testclaw-cli`
- 优先执行 `testclaw --json package upload` 和 `testclaw --json app install`

## 应命中：执行类

```text
帮我在 TestClaw 上执行这个套件并拉结果。
```

期望：

- 命中 `testclaw-cli`
- 优先执行 `testclaw --json suite run` 和 `testclaw --json result get`
- 校验证据链是否包含录屏、日志、抓包、截图和性能数据

## 应命中：APK 自动化测试

```text
使用 TestClaw 自动化测试这个 APK。
```

期望：

- 命中 `testclaw-cli`
- 优先查 suite；无 suite 时进入 testclaw-cli 手工冒烟模式
- 必须采集完整 evidence workflow

## 不应命中

```text
帮我写一个 React 表单组件。
```

期望：

- 不应优先命中 `testclaw-cli`
- 走前端开发相关能力

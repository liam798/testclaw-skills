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
- 不自动占用；列出候选后等待用户指定或确认自动选择

## 应命中：应用类

```text
帮我把 apk 上传到 TestClaw。
```

期望：

- 命中 `testclaw-cli`
- 优先执行 `testclaw --json package upload`

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
- 涉及真机前先列出设备候选，等待用户指定或确认自动选择
- 必须采集完整 evidence workflow

## 应命中：真机浏览器网页巡检

```text
使用这台 TestClaw 设备打开浏览器加载百度，并把返回的内容总结给我。
```

期望：

- 命中 `testclaw-cli`
- 如果用户说“这台设备”但上下文中已有明确 `deviceId` / `udid`，可使用该设备；否则必须先列设备候选并等待指定
- 打开浏览器或访问网页前必须完成 evidence preflight：artifacts 目录、录屏、日志起点、网络记录、基线截图、基线 Activity/性能信息
- 不得先打开网页、截图或读取页面内容后再补录证据
- 最终回复必须列出 `video`、`log`、`network`、`screenshots`、`performance`、`structured report` 六类证据路径或缺失原因

反例：

```text
先 prepare-android-debug，然后直接 adb am start 打开 Chrome，再截图总结页面。
```

问题：

- 跳过了 evidence preflight
- 缺少全程录屏、日志起点、网络记录和结构化报告
- 不能包装成完整 TestClaw 验证结论，必须标注证据不完整并建议重跑

## 不应命中

```text
帮我写一个 React 表单组件。
```

期望：

- 不应优先命中 `testclaw-cli`
- 走前端开发相关能力

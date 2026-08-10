# Using TestClaw 召回验收矩阵

## 验收目标

- 用户提到 `TestClaw` 且目标是设备、应用、执行、UI 校对或自动化测试时，应优先命中 `testclaw-cli`
- 已登录场景不应被误导回配置话术
- 业务请求应优先落到 `testclaw-cli` 命令，而不是 shell、web 或通用建议
- 所有 case 都必须执行统一 evidence workflow
- 设备相关请求必须先列出候选设备；用户未指定或未明确授权自动选择时，不得直接占用或准备调试
- 真实设备浏览器访问网页、截图确认、页面内容总结必须按手工冒烟处理，不能绕过 evidence preflight

## 验收表

| 编号 | 用户问法 | 期望命中 | 期望路由 | 关键动作 |
| --- | --- | --- | --- | --- |
| R1 | 帮我配置 TestClaw CLI 并登录 | `testclaw-cli` | CLI 登录流 | `testclaw config set`、`testclaw login` |
| R2 | testclaw-cli 调用失败，帮我查是不是登录态过期 | `testclaw-cli` | 登录态排查流 | `testclaw --json doctor`、`testclaw --json whoami` |
| R3 | 用 TestClaw 帮我找一台空闲 Android 设备 | `testclaw-cli` | 设备流 | `testclaw --json device list` |
| R4 | 占用一台 TestClaw 设备并准备调试 | `testclaw-cli` | 设备流 | 先 `testclaw --json device list`；用户指定或确认后再 `testclaw --json device prepare-android-debug --device-id <id>` |
| R5 | 释放刚才那台 TestClaw 设备 | `testclaw-cli` | 设备流 | `testclaw --json device release` |
| R6 | 用 TestClaw 看下设备装了哪些 app | `testclaw-cli` | 应用流 | `testclaw --json app list-installed --device-id <id>` |
| R7 | 上传 apk 到 TestClaw | `testclaw-cli` | 应用流 | `testclaw --json package upload` |
| R8 | 在 TestClaw 真机上打开应用 | `testclaw-cli` | 应用流 | `testclaw --json app open --device-id <id>` |
| R9 | 用 TestClaw 创建模块、用例和步骤 | `testclaw-cli` | 执行资产流 | 资产类 CLI 命令 |
| R10 | 帮我在 TestClaw 上执行套件并拉结果 | `testclaw-cli` | 执行流 | `testclaw --json suite run`、`testclaw --json result get` |
| R11 | 用 TestClaw 空闲设备做 UI 校对 | `testclaw-cli` | UI 校对流 | 设备候选 -> 用户指定或确认 -> 设备准备 -> evidence workflow -> 真机检查 -> 释放 |
| R12 | 使用 TestClaw 自动化测试这个 APK | `testclaw-cli` | APK 测试流 | suite 或手工冒烟 + 设备候选确认 + 完整 evidence workflow |
| R13 | 使用这台 TestClaw 设备打开浏览器加载百度，并把返回的内容总结给我 | `testclaw-cli` | 真机浏览器网页巡检流 | 已有设备指定依据 -> evidence preflight -> 打开浏览器/网页 -> 关键截图/日志/网络/性能 -> 结构化报告 -> 释放 |
| R14 | 帮我写一个 React 表单组件 | 不应优先命中 | 非 TestClaw 技能 | 无 |

## 通过标准

- R1-R13 都能稳定命中 `testclaw-cli`
- R3-R13 不再退回“请先配置地址 / 登录 TestClaw”
- R3-R13 优先落到 `testclaw-cli` 命令，而不是 shell/web/Computer Use
- R3-R13 涉及真实设备时，未获得用户指定或确认前只能执行设备查询，不能占用或准备调试
- R10-R13 强制校验证据链：录屏、日志、抓包、截图、性能数据
- R13 必须在打开浏览器或访问网页前完成 evidence preflight；漏采后只能报告证据不完整，不能补录伪装完整报告
- R14 不应被 `testclaw-cli` 抢占

## 建议执行顺序

每次修改 `testclaw-cli` 后，建议至少执行下面 3 步：

1. `python3 testclaw-skills/testclaw-cli/scripts/lint_skill_refs.py`
2. `python3 testclaw-skills/testclaw-cli/scripts/package_skill.py`
3. `python3 testclaw-skills/testclaw-cli/scripts/check_skill_integrity.py`

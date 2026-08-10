# TestClaw Evidence Workflow

所有 TestClaw case、suite、testclaw-cli 手工冒烟、平台执行任务、真机页面巡检、浏览器打开网页、截图取证和 UI 校对都必须遵守本工作流。

## 启动前硬闸门

只要任务会操作或观察真实设备 UI，就必须先完成本闸门；未完成前不得执行安装、打开应用、打开浏览器、访问网页、截图、点击、输入、读取页面内容或总结页面。

在启动被测对象前，必须确认：

1. 已有用户指定设备或明确授权自动选择，并记录 `deviceId`、`udid`、`agentId`、选择依据和抢占风险。
2. 已创建本次 artifacts 目录，目录名包含时间、设备和任务简述。
3. 已启动全程录屏，或已确认平台 suite 会录屏；手工模式下 Android 至少使用 `screenrecord`。
4. 已清空或标记 `logcat` 起点。
5. 已启动网络抓包、MITM/代理日志、pcap 或等价网络请求记录；如果当前平台没有抓包能力，必须在结构化报告中提前写明缺失原因，结论只能是“证据不完整”。
6. 已采集基线截图。
7. 已采集基线性能/环境信息：前台 Activity、进程、内存或明确说明还没有目标包名时如何在启动后补采。

任一项失败时，暂停设备操作并报告阻塞。只有用户明确说“本次不需要证据，只做临时观察”时，才允许继续，但最终必须标注不是完整 TestClaw 验证报告。

## 强制产物

| 产物 | 要求 | 缺失处理 |
| --- | --- | --- |
| 全程录屏 | 从启动被测对象前开始，到最后一个结果稳定后停止，归档 MP4 | 阻塞或证据不完整 |
| 全程日志 | 测试前清空或标记起点，结束后归档完整日志；Android 至少 `logcat` | 阻塞或证据不完整 |
| 全程网络抓包 | 优先平台 MITM/PCAP；至少归档 pcap、代理日志或等价请求记录 | 阻塞或证据不完整 |
| 关键节点截图 | 安装后、启动首屏、每个关键交互后、异常弹窗、最终状态 | 阻塞或证据不完整 |
| 性能数据 | 启动耗时、进程、前台 Activity、内存、gfxinfo；需要时补 CPU/网络/trace | 阻塞或证据不完整 |
| 结构化报告 | 输入、环境、设备、执行依据、步骤、结果、异常、证据路径、限制 | 阻塞或证据不完整 |

## 平台 suite 执行

平台执行 case 时，应由 TestClaw Controller 下发 evidence policy，由 TestClaw Agent 采集并上传：

```json
{
  "recordVideo": true,
  "collectLogs": true,
  "captureNetwork": true,
  "captureScreenshots": true,
  "collectPerformance": true
}
```

套件创建或配置时性能监控必须开启：

```bash
testclaw --json suite create ... --is-open-perfmon 1 --perfmon-interval 1000
```

如果平台 suite 当前只全程录屏，未全程归档日志、抓包或性能数据，执行者必须额外补采；不能补采则报告证据不完整。

## testclaw-cli 手工冒烟模式

手工模式不是降级。没有可用 suite 或用户明确要求手工验证时，仍必须执行完整 evidence workflow。打开浏览器访问网页、读取页面内容、截图确认和页面巡检也属于手工冒烟。

推荐顺序：

1. `testclaw --json doctor`
2. 解析 APK 或目标信息
3. `testclaw --json device list`
4. 列出候选设备，等待用户指定 `deviceId` / `udid` / 设备名称，或明确授权自动选择
5. `testclaw --json device prepare-android-debug --device-id <id>` 或等价指定设备命令
6. 创建本次 artifacts 目录
7. 启动录屏
8. 清空或标记日志起点
9. 启动网络抓包或代理日志采集
10. 采集基线截图和前台 Activity
11. 安装、启动、交互、断言或打开浏览器/网页
12. 每个关键节点截图
13. 采集性能数据
14. 停止录屏、日志、抓包
15. 拉取和归档产物
16. 生成结构化报告
17. 释放设备

Android 最小命令集合：

```bash
adb -s <adbAddress> logcat -c
adb -s <adbAddress> shell screenrecord /sdcard/testclaw-run.mp4
adb -s <adbAddress> shell dumpsys window
adb -s <adbAddress> shell pidof <package>
adb -s <adbAddress> shell dumpsys meminfo <package>
adb -s <adbAddress> shell dumpsys gfxinfo <package>
adb -s <adbAddress> exec-out screencap -p > step.png
adb -s <adbAddress> logcat -d > logcat-full.txt
adb -s <adbAddress> pull /sdcard/testclaw-run.mp4 ./artifacts/
```

在 TestClaw 外部 AI Agent 场景中，不要默认使用运行 CLI 机器的本地 `adb`。上述命令应通过 TestClaw Server -> Agent 的受控命令通道执行，例如：

```bash
testclaw --json raw request --path /agents/<agentId>/command --method POST --body '{"cmd":"adb","args":["-s","<udid>","shell","screenrecord","/sdcard/testclaw-run.mp4"]}'
```

`screenrecord` 是前台阻塞命令，必须用后台执行、平台录屏接口或 Agent 支持的异步采集能力；如果当前 CLI/Agent 只能同步执行导致无法后台录屏，应先报告阻塞或证据不完整，而不是直接跳过录屏继续操作。

网络抓包优先使用平台 MITM/PCAP 能力；没有平台能力时，使用项目可用代理、tcpdump、系统 VPN 代理日志或等价网络请求记录，并在报告中说明采集方式。

## 报告验收

报告必须列出每类产物路径：

- video
- log
- network
- screenshots
- performance
- structured report

任一类别缺失时，报告结论不得写“完整通过”；必须写明缺失项和原因。

如果执行者已经操作真实设备后才发现未提前启动录屏、日志或网络记录，不允许声称“补采完成”。正确处理是：停止继续扩大操作、释放设备、说明本轮证据不完整，并在需要完整报告时重新执行一次完整流程。

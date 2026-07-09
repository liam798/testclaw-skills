# TestClaw Evidence Workflow

所有 TestClaw case、suite、testclaw-cli 手工冒烟和平台执行任务都必须遵守本工作流。

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

手工模式不是降级。没有可用 suite 或用户明确要求手工验证时，仍必须执行完整 evidence workflow。

推荐顺序：

1. `testclaw --json doctor`
2. 解析 APK 或目标信息
3. `testclaw --json device list`
4. `testclaw --json device prepare-android-debug`
5. 启动录屏
6. 清空或标记日志起点
7. 启动网络抓包或代理日志采集
8. 安装、启动、交互、断言
9. 每个关键节点截图
10. 采集性能数据
11. 停止录屏、日志、抓包
12. 拉取和归档产物
13. 释放设备
14. 生成报告

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

---
name: testclaw-cli
description: 通过 testclaw-cli 使用 TestClaw 平台完成设备、应用、测试资产、套件执行、结果查询、真机验证、全量证据采集与报告闭环。
---

# 使用 TestClaw

使用 TestClaw 时，统一走这条主路径：

`AI Agent -> testclaw-cli -> TestClaw Server / TestClaw Agent / 本地 adb`

本 skill 只描述 TestClaw 业务操作、CLI 登录流程和自动化测试证据标准。`testclaw-cli` 指本 skill 与 CLI 执行面；真实可执行命令为 `testclaw`。

## 何时使用

当用户有下面任一目标时使用本 skill：

- 使用 `testclaw login` 打开浏览器完成 OAuth 登录
- 查询 TestClaw 当前登录用户、项目、模块、设备、安装包、测试套件、执行结果
- 查询空闲设备、在线设备、设备状态
- 占用设备、释放设备、准备 Android 调试环境
- 上传安装包、安装应用、打开应用、停止应用、卸载应用
- 创建模块、测试用例、步骤、测试套件
- 自动触发测试套件执行并查询结果
- 使用 TestClaw 真机做 APK/App 冒烟验证、UI 校对、页面巡检、截图取证
- 执行任何 TestClaw case、suite 或 testclaw-cli 手工冒烟任务

如果用户要做的是部署、线上排障、代码与部署比对、服务存活检查，这些属于运维与排障任务，不属于本 skill 的主路径。

## 核心工作流

1. 先判断当前任务属于“登录配置类”还是“业务类”。
2. 如果是登录配置类，先确认 TestClaw Server 地址，再配置 `testclaw-cli` 并指导或执行 `testclaw login`。
3. 如果是业务类，默认直接优先使用 `testclaw-cli` 完成，不要先退回 web、Computer Use 或泛化建议。
4. 业务执行前先观察当前项目、设备、套件状态，避免盲目创建重复资产。
5. 涉及设备时，先占用并准备调试，再做安装包、应用、页面或执行操作。
6. 涉及自动化测试时，所有 case 都必须遵守统一 evidence workflow。
7. 执行套件后，轮询结果直到完成、失败或明确阻塞。
8. 无论成功或失败，结束时都释放设备，或明确说明无法释放的原因。

能力边界：

- 可以自动执行 `testclaw` 命令和读取其输出。
- 可以指导用户完成浏览器 OAuth 登录。
- 不能替用户完成需要浏览器授权确认的登录动作。
- 不要把 TestClaw 业务请求泛化成“测试建议”；能执行时优先真实执行。

## 强制约束

- 先观察，再执行。先查当前项目、设备、套件状态，不要盲目创建重复资产。
- 如果可以复用已有模块、用例、套件，优先复用；只有在用户明确要求新建或需要隔离验证时再创建新的。
- 只要 `testclaw-cli` 已可用，优先使用 `testclaw` 命令，而不是：
  - Computer Use
  - web 搜索替代真机验证
  - 裸 `adb` 脚本
  - 泛化成“给你一份测试建议”
- 涉及设备时，要明确记录 `deviceId`、占用结果、调试地址和最终释放结果。
- 涉及执行结果时，要明确记录 `resultId`、最终状态、失败原因。
- 如果设备处于 `DEBUGGING`、`TESTING`、`ERROR` 等非空闲状态，先判断能否释放，再继续执行。
- `testclaw login` 的浏览器授权默认应对接 TestClaw Server OAuth。
- 所有 TestClaw case、suite、testclaw-cli 手工冒烟和平台执行任务都必须采集完整 evidence workflow：全程录屏、全程日志、全程网络抓包、关键节点截图、性能数据和结构化报告。
- evidence workflow 不允许降级。缺少 MP4、完整日志、pcap/代理日志、关键截图或性能数据中的任一项时，不能交付为“完整自动化测试报告”，必须标注阻塞或证据不完整。

## 业务意图与命令映射

当任务是 TestClaw 业务操作时，优先按下面的意图映射执行。

- 查询当前登录用户
  - 典型表达：`我当前连的是谁`、`TestClaw 登录用户是谁`
  - 优先命令：`testclaw --json whoami`
- 查看项目
  - 典型表达：`列出项目`、`看下 TestClaw 项目`
  - 优先命令：`testclaw --json project list`
- 查看空闲/在线设备
  - 典型表达：`查看空闲设备`、`找台在线 Android`、`列出设备`
  - 优先命令：`testclaw --json device list`
- 占用设备并准备 Android 调试
  - 典型表达：`占用一台设备`、`准备调试`、`拿一个空闲机`
  - 优先命令：`testclaw --json device prepare-android-debug`
- 释放设备
  - 典型表达：`释放设备`、`结束占用`
  - 优先命令：`testclaw --json device release`
- 上传安装包 / 安装应用 / 查看已安装应用
  - 典型表达：`上传 apk`、`安装应用`、`看设备装了什么 app`
  - 优先命令：`testclaw --json package upload`、`testclaw --json app install`、`testclaw --json app list-installed`
- 打开 / 停止 / 卸载应用
  - 典型表达：`打开 app`、`启动应用`、`停止 app`、`卸载 app`
  - 优先命令：`testclaw --json app open`、`testclaw --json app kill`、`testclaw --json app uninstall`
- 创建测试资产
  - 典型表达：`创建模块`、`创建测试用例`、`补步骤`、`建套件`
  - 优先命令：`testclaw --json module create`、`testclaw --json case create`、`testclaw --json step create`、`testclaw --json suite create`
- 执行与结果查询
  - 典型表达：`执行用例`、`跑套件`、`查执行结果`
  - 优先命令：`testclaw --json suite run`、`testclaw --json result get`
- APK/App 自动化测试、冒烟验证、UI 校对
  - 典型表达：`自动化测试这个 APK`、`真机验一下`、`做 UI 校对`
  - 默认流程：先找可复用 suite；没有 suite 时进入 testclaw-cli 手工冒烟模式；两种模式都必须完整采集 evidence workflow。

如果请求里同时出现 “TestClaw + 业务动作”，不要只回答说明，必须优先尝试命令执行。

## 默认执行顺序

登录配置类任务：

1. 读取 `references/flows.md` 的“CLI 登录流程”。
2. 读取 `references/tools.md` 的“配置项与验证点”。
3. 执行或指导 `testclaw config set base_url ...`。
4. 指导用户执行 `testclaw login`。
5. 用 `testclaw --json whoami` 验证登录态。

业务类任务：

1. 确认当前环境是否可直接执行 `testclaw`。
2. 能执行时优先走 `testclaw-cli`。
3. 根据用户意图选择对应命令。
4. 自动化测试类任务必须读取 `references/evidence-workflow.md`。
5. 优先真实执行，不要退化为泛泛说明。
6. 结束后输出结果、证据和资源释放状态。

## 成功判定

以下条件同时满足时，可认为一次 TestClaw 自动化任务闭环完成：

- TestClaw 登录成功，或已明确当前登录用户
- 目标项目、模块、设备、套件或 APK 定位正确
- 如果创建了资产，可以拿到对应的 `id`
- 如果执行了套件，可以拿到 `resultId`
- 结果已明确为成功、失败或人工停止，不处于悬空状态
- 录屏、日志、网络抓包、关键截图、性能数据和结构化报告均已归档
- 设备最终已释放，或明确说明为何不能释放

## 失败处理

优先按下面顺序定位：

1. `testclaw` 是否可执行
2. TestClaw Server 地址是否正确
3. TestClaw 登录是否成功
4. 项目、设备、套件数据是否存在
5. 设备是否可占用
6. Android 调试是否准备完成
7. 应用安装或启动是否失败
8. 套件执行失败是在 TestClaw 编排层还是设备执行层
9. evidence workflow 是否完整；缺任一证据产物时，按证据不完整处理

## 常见误匹配根因

如果发现模型经常没用上 TestClaw，优先检查下面几类问题：

1. 技能描述没有覆盖“设备/应用/执行/UI 校对/证据采集”
2. 用户请求里虽然写了 `TestClaw`，但 skill 仍把任务理解成通用测试建议
3. 没有把用户意图映射到明确的 `testclaw` 命令
4. 可执行 CLI 时仍错误退回 `adb`、web、Computer Use 或纯文本建议
5. 只会解释能力，不会直接执行业务命令
6. 把 evidence workflow 当作可选项或兼容降级项

## 参考资料

- CLI 登录与业务流程：`references/flows.md`
- 配置项、验证点与命令映射：`references/tools.md`
- 自动化测试证据工作流：`references/evidence-workflow.md`
- 通用任务模板：`references/templates.md`
- 触发与回归样例：`references/examples.md`
- 召回验收矩阵：`references/regression-matrix.md`
- skill 引用检查脚本：`scripts/lint_skill_refs.py`
- skill 完整性检查脚本：`scripts/check_skill_integrity.py`
- skill 打包脚本：`scripts/package_skill.py`

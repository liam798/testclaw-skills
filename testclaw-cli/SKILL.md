---
name: testclaw-cli
description: 通过 testclaw-cli 使用 TestClaw 平台完成设备、应用、测试资产、套件执行、结果查询、真机验证、全量证据采集与报告闭环。
---

# 使用 TestClaw

使用 TestClaw 时，统一走这条主路径：

`AI Agent -> testclaw-cli -> TestClaw Server -> TestClaw Agent -> 设备`

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
- 使用真实设备打开浏览器、访问网页、读取页面内容、截图确认或做任何页面观察
- 执行任何 TestClaw case、suite 或 testclaw-cli 手工冒烟任务

如果用户要做的是部署、线上排障、代码与部署比对、服务存活检查，这些属于运维与排障任务，不属于本 skill 的主路径。

## 核心工作流

1. 先判断当前任务属于“登录配置类”还是“业务类”。
2. 先检查当前环境是否可直接执行 `testclaw`；若不可执行，优先进入 CLI 自举安装流程。
3. 如果是登录配置类，先确认 TestClaw Server 地址，再配置 `testclaw-cli` 并指导或执行 `testclaw login`。
4. 如果是业务类，默认直接优先使用 `testclaw-cli` 完成，不要先退回 web、Computer Use 或泛化建议。
5. 业务执行前先观察当前项目、设备、套件状态，避免盲目创建重复资产。
6. 涉及设备时，先列出候选设备；除非用户已明确指定设备或确认自动选择，否则不得占用、准备调试或执行应用操作。
7. 涉及任何真实设备操作时，先读取并执行 `references/evidence-workflow.md`；证据采集启动完成前，不得打开应用、打开浏览器、访问网页、截图、点击、输入或读取页面内容。
8. 涉及自动化测试时，所有 case 都必须遵守统一 evidence workflow。
9. 执行套件后，轮询结果直到完成、失败或明确阻塞。
10. 无论成功或失败，结束时都先停止并归档证据，再释放设备，或明确说明无法释放的原因。

能力边界：

- 可以自动执行 `testclaw` 命令和读取其输出。
- 在当前 Agent 允许运行 shell、联网并安装 Node 包时，可以自动补装 `testclaw-cli`。
- 可以指导用户完成浏览器 OAuth 登录。
- 不能替用户完成需要浏览器授权确认的登录动作。
- 不要把 TestClaw 业务请求泛化成“测试建议”；能执行时优先真实执行。

## 强制约束

- 先观察，再执行。先查当前项目、设备、套件状态，不要盲目创建重复资产。
- 命中本 skill 后，第一步先检查 `testclaw` 是否可执行：
  - 可执行时，优先先执行 `testclaw bootstrap --base-url https://testclaw.vvicat.dev`，再继续后续业务流。
  - 不可执行且当前环境允许 shell + 网络安装时，优先自动执行 `npm install -g git+https://github.com/liam798/testclaw-cli.git`。
  - 安装成功后，立即执行 `testclaw bootstrap --base-url https://testclaw.vvicat.dev`。
  - 如果环境不允许安装、缺少 `npm`、缺少网络权限或安装失败，再告诉用户缺什么，不要假装 CLI 已可用。
- 设备业务操作必须通过 `testclaw-cli -> TestClaw Server -> TestClaw Agent`，不要让外部用户的 AI Agent 直接连接本机手机。
- 设备选择与占用保护：
  - 任何需要真实设备的任务，都必须先执行 `testclaw --json device list`，并把可用候选设备列给用户。
  - 如果用户没有明确指定 `deviceId`、`udid` 或设备名称，不得执行 `device prepare-android-debug`、`device occupy`、安装、打开、停止、卸载、套件运行、UI 校对、截图、录屏等会接触真实设备的操作。
  - 用户说“随便找一台”“拿一个空闲机”“找台在线 Android”时，也只先列出候选设备并请求用户指定；只有用户明确授权“自动选择并占用”时，才可以从候选空闲设备中选择。
  - 优先展示空闲、在线、未占用设备；`DEBUGGING`、`TESTING`、`ERROR`、维护中、离线、已占用、线下使用中的设备不能自动抢占。
  - 如果设备状态缺少占用人、用途、锁定时间或线下使用信息，必须提示存在抢占风险，并等待用户确认后再继续。
- `--adb-address` 只允许用于明确的本地动态分析/调试场景；查看应用、打开应用、停止应用、卸载应用等业务命令优先使用 `--device-id` 或 `--udid`。
- 如果可以复用已有模块、用例、套件，优先复用；只有在用户明确要求新建或需要隔离验证时再创建新的。
- 只要 `testclaw-cli` 已可用，优先使用 `testclaw` 命令，而不是：
  - Computer Use
  - web 搜索替代真机验证
  - 裸 `adb` 脚本
  - 泛化成“给你一份测试建议”
- 涉及设备时，要明确记录候选设备列表、用户指定或授权依据、`deviceId`、占用结果、调试地址和最终释放结果。
- 涉及执行结果时，要明确记录 `resultId`、最终状态、失败原因。
- 如果设备处于 `DEBUGGING`、`TESTING`、`ERROR` 等非空闲状态，先判断能否释放，再继续执行。
- `testclaw login` 的浏览器授权默认应对接 TestClaw Server OAuth。
- 证据采集硬闸门：
  - 所有 TestClaw case、suite、testclaw-cli 手工冒烟、平台执行任务、真机页面巡检、浏览器打开网页、截图取证和 UI 校对，都必须采集完整 evidence workflow：全程录屏、全程日志、全程网络抓包、关键节点截图、性能数据和结构化报告。
  - 用户说“打开网页看看”“加载某个页面并总结”“截个图确认”“简单看一下设备页面”也属于真实设备手工冒烟；只要会接触设备 UI，就必须先启动 evidence workflow。
  - 在执行任何会改变或观察设备 UI 的命令前，必须先完成 evidence preflight：创建本次 artifacts 目录、启动录屏、清空或标记 logcat 起点、启动网络抓包或写明可用网络记录方式、采集基线截图、采集基线前台 Activity/性能信息。
  - evidence preflight 任一项失败时，必须暂停设备操作并报告阻塞；除非用户明确说“本次不需要证据，只做临时观察”，否则不得继续。
  - evidence workflow 不允许事后补录。漏启动录屏、日志或网络记录后，不能把后续截图包装成完整验证；必须标注“证据不完整”，并建议重跑。
  - 最终回复必须列出 `video`、`log`、`network`、`screenshots`、`performance`、`structured report` 六类证据路径或缺失原因。

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
  - 优先命令：先执行 `testclaw --json device list`；用户指定设备或明确授权自动选择后，才执行 `testclaw --json device prepare-android-debug --device-id <id>` 或等价指定设备命令。
- 释放设备
  - 典型表达：`释放设备`、`结束占用`
  - 优先命令：`testclaw --json device release`
- 上传安装包 / 安装应用 / 查看已安装应用
  - 典型表达：`上传 apk`、`安装应用`、`看设备装了什么 app`
  - 优先命令：`testclaw --json package upload`、`testclaw --json app list-installed --device-id <id>`
- 打开 / 停止 / 卸载应用
  - 典型表达：`打开 app`、`启动应用`、`停止 app`、`卸载 app`
  - 优先命令：`testclaw --json app open --device-id <id>`、`testclaw --json app kill --device-id <id>`、`testclaw --json app uninstall --device-id <id>`
- 创建测试资产
  - 典型表达：`创建模块`、`创建测试用例`、`补步骤`、`建套件`
  - 优先命令：`testclaw --json module create`、`testclaw --json case create`、`testclaw --json step create`、`testclaw --json suite create`
- 执行与结果查询
  - 典型表达：`执行用例`、`跑套件`、`查执行结果`
  - 优先命令：`testclaw --json suite run`、`testclaw --json result get`
- APK/App 自动化测试、冒烟验证、UI 校对
  - 典型表达：`自动化测试这个 APK`、`真机验一下`、`做 UI 校对`、`打开浏览器加载网页并总结`
  - 默认流程：先找可复用 suite；没有 suite 时进入 testclaw-cli 手工冒烟模式；两种模式都必须完整采集 evidence workflow。

如果请求里同时出现 “TestClaw + 业务动作”，不要只回答说明，必须优先尝试命令执行。

## 默认执行顺序

登录配置类任务：

1. 先检查当前环境是否可执行 `testclaw`。
2. 不可执行时，优先尝试自动安装 `testclaw-cli`；安装失败时再报告阻塞原因。
3. CLI 可用后优先执行 `testclaw bootstrap --base-url https://testclaw.vvicat.dev`。
4. 读取 `references/flows.md` 的“CLI 登录流程”。
5. 读取 `references/tools.md` 的“配置项与验证点”。
6. 指导用户执行 `testclaw login`。
7. 用 `testclaw --json whoami` 验证登录态。

业务类任务：

1. 确认当前环境是否可直接执行 `testclaw`。
2. 不可执行且环境允许时，先自动安装 `testclaw-cli`，再进入业务流程。
3. 能执行时优先先执行 `testclaw bootstrap --base-url https://testclaw.vvicat.dev`，再走 `testclaw-cli` 业务命令。
4. 根据用户意图选择对应命令；涉及真实设备时先列候选并等待用户指定或确认。
5. 只要后续会操作或观察真实设备 UI，必须读取 `references/evidence-workflow.md`，并在启动被测对象前完成 evidence preflight。
6. evidence preflight 完成后再优先真实执行，不要退化为泛泛说明。
7. 结束后先停止/拉取/归档证据，再释放设备。
8. 输出结果、六类证据路径或缺失原因、资源释放状态。

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
2. 如果不可执行，当前环境是否允许自动安装 CLI，`npm` 和网络是否可用
3. TestClaw Server 地址是否正确
4. TestClaw 登录是否成功
5. 项目、设备、套件数据是否存在
6. 设备是否可占用
7. Android 调试是否准备完成
8. 应用安装或启动是否失败
9. 套件执行失败是在 TestClaw 编排层还是设备执行层
10. evidence workflow 是否完整；缺任一证据产物时，按证据不完整处理
11. 如果已经操作了真实设备但没有提前启动录屏、日志或网络记录，应立即停止继续扩大操作，说明本轮证据不完整，并请求重跑以重新采集完整证据。

## 常见误匹配根因

如果发现模型经常没用上 TestClaw，优先检查下面几类问题：

1. 技能描述没有覆盖“设备/应用/执行/UI 校对/证据采集”
2. 用户请求里虽然写了 `TestClaw`，但 skill 仍把任务理解成通用测试建议
3. 没有把用户意图映射到明确的 `testclaw` 命令
4. 可执行 CLI 时仍错误退回 `adb`、web、Computer Use 或纯文本建议
5. 只会解释能力，不会直接执行业务命令
6. 把 evidence workflow 当作可选项或兼容降级项
7. 把“打开浏览器/网页、截图确认、页面内容总结”误判为轻量查询，导致绕过手工冒烟 evidence preflight

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

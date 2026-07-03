# ReadOutLoud 上架 Mac App Store 指南

## 结论

可以尝试上架，而且这个项目不是明显不合规的类型。

但它不是“现在直接上传就能过审”的状态。最重要的前提有 4 个：

1. App 必须用 **App Sandbox** 构建并签名。
2. App Store Connect 里必须补齐 **隐私政策 URL**、**支持 URL**、版本信息、截图和描述。
3. 你必须如实披露：**输入文本会发送到 Microsoft Edge TTS 在线服务** 才能生成音频。
4. 你需要用自己的 Apple Developer 账号、证书和 provisioning profile 完成最终签名与上传。

## 我已经帮你补好的内容

1. `AudioGenerator.py`
   - 增加了 App 内可见的“隐私政策”和“联系支持”入口。
   - 把默认输出目录改成了更适合沙盒环境的路径策略。
2. `ReadOutLoud.spec`
   - 增加了版本号、构建号、最小系统版本、App 分类等 Info.plist 配置入口。
   - 增加了通过环境变量传入签名身份和 entitlements 的能力。
3. `appstore/ReadOutLoud-AppStore.entitlements`
   - 预设了当前这个 App 最可能需要的沙盒权限：
     - `app-sandbox`
     - `network.client`
     - `files.user-selected.read-write`
4. `landing-page/privacy-policy.html`
   - 可作为 App Store Connect 的隐私政策 URL 页面基础稿。
5. `landing-page/support.html`
   - 可作为 App Store Connect 的支持 URL 页面基础稿。
6. `appstore/metadata-template.md`
   - 给你准备了 App Store Connect 文案草稿。
7. `appstore/review-notes-template.md`
   - 给你准备了审核备注草稿。

## 当前最大的审核风险

### 1. 在线 TTS 依赖

ReadOutLoud 不是纯离线 App。它需要联网把输入文本发送给 Microsoft Edge TTS 服务生成音频。

这不必然违规，但你必须：

1. 在审核备注里明确说明为什么需要联网。
2. 在隐私政策里写清楚文本会被发送到第三方语音服务。
3. 在 App Privacy 问卷里认真判断这是否构成需要披露的数据传输或第三方处理。

这一步我不能替你做最终法律判断，但我已经把需要披露的事实写进了文案草稿。

### 2. 当前构建是 Apple Silicon only

你现在的本地二进制是 `arm64`。如果你继续保持 Apple Silicon only，上架前要确认：

1. 你接受只支持 Apple Silicon Mac。
2. 你的最小系统版本设置与 Apple 当前要求一致。

目前我在 spec 里默认给了 `12.0`，因为这更接近 Apple Silicon-only 的安全起点，但最终仍建议你在提交前再确认一次。

## 明天你要做的实际步骤

### A. 先把网页链接部署出来

把下面两个页面发布成公网 URL：

1. `landing-page/privacy-policy.html`
2. `landing-page/support.html`

如果你用 GitHub Pages，部署后通常会得到类似：

- `https://<your-name>.github.io/ReadOutLoud/privacy-policy.html`
- `https://<your-name>.github.io/ReadOutLoud/support.html`

这两个 URL 稍后要填进 App Store Connect。

### B. 准备 Apple Developer 账号材料

你需要确认自己已经有：

1. Apple Developer Program 会员资格
2. App Store Connect 权限
3. 用于 Mac App Store 的证书
4. 对应 App ID：`com.socranotes.readoutloud`
5. 对应的 App Store provisioning profile

### C. 在 Apple Developer 后台启用能力

为 `com.socranotes.readoutloud` 这个 App ID 检查并启用：

1. App Sandbox
2. Outgoing Network Connections

当前这个 App 的设计下，通常不需要额外的文件夹白名单，因为它主要依赖用户自己通过文件选择器来授权访问。

### D. 用 App Store 配置重新构建

在项目目录运行前，先设置这些环境变量：

```bash
export READOUTLOUD_VERSION="1.0.0"
export READOUTLOUD_BUILD="1"
export READOUTLOUD_MIN_MACOS="12.0"
export READOUTLOUD_CODESIGN_IDENTITY="Apple Distribution: Your Name (TEAMID)"
export READOUTLOUD_ENTITLEMENTS_FILE="$PWD/appstore/ReadOutLoud-AppStore.entitlements"
```

然后构建：

```bash
python3 -m PyInstaller ReadOutLoud.spec --noconfirm
```

### E. 手动检查产物

至少检查这几项：

1. App 能打开
2. 能输入文本并生成音频
3. 能导入 `.txt`
4. 能选择保存目录
5. “隐私政策”和“联系支持”入口能正常打开
6. 日语与中文界面都没有布局问题
7. 在网络断开时，错误提示是可理解的

### F. 在 App Store Connect 创建 App

建议填写：

1. App Name: `ReadOutLoud`
2. Primary Language: 你准备主推的语言
3. Bundle ID: `com.socranotes.readoutloud`
4. SKU: 自己定义，比如 `readoutloud-mac-001`

### G. 填元数据

参考：

1. `appstore/metadata-template.md`
2. `appstore/review-notes-template.md`

你还需要上传：

1. App 图标
2. macOS 截图
3. App 描述
4. 隐私政策 URL
5. 支持 URL

### H. 上传构建

可用方式通常是：

1. Xcode Organizer
2. Transporter
3. `xcrun altool`

如果你想走最稳的路线，优先用 Xcode Organizer 或 Transporter。

### I. 填 App Privacy 与审核问卷

这里一定要基于真实行为填写。特别注意：

1. 用户输入的文本会被发送到 Microsoft Edge TTS 服务。
2. App 本身没有登录、广告或自建分析。
3. 你需要根据 Apple 的问卷定义判断这是否属于需要披露的数据类别。

### J. 提交审核

提交前再检查一次：

1. 所有链接都能访问
2. App 内支持与隐私入口都可打开
3. 审核备注里已经解释联网用途
4. 如果审核设备无法访问 Edge TTS，审核员是否仍能理解 App 的核心流程

## 我对“能不能上”的真实判断

### 从技术角度

可以。

Tkinter + PyInstaller 不会自动让你失去上架资格，真正决定成败的是：

1. 沙盒是否正确
2. 签名是否正确
3. 隐私披露是否真实
4. 链接和元数据是否完整

### 从审核风险角度

中等风险，不是高风险。

最容易被问到的点不是 UI，而是：

1. 为什么必须联网
2. 文本是否发送到第三方
3. 隐私政策是否写清楚

如果这三点说清楚，过审概率会明显高很多。

## 你明天醒来后最先做什么

按顺序做这 5 件事就行：

1. 把 `landing-page/privacy-policy.html` 和 `landing-page/support.html` 部署成公开 URL。
2. 在 Apple Developer 后台确认 `com.socranotes.readoutloud` 的 App Sandbox 能力。
3. 创建 App Store provisioning profile。
4. 用自己的 Apple 证书跑一次 App Store 构建。
5. 用 `appstore/metadata-template.md` 和 `appstore/review-notes-template.md` 填 App Store Connect。

如果你明天回来要继续，我建议我下一步直接帮你做：

1. 把隐私页和支持页接进现有 landing page 导航
2. 帮你整理 App Store Connect 文案成中英日三套
3. 帮你继续处理签名、上传和审核备注

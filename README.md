# ReadOutLoud

把任何英文单词、句子或段落，快速变成标准、自然的英语朗读音频。

ReadOutLoud 是一个基于 `Python + Tkinter + edge-tts` 的 macOS 桌面小工具，适合英语老师批量生成词汇朗读材料，也适合学习者自己做跟读和磨耳朵音频。

![ReadOutLoud 海报](landing-page/assets/hero-poster.png)

## 亮点

- 支持把多行英文批量生成为音频
- 支持美音、英音、男声、女声多种组合
- 支持自定义语速
- 支持逐句生成，或合并成一个音频
- 内置我最常用的“强推设置”

## 强推设置

点击“用我的强推设置生成”后，工具会把每一个单词或句子连续读三遍：

- 第 1 遍：`Aria`，`-20%`
- 第 2 遍：`Guy`，`-30%`
- 第 3 遍：`Jenny`，`-10%`

每遍之间会停顿 `0.5` 秒，每句之间会停顿 `1` 秒，方便学习者回想、复述或跟读。

## 系统要求

- macOS
- Apple Silicon 芯片：`M1 / M2 / M3 / M4`
- 需要联网

## 从源码运行

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 AudioGenerator.py
```

## 打包本地 App

```bash
pip install pyinstaller
pyinstaller ReadOutLoud.spec
```

打包完成后，可在 `dist/` 下找到 `ReadOutLoud.app` 或相关产物。

## 第一次打开 App

如果系统提示“无法验证开发者”，请按下面方式打开一次：

1. 右键点击 `ReadOutLoud.app`
2. 选择“打开”
3. 在弹窗里再点一次“打开”

之后就可以正常双击使用。

## GitHub Pages

仓库内已包含独立的静态介绍页，位于 [`landing-page/`](landing-page/README.md)。

推送到 GitHub 后，启用 Pages 并让 GitHub Actions 运行一次，页面就会自动发布。工作流文件在 [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml)。

## 联系方式

- 邮箱：`socranote@gmail.com`
- 微信：`yxkenglish`

## 说明

这个项目当前主要整理为“源码仓库 + GitHub Pages 展示页”的发布形态。仓库里没有提交本地构建产物、历史废稿和大体积临时素材；如需给别人下载 App，推荐把打包好的 zip 作为 GitHub Release 附件上传。

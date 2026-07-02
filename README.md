# ReadOutLoud

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/macOS-Apple%20Silicon-000000?logo=apple&logoColor=white)](https://www.apple.com/mac/)
[![edge-tts](https://img.shields.io/badge/TTS-edge--tts-0078D4?logo=microsoft&logoColor=white)](https://github.com/rany2/edge-tts)
[![License](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)

把任何英文单词、句子或段落，快速变成标准、自然的英语朗读音频。

ReadOutLoud 是一个基于 `Python + Tkinter + edge-tts` 的 macOS 桌面工具，适合英语老师批量生成词汇朗读材料，也适合学习者自己制作跟读和磨耳朵音频。

![ReadOutLoud 海报](landing-page/assets/hero-poster-v2.png)

---

## 目录

- [功能亮点](#功能亮点)
- [强推设置](#强推设置)
- [系统要求](#系统要求)
- [安装与运行](#安装与运行)
- [第一次打开 App](#第一次打开-app)
- [GitHub Pages](#github-pages)
- [联系方式](#联系方式)

---

## 功能亮点

- 多行英文**批量**生成音频，一键完成
- 支持**美音、英音、男声、女声**多种组合
- 可自定义**语速**（百分比调节）
- 支持**逐句生成**或**合并为单个文件**
- 内置「强推设置」——三遍重复 + 自动停顿，专为跟读训练设计

---

## 强推设置

点击「用我的强推设置生成」后，每个单词或句子会连续朗读三遍：

| 轮次 | 音色 | 语速 |
|:----:|------|:----:|
| 第 1 遍 | Aria（美式女声） | −20% |
| 第 2 遍 | Guy（美式男声） | −30% |
| 第 3 遍 | Jenny（美式女声） | −10% |

- 每遍之间停顿 **0.5 秒**，方便回想
- 句与句之间停顿 **1 秒**，方便跟读或复述

---

## 系统要求

| 项目 | 要求 |
|------|------|
| 操作系统 | macOS |
| 芯片 | Apple Silicon（M1 / M2 / M3 / M4） |
| 网络 | 需要联网（edge-tts 在线调用） |
| Python | 3.9+（从源码运行时） |

---

## 安装与运行

### 方式一：从源码运行

```bash
git clone https://github.com/GadflyRun/ReadOutLoud.git
cd ReadOutLoud

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 AudioGenerator.py
```

### 方式二：自行打包为本地 App

```bash
pip install pyinstaller
pyinstaller ReadOutLoud.spec
```

打包完成后，在 `dist/` 目录下找到 `ReadOutLoud.app`。

> 如需分发给他人，推荐将打包好的 `.zip` 作为 [GitHub Release](https://github.com/GadflyRun/ReadOutLoud/releases) 附件上传。

---

## 第一次打开 App

如果系统提示「无法验证开发者」，按以下步骤操作一次：

1. **右键点击** `ReadOutLoud.app`
2. 选择「**打开**」
3. 在弹窗中再点一次「**打开**」

之后即可正常双击使用。

---

## GitHub Pages

仓库内含独立静态介绍页，位于 [`landing-page/`](landing-page/README.md)。

推送到 GitHub 后，启用 Pages，GitHub Actions 会自动完成部署。工作流配置见 [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml)。

---

## 联系方式

有问题或建议，欢迎通过以下方式联系：

- 邮箱：`socranote@gmail.com`
- 微信：`yxkenglish`

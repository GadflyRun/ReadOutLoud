# ReadOutLoud

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/macOS-Apple%20Silicon-000000?logo=apple&logoColor=white)](https://www.apple.com/mac/)
[![edge-tts](https://img.shields.io/badge/TTS-edge--tts-0078D4?logo=microsoft&logoColor=white)](https://github.com/rany2/edge-tts)
[![License](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)

[中文](#中文) · [English](#english)

---

<a name="中文"></a>

## 中文

把任何英文单词、句子或段落，快速变成标准、自然的英语朗读音频。

ReadOutLoud 是一个基于 `Python + Tkinter + edge-tts` 的 macOS 桌面工具，适合英语老师批量生成词汇朗读材料，也适合学习者自己制作跟读和磨耳朵音频。

![ReadOutLoud 海报](landing-page/assets/hero-poster-v2.png)

### 功能亮点

- 多行英文**批量**生成音频，一键完成
- 支持**美音、英音、男声、女声**多种组合
- 可自定义**语速**（百分比调节）
- 支持**逐句生成**或**合并为单个文件**
- 内置「强推设置」——三遍重复 + 自动停顿，专为跟读训练设计

### 强推设置

点击「用我的强推设置生成」后，每个单词或句子会连续朗读三遍：

| 轮次 | 音色 | 语速 |
|:----:|------|:----:|
| 第 1 遍 | Aria（美式女声） | −20% |
| 第 2 遍 | Guy（美式男声） | −30% |
| 第 3 遍 | Jenny（美式女声） | −10% |

- 每遍之间停顿 **0.5 秒**，方便回想
- 句与句之间停顿 **1 秒**，方便跟读或复述

### 系统要求

| 项目 | 要求 |
|------|------|
| 操作系统 | macOS |
| 芯片 | Apple Silicon（M1 / M2 / M3 / M4） |
| 网络 | 需要联网（edge-tts 在线调用） |
| Python | 3.9+（从源码运行时） |

### 安装与运行

**方式一：直接下载**

前往 [Releases](https://github.com/GadflyRun/ReadOutLoud/releases) 下载最新 `ReadOutLoud.zip`，解压后将 App 拖入「应用程序」文件夹。

**方式二：从源码运行**

```bash
git clone https://github.com/GadflyRun/ReadOutLoud.git
cd ReadOutLoud
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 AudioGenerator.py
```

**方式三：自行打包**

```bash
pip install pyinstaller
pyinstaller ReadOutLoud.spec
```

### 第一次打开 App

如果系统提示「无法验证开发者」：

1. **右键点击** `ReadOutLoud.app`
2. 选择「**打开**」
3. 在弹窗中再点一次「**打开**」

之后即可正常双击使用。

### 联系方式

- 邮箱：`socranote@gmail.com`
- 微信：`yxkenglish`

---

<a name="english"></a>

## English

Convert any English words, sentences, or paragraphs into natural-sounding audio — fast.

ReadOutLoud is a macOS desktop app built with `Python + Tkinter + edge-tts`. It's designed for English teachers who need to batch-generate vocabulary audio, and for learners who want to create their own shadowing or listening practice files.

### Features

- **Batch processing** — convert multiple lines of text into audio in one click
- **Multiple voices** — American / British English, male / female options
- **Adjustable speed** — fine-tune playback rate with percentage controls
- **Flexible output** — generate one file per sentence or merge everything into a single audio file
- **Shadowing Mode** — reads each item three times with different voices and built-in pauses, designed for repeat-and-shadow practice

### Shadowing Mode

Click "Generate with Recommended Settings" and each word or sentence is read three times:

| Round | Voice | Speed |
|:-----:|-------|:-----:|
| 1st | Aria (American female) | −20% |
| 2nd | Guy (American male) | −30% |
| 3rd | Jenny (American female) | −10% |

- **0.5 s** pause between each round — time to recall
- **1 s** pause between sentences — time to shadow or repeat

### System Requirements

| | Requirement |
|---|---|
| OS | macOS |
| Chip | Apple Silicon (M1 / M2 / M3 / M4) |
| Network | Required (edge-tts is cloud-based) |
| Python | 3.9+ (source-code mode only) |

### Installation

**Option 1 — Download (recommended)**

Go to [Releases](https://github.com/GadflyRun/ReadOutLoud/releases), download `ReadOutLoud.zip`, unzip it, and drag the app into your Applications folder.

**Option 2 — Run from source**

```bash
git clone https://github.com/GadflyRun/ReadOutLoud.git
cd ReadOutLoud
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 AudioGenerator.py
```

**Option 3 — Build your own .app**

```bash
pip install pyinstaller
pyinstaller ReadOutLoud.spec
```

### First Launch

If macOS shows "cannot verify the developer":

1. **Right-click** `ReadOutLoud.app`
2. Choose **Open**
3. Click **Open** again in the dialog

After that, you can double-click it normally.

### Contact

- Email: `socranote@gmail.com`
- WeChat: `yxkenglish`

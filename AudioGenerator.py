#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ReadOutLoud desktop app.
Based on edge-tts. Install once before first run: pip install edge-tts
"""

import asyncio
import base64
import locale
import os
import re
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    import edge_tts
except ImportError:
    raise SystemExit("请先安装 / 先にインストールしてください: pip install edge-tts")

APP_NAME = "ReadOutLoud"
APP_BUNDLE_ID = "com.socranotes.readoutloud"
SUPPORT_EMAIL = "socranote@gmail.com"
SUPPORT_WECHAT = "yxkenglish"


# ===================== 主题 =====================
THEME = {
    "accent": "#E8E8ED",
    "accent_hover": "#DDDDE3",
    "bg": "#F5F5F7",
    "btn_border": "#D2D2D7",
    "btn_disabled_bg": "#E8E8ED",
    "btn_disabled_fg": "#AEAEB2",
    "btn_font": ("Helvetica Neue", 13),
    "btn_small": ("Helvetica Neue", 11),
    "btn_h": 44,
    "card_bg": "#FFFFFF",
    "field_bg": "#FFFFFF",
    "field_border": "#D2D2D7",
    "field_bw": 1,
    "ghost_bg": "#FFFFFF",
    "ghost_fg": "#007AFF",
    "ghost_hover": "#F0F0F2",
    "link_fg": "#0066CC",
    "muted_fg": "#86868B",
    "on_accent": "#007AFF",
    "on_primary": "#FFFFFF",
    "pad": 24,
    "primary": "#007AFF",
    "primary_hover": "#0A6FE0",
    "radius": 12,
    "small_font": ("Helvetica Neue", 11),
    "tiny_font": ("Helvetica Neue", 10),
    "credit_font": ("Helvetica Neue", 11, "bold"),
    "hint_font": ("Helvetica Neue", 10),
    "text_fg": "#1D1D1F",
    "text_font": ("Helvetica Neue", 12),
    "area_font": ("Helvetica Neue", 10),
    "title_fg": "#1D1D1F",
    "title_font": ("Helvetica Neue", 20, "bold"),
    "title_en_font": ("Helvetica Neue", 14, "bold"),
}
# ================================================


VOICE_OPTIONS = [
    {
        "id": "en-US-AriaNeural",
        "labels": {
            "zh": "美音女声 Aria",
            "ja": "アメリカ英語 女性 Aria",
        },
    },
    {
        "id": "en-US-JennyNeural",
        "labels": {
            "zh": "美音女声 Jenny",
            "ja": "アメリカ英語 女性 Jenny",
        },
    },
    {
        "id": "en-US-GuyNeural",
        "labels": {
            "zh": "美音男声 Guy",
            "ja": "アメリカ英語 男性 Guy",
        },
    },
    {
        "id": "en-GB-SoniaNeural",
        "labels": {
            "zh": "英音女声 Sonia",
            "ja": "イギリス英語 女性 Sonia",
        },
    },
    {
        "id": "en-GB-RyanNeural",
        "labels": {
            "zh": "英音男声 Ryan",
            "ja": "イギリス英語 男性 Ryan",
        },
    },
]

VOICE_BY_ID = {voice["id"]: voice for voice in VOICE_OPTIONS}

LANGUAGE_OPTIONS = [
    ("auto", {"zh": "跟随系统", "ja": "システムに合わせる"}),
    ("zh", {"zh": "中文", "ja": "中国語"}),
    ("ja", {"zh": "日文", "ja": "日本語"}),
]

RATE_OPTIONS = ["-30%", "-20%", "-10%", "+0%", "+10%", "+20%"]

REPEAT_SEQUENCE = [
    ("en-US-AriaNeural", "-20%"),
    ("en-US-GuyNeural", "-30%"),
    ("en-US-JennyNeural", "-10%"),
]

TEXTS = {
    "zh": {
        "app_title": "ReadOutLoud - 朗读音频生成器",
        "title_main": "ReadOutLoud",
        "title_sub": " 一款朗读音频生成器",
        "credit": "由 Socranotes 设计，与 Claude Code 协作开发",
        "input_hint": "输入英文文本，每行一句或一个单词",
        "language_label": "界面语言",
        "voice_label": "语音",
        "rate_label": "语速",
        "merge_audio": "合并成一个音频",
        "output_to": "输出到",
        "filename": "文件名",
        "import_txt": "导入 txt…",
        "clear": "清空",
        "choose": "选择…",
        "generate": "按上方设置生成",
        "strong_generate": "用我的强推设置生成",
        "strong_desc": (
            "强推设置：每个单词/句子连读 3 遍，依次为 Aria 慢速(-20%) → "
            "Guy 更慢(-30%) → Jenny 稍慢(-10%)；每遍之间停顿 0.5 秒，"
            "每句之间停顿 1 秒。"
        ),
        "status_ready": "就绪",
        "status_generating_three": "正在生成 {current}/{total} 句（每句三遍）…",
        "status_generating_merged": "正在生成合并音频…",
        "status_generating_single": "正在生成 {current}/{total} …",
        "status_done_file": "完成！已保存到 {path}",
        "status_done_dir": "完成！已保存到 {path}",
        "status_error": "出错",
        "warn_title": "提示",
        "done_title": "完成",
        "error_title": "错误",
        "no_text_warning": "请先输入文本",
        "done_three_message": (
            "已生成一个音频，每句按 Aria → Guy → Jenny 读三遍：\n\n{path}"
        ),
        "done_dir_message": "音频已保存到：\n{path}",
        "filetype_text": "文本文件",
        "filetype_all": "所有文件",
        "default_filename": "tts_output 01",
        "support_link": "联系支持",
        "privacy_link": "隐私政策",
        "close": "关闭",
        "support_title": "联系支持",
        "support_body": (
            "如需帮助，请联系：\n\n"
            f"邮箱：{SUPPORT_EMAIL}\n"
            f"微信：{SUPPORT_WECHAT}\n\n"
            "支持说明：\n"
            "1. 这是一个联网生成英语朗读音频的 macOS 工具。\n"
            "2. 如果你遇到无法生成、打包、语言显示或导出问题，请把问题描述和截图一起发来。\n"
            "3. 如果你希望按自己的教学或学习场景定制功能，也可以直接来信。"
        ),
        "privacy_title": "隐私政策",
        "privacy_body": (
            "ReadOutLoud 隐私说明\n\n"
            "1. 为生成音频，App 会将你输入的文本发送给 Microsoft Edge TTS 在线语音服务。\n"
            "2. App 本身不要求注册账号，不内置广告，也不主动收集姓名、电话、邮箱或其他身份信息。\n"
            "3. 你通过“导入 txt”选择的文件仅在本地读取；你通过“输出到”选择的目录仅用于本地保存生成的 mp3。\n"
            "4. 如果你主动发送邮件联系支持，邮件内容会由你的邮件服务商和收件服务商处理。\n"
            "5. 如需删除本地生成的音频文件，请直接在你的 Mac 上删除相关文件。"
        ),
        "exit_prompt": "出错了，按回车关闭…",
    },
    "ja": {
        "app_title": "ReadOutLoud - 読み上げ音声ジェネレーター",
        "title_main": "読み上げ音声ジェネレーター",
        "title_sub": " ReadOutLoud",
        "credit": "Socranotes が設計し、Claude Code と協力して開発",
        "input_hint": "英語テキストを入力してください。1行に1単語または1文。",
        "language_label": "表示言語",
        "voice_label": "音声",
        "rate_label": "速度",
        "merge_audio": "1つの音声に結合",
        "output_to": "保存先",
        "filename": "ファイル名",
        "import_txt": "txt を読み込む…",
        "clear": "クリア",
        "choose": "選択…",
        "generate": "この設定で生成",
        "strong_generate": "おすすめ設定で生成",
        "strong_desc": (
            "おすすめ設定：各単語・文を 3 回連続で読み上げます。"
            "Aria ゆっくり(-20%) → Guy さらにゆっくり(-30%) → "
            "Jenny ややゆっくり(-10%)。各回の間に 0.5 秒、"
            "文ごとに 1 秒の間隔が入ります。"
        ),
        "status_ready": "準備完了",
        "status_generating_three": "{current}/{total} を生成中（各行 3 回読み上げ）…",
        "status_generating_merged": "結合音声を生成中…",
        "status_generating_single": "{current}/{total} を生成中…",
        "status_done_file": "完了しました。保存先: {path}",
        "status_done_dir": "完了しました。保存先: {path}",
        "status_error": "エラー",
        "warn_title": "お知らせ",
        "done_title": "完了",
        "error_title": "エラー",
        "no_text_warning": "先にテキストを入力してください",
        "done_three_message": (
            "1つの音声ファイルを生成しました。各行は Aria → Guy → Jenny の順で "
            "3 回読み上げます。\n\n{path}"
        ),
        "done_dir_message": "音声を保存しました:\n{path}",
        "filetype_text": "テキストファイル",
        "filetype_all": "すべてのファイル",
        "default_filename": "tts_output 01",
        "support_link": "サポート",
        "privacy_link": "プライバシー",
        "close": "閉じる",
        "support_title": "サポート",
        "support_body": (
            "お問い合わせ先\n\n"
            f"メール：{SUPPORT_EMAIL}\n"
            f"WeChat：{SUPPORT_WECHAT}\n\n"
            "サポート案内：\n"
            "1. この App はインターネット経由で英語音声を生成する macOS ツールです。\n"
            "2. 生成できない、パッケージ化できない、表示言語が不自然、書き出しに失敗するなどの問題があれば、状況説明とスクリーンショットを送ってください。\n"
            "3. 授業用・学習用に合わせた機能調整の相談も歓迎します。"
        ),
        "privacy_title": "プライバシーポリシー",
        "privacy_body": (
            "ReadOutLoud のプライバシーについて\n\n"
            "1. 音声生成のため、入力したテキストは Microsoft Edge TTS のオンライン音声サービスへ送信されます。\n"
            "2. App 自体はアカウント登録を求めず、広告や独自の分析機能もなく、氏名・電話番号・メールアドレスなどの個人識別情報を積極的に収集しません。\n"
            "3. 「txt を読み込む」で選んだファイルはローカルでのみ読み込まれ、「保存先」で選んだ場所には生成した mp3 だけを保存します。\n"
            "4. サポートへメールを送る場合、その内容は利用中のメール事業者と受信側事業者によって処理されます。\n"
            "5. 生成済み音声を削除したい場合は、Mac 上で該当ファイルを削除してください。"
        ),
        "exit_prompt": "エラーが発生しました。Enter キーで閉じます…",
    },
}

_SILENCE_100MS_B64 = (
    "//NkxAAAAANIAAAAAExBTUVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NkxHwAAANIAAAAAFVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NkxHwAAANIAAAAAFVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NkxHwAAANIAAAAAFVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NkxHwAAANIAAAAAFVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NkxHwAAANIAAAAAFVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NkxHwAAANIAAAAAFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"
)
_SILENCE_100MS = base64.b64decode(_SILENCE_100MS_B64)


def silence_bytes(seconds):
    n = max(0, round(seconds / 0.1))
    return _SILENCE_100MS * n


def safe_name(text, idx):
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "_", text).strip("_")[:40]
    return f"{idx:03d}_{s or 'line'}.mp3"


def _normalize_lang(value):
    if not value:
        return None
    for chunk in re.split(r"[:;,\s]+", value):
        token = chunk.strip().strip('"').split(".")[0].replace("_", "-").lower()
        if token.startswith("ja"):
            return "ja"
        if token.startswith("zh"):
            return "zh"
    return None


def detect_system_language():
    try:
        result = subprocess.run(
            ["defaults", "read", "-g", "AppleLanguages"],
            capture_output=True,
            text=True,
            check=True,
        )
        detected = _normalize_lang(result.stdout)
        if detected:
            return detected
    except Exception:
        pass

    for env_name in ("LC_ALL", "LC_MESSAGES", "LANGUAGE", "LANG"):
        detected = _normalize_lang(os.environ.get(env_name, ""))
        if detected:
            return detected

    try:
        lang_code, _ = locale.getlocale()
        detected = _normalize_lang(lang_code or "")
        if detected:
            return detected
    except Exception:
        pass

    return "zh"


def default_output_dir():
    return os.path.expanduser("~/Desktop")


async def _speak(text, out_path, voice, rate):
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    await communicate.save(out_path)


async def _speak_to_bytes(text, voice, rate):
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    buf = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.extend(chunk["data"])
    return bytes(buf)


# ===================== 自绘按钮（保证配色一致） =====================
class FlatButton(tk.Canvas):
    def __init__(self, parent, text, command, kind="primary", font_key="btn_font", **kw):
        self.t = THEME
        self.kind = kind
        self.command = command
        self.enabled = True
        self.font_key = font_key
        h = self.t["btn_h"]
        super().__init__(parent, height=h, bd=0, highlightthickness=0, bg=self.t["bg"], **kw)
        self._text = text
        self.bind("<Configure>", lambda e: self._draw())
        self.bind("<Button-1>", self._click)
        self.bind("<Enter>", lambda e: self._draw(hover=True))
        self.bind("<Leave>", lambda e: self._draw(hover=False))

    def _colors(self, hover):
        t = self.t
        if not self.enabled:
            return t["btn_disabled_bg"], t["btn_disabled_fg"]
        if self.kind == "primary":
            return (t["primary_hover"] if hover else t["primary"]), t["on_primary"]
        if self.kind == "accent":
            return (t["accent_hover"] if hover else t["accent"]), t["on_accent"]
        return (t["ghost_hover"] if hover else t["ghost_bg"]), t["ghost_fg"]

    def _draw(self, hover=False):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 4:
            return
        bg, fg = self._colors(hover)
        r = self.t["radius"]
        self._round_rect(0, 0, w, h, r, fill=bg, outline=self.t.get("btn_border", bg))
        self.create_text(w // 2, h // 2, text=self._text, fill=fg, font=self.t[self.font_key])

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        x2 -= 1
        y2 -= 1
        pts = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
            x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        self.create_polygon(pts, smooth=True, **kw)

    def _click(self, _event):
        if self.enabled and self.command:
            self.command()

    def set_enabled(self, on):
        self.enabled = on
        self._draw()

    def set_text(self, text):
        self._text = text
        self._draw()


# ===================== 主界面 =====================
class App:
    def __init__(self, root):
        self.root = root
        self.t = THEME
        self.window_width = 920
        self.system_lang = detect_system_language()
        self.language_pref = "auto"
        self.ui_lang = self._effective_lang(self.language_pref)
        self.current_voice_id = VOICE_OPTIONS[0]["id"]
        self.status_state = ("status_ready", {})
        self.language_value_to_code = {}
        self.voice_value_to_id = {}

        root.configure(bg=self.t["bg"])

        wrap = tk.Frame(root, bg=self.t["bg"])
        wrap.pack(fill="both", expand=True, padx=self.t["pad"], pady=self.t["pad"])
        self.wrap = wrap

        title_row = tk.Frame(wrap, bg=self.t["bg"])
        title_row.pack(anchor="w")
        self.title_main_label = tk.Label(
            title_row,
            bg=self.t["bg"],
            fg=self.t["title_fg"],
            font=self.t["title_font"],
        )
        self.title_main_label.pack(side="left")
        self.title_sub_label = tk.Label(
            title_row,
            bg=self.t["bg"],
            fg=self.t["muted_fg"],
            font=self.t["title_en_font"],
        )
        self.title_sub_label.pack(side="left", anchor="s", pady=(0, 3))
        self.credit_label = tk.Label(
            wrap,
            bg=self.t["bg"],
            fg=self.t["muted_fg"],
            font=self.t["credit_font"],
        )
        self.credit_label.pack(anchor="w", pady=(2, 0))
        self.input_hint_label = tk.Label(
            wrap,
            bg=self.t["bg"],
            fg=self.t["muted_fg"],
            font=self.t["hint_font"],
        )
        self.input_hint_label.pack(anchor="w", pady=(16, 10))

        txt_wrap = tk.Frame(wrap, bg=self.t["field_border"], bd=0)
        txt_wrap.pack(fill="both", expand=True)
        self.text = tk.Text(
            txt_wrap,
            height=8,
            wrap="word",
            font=self.t["area_font"],
            bg=self.t["field_bg"],
            fg=self.t["text_fg"],
            bd=0,
            highlightthickness=self.t["field_bw"],
            highlightbackground=self.t["field_border"],
            highlightcolor=self.t["primary"],
            insertbackground=self.t["text_fg"],
            spacing1=7,
            spacing2=4,
            spacing3=7,
            padx=12,
            pady=10,
        )
        self.text.pack(fill="both", expand=True, padx=self.t["field_bw"], pady=self.t["field_bw"])

        row_file = tk.Frame(wrap, bg=self.t["bg"])
        row_file.pack(fill="x", pady=(10, 4))
        self.import_link = self._mini(row_file, "", self.load_file)
        self.import_link.pack(side="left")
        self.clear_link = self._mini(row_file, "", lambda: self.text.delete("1.0", "end"))
        self.clear_link.pack(side="left", padx=8)

        card = tk.Frame(wrap, bg=self.t["card_bg"])
        card.pack(fill="x", pady=8)
        inner = tk.Frame(card, bg=self.t["card_bg"])
        inner.pack(fill="x", padx=14, pady=12)

        self.language_combo = self._labeled_combo(inner, "", [], 0, 0, width=16)
        self.language_combo.bind("<<ComboboxSelected>>", self.on_language_selected)
        self.voice_combo = self._labeled_combo(inner, "", [], 0, 2, width=24)
        self.voice_combo.bind("<<ComboboxSelected>>", self.on_voice_selected)
        self.rate_combo = self._labeled_combo(inner, "", RATE_OPTIONS, 0, 4, width=7)
        self.rate_combo.set("-10%")
        self.merge = tk.BooleanVar(value=False)
        self.merge_check = self._check(inner, "", self.merge)
        self.merge_check.grid(row=1, column=0, columnspan=6, sticky="w", pady=(10, 0))

        row_out = tk.Frame(wrap, bg=self.t["bg"])
        row_out.pack(fill="x", pady=(4, 8))
        self.outdir_label = tk.Label(
            row_out,
            bg=self.t["bg"],
            fg=self.t["muted_fg"],
            font=self.t["small_font"],
        )
        self.outdir_label.pack(side="left")
        self.outdir = tk.StringVar(value=default_output_dir())
        self.outdir_entry = tk.Entry(
            row_out,
            textvariable=self.outdir,
            font=self.t["small_font"],
            bg=self.t["field_bg"],
            fg=self.t["text_fg"],
            bd=0,
            highlightthickness=1,
            highlightbackground=self.t["field_border"],
            highlightcolor=self.t["primary"],
        )
        self.outdir_entry.pack(side="left", fill="x", expand=True, padx=8, ipady=4)
        self.choose_link = self._mini(row_out, "", self.pick_dir)
        self.choose_link.pack(side="left")

        row_name = tk.Frame(wrap, bg=self.t["bg"])
        row_name.pack(fill="x", pady=(0, 8))
        self.filename_label = tk.Label(
            row_name,
            bg=self.t["bg"],
            fg=self.t["muted_fg"],
            font=self.t["small_font"],
        )
        self.filename_label.pack(side="left")
        self.fname = tk.StringVar(value=TEXTS["zh"]["default_filename"])
        self.filename_entry = tk.Entry(
            row_name,
            textvariable=self.fname,
            font=self.t["small_font"],
            bg=self.t["field_bg"],
            fg=self.t["text_fg"],
            bd=0,
            highlightthickness=1,
            highlightbackground=self.t["field_border"],
            highlightcolor=self.t["primary"],
        )
        self.filename_entry.pack(side="left", fill="x", expand=True, padx=8, ipady=4)
        self.filename_suffix_label = tk.Label(
            row_name,
            text=".mp3",
            bg=self.t["bg"],
            fg=self.t["muted_fg"],
            font=self.t["small_font"],
        )
        self.filename_suffix_label.pack(side="left")

        btn_row = tk.Frame(wrap, bg=self.t["bg"])
        btn_row.pack(pady=(10, 4))
        self.btn = FlatButton(btn_row, "", self.start, kind="ghost", width=200, font_key="btn_small")
        self.btn.pack(side="left", padx=(0, 10))
        self.btn3 = FlatButton(btn_row, "", self.start_three, kind="primary", width=200, font_key="btn_small")
        self.btn3.pack(side="left")

        self.strong_desc_label = tk.Label(
            wrap,
            bg=self.t["bg"],
            fg=self.t["muted_fg"],
            font=self.t["tiny_font"],
            anchor="w",
            justify="left",
            wraplength=700,
        )
        self.strong_desc_label.pack(fill="x", pady=(10, 0))

        self.status = tk.Label(
            wrap,
            bg=self.t["bg"],
            fg=self.t["muted_fg"],
            font=self.t["small_font"],
            anchor="w",
        )
        self.status.pack(fill="x", pady=(10, 0))
        footer_links = tk.Frame(wrap, bg=self.t["bg"])
        footer_links.pack(fill="x", pady=(6, 0))
        self.support_link = self._mini(footer_links, "", self.show_support_info)
        self.support_link.pack(side="left")
        self.link_divider = tk.Label(
            footer_links,
            text=" · ",
            bg=self.t["bg"],
            fg=self.t["muted_fg"],
            font=self.t["small_font"],
        )
        self.link_divider.pack(side="left")
        self.privacy_link = self._mini(footer_links, "", self.show_privacy_policy)
        self.privacy_link.pack(side="left")

        self.apply_language(self.ui_lang, force_status=True)

        win_w = self.window_width
        root.geometry(f"{win_w}x560")
        self._resize_window(win_w)
        root.resizable(False, False)

    # ---------- 本地化 ----------
    def _effective_lang(self, lang_code):
        return self.system_lang if lang_code == "auto" else lang_code

    def tr(self, key, **kwargs):
        return TEXTS[self.ui_lang][key].format(**kwargs)

    def _language_label(self, lang_code):
        for code, labels in LANGUAGE_OPTIONS:
            if code == lang_code:
                return labels[self.ui_lang]
        return lang_code

    def _voice_label(self, voice_id):
        return VOICE_BY_ID[voice_id]["labels"][self.ui_lang]

    def apply_language(self, lang_code, force_status=False):
        self.ui_lang = lang_code
        self.root.title(self.tr("app_title"))

        self.title_main_label.config(text=self.tr("title_main"))
        self.title_sub_label.config(text=self.tr("title_sub"))
        self.credit_label.config(text=self.tr("credit"))
        self.input_hint_label.config(text=self.tr("input_hint"))
        self.import_link.config(text=self.tr("import_txt"))
        self.clear_link.config(text=self.tr("clear"))
        self.outdir_label.config(text=self.tr("output_to"))
        self.filename_label.config(text=self.tr("filename"))
        self.choose_link.config(text=self.tr("choose"))
        self.support_link.config(text=self.tr("support_link"))
        self.privacy_link.config(text=self.tr("privacy_link"))
        self.btn.set_text(self.tr("generate"))
        self.btn3.set_text(self.tr("strong_generate"))
        self.merge_check.config(text=self.tr("merge_audio"))
        self.strong_desc_label.config(text=self.tr("strong_desc"))

        self._update_combo_label(self.language_combo, self.tr("language_label"))
        self._update_combo_label(self.voice_combo, self.tr("voice_label"))
        self._update_combo_label(self.rate_combo, self.tr("rate_label"))

        self.language_value_to_code = {
            self._language_label(code): code for code, _labels in LANGUAGE_OPTIONS
        }
        self.language_combo["values"] = list(self.language_value_to_code.keys())
        self.language_combo.set(self._language_label(self.language_pref))

        self.voice_value_to_id = {
            self._voice_label(voice["id"]): voice["id"] for voice in VOICE_OPTIONS
        }
        self.voice_combo["values"] = list(self.voice_value_to_id.keys())
        self.voice_combo.set(self._voice_label(self.current_voice_id))

        if not self.fname.get().strip():
            self.fname.set(self.tr("default_filename"))

        if force_status:
            self.set_status_key("status_ready")
        else:
            self._refresh_status()

        self._resize_window(self.window_width)

    def _refresh_status(self):
        key, kwargs = self.status_state
        self.status.config(text=self.tr(key, **kwargs))
        self.root.update_idletasks()

    # ---------- 小组件工厂 ----------
    def _mini(self, parent, text, cmd):
        b = tk.Label(
            parent,
            text=text,
            bg=self.t["bg"],
            fg=self.t["link_fg"],
            font=self.t["small_font"],
            cursor="hand2",
        )
        b.bind("<Button-1>", lambda _event: cmd())
        return b

    def _labeled_combo(self, parent, label, values, r, c, width=10, pady=(0, 0)):
        from tkinter import ttk

        wrapper = tk.Frame(parent, bg=self.t["card_bg"])
        wrapper.grid(row=r, column=c, columnspan=2, sticky="w", pady=pady, padx=(0, 16))

        lbl = tk.Label(
            wrapper,
            text=label,
            bg=self.t["card_bg"],
            fg=self.t["muted_fg"],
            font=self.t["small_font"],
        )
        lbl.pack(side="left", padx=(0, 6))

        cb = ttk.Combobox(wrapper, values=values, state="readonly", width=width)
        cb.pack(side="left")
        cb._label_widget = lbl
        return cb

    def _update_combo_label(self, combo, label_text):
        combo._label_widget.config(text=label_text)

    def _check(self, parent, text, var):
        return tk.Checkbutton(
            parent,
            text=text,
            variable=var,
            bg=self.t["card_bg"],
            fg=self.t["text_fg"],
            selectcolor=self.t["field_bg"],
            activebackground=self.t["card_bg"],
            font=self.t["small_font"],
            bd=0,
            highlightthickness=0,
        )

    def _resize_window(self, width):
        self.root.update_idletasks()
        need_h = self.wrap.winfo_reqheight() + 2 * self.t["pad"]
        self.root.geometry(f"{width}x{need_h}")

    def _show_text_sheet(self, title, body):
        sheet = tk.Toplevel(self.root)
        sheet.title(title)
        sheet.configure(bg=self.t["bg"])
        sheet.transient(self.root)
        sheet.resizable(False, False)
        sheet.grab_set()

        wrap = tk.Frame(sheet, bg=self.t["bg"])
        wrap.pack(fill="both", expand=True, padx=self.t["pad"], pady=self.t["pad"])

        tk.Label(
            wrap,
            text=title,
            bg=self.t["bg"],
            fg=self.t["title_fg"],
            font=self.t["title_en_font"],
            anchor="w",
        ).pack(fill="x", pady=(0, 10))

        text = tk.Text(
            wrap,
            height=14,
            width=70,
            wrap="word",
            font=self.t["text_font"],
            bg=self.t["field_bg"],
            fg=self.t["text_fg"],
            bd=0,
            highlightthickness=1,
            highlightbackground=self.t["field_border"],
            highlightcolor=self.t["primary"],
            padx=12,
            pady=10,
        )
        text.pack(fill="both", expand=True)
        text.insert("1.0", body)
        text.config(state="disabled")

        actions = tk.Frame(wrap, bg=self.t["bg"])
        actions.pack(fill="x", pady=(12, 0))
        close_btn = FlatButton(actions, self.tr("close"), sheet.destroy, kind="primary", width=120, font_key="btn_small")
        close_btn.pack(anchor="e")

        sheet.update_idletasks()
        sheet.geometry(f"720x{sheet.winfo_reqheight()}")

    def show_support_info(self):
        self._show_text_sheet(self.tr("support_title"), self.tr("support_body"))

    def show_privacy_policy(self):
        self._show_text_sheet(self.tr("privacy_title"), self.tr("privacy_body"))

    # ---------- 事件 ----------
    def on_language_selected(self, _event=None):
        label = self.language_combo.get()
        code = self.language_value_to_code.get(label, "auto")
        self.language_pref = code
        self.apply_language(self._effective_lang(code))

    def on_voice_selected(self, _event=None):
        label = self.voice_combo.get()
        self.current_voice_id = self.voice_value_to_id.get(label, VOICE_OPTIONS[0]["id"])

    # ---------- 行为 ----------
    def load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[
                (self.tr("filetype_text"), "*.txt"),
                (self.tr("filetype_all"), "*.*"),
            ]
        )
        if path:
            with open(path, encoding="utf-8") as fh:
                self.text.delete("1.0", "end")
                self.text.insert("1.0", fh.read())

    def pick_dir(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.outdir.set(selected_dir)

    def _get_lines(self):
        return [ln.strip() for ln in self.text.get("1.0", "end").splitlines() if ln.strip()]

    def _busy(self, on):
        self.btn.set_enabled(not on)
        self.btn3.set_enabled(not on)

    def start(self):
        lines = self._get_lines()
        if not lines:
            messagebox.showwarning(self.tr("warn_title"), self.tr("no_text_warning"))
            return
        self._busy(True)
        threading.Thread(target=self.worker, args=(lines,), daemon=True).start()

    def start_three(self):
        lines = self._get_lines()
        if not lines:
            messagebox.showwarning(self.tr("warn_title"), self.tr("no_text_warning"))
            return
        self._busy(True)
        threading.Thread(target=self.worker_three, args=(lines,), daemon=True).start()

    def _clean_name(self):
        name = self.fname.get().strip() or self.tr("default_filename")
        name = re.sub(r"\.mp3$", "", name, flags=re.IGNORECASE)
        name = re.sub(r'[/\\:*?"<>|]', "_", name)
        return name

    def _unique_path(self, outdir, name):
        path = os.path.join(outdir, name + ".mp3")
        if not os.path.exists(path):
            return path
        k = 2
        while True:
            candidate = os.path.join(outdir, f"{name}_{k}.mp3")
            if not os.path.exists(candidate):
                return candidate
            k += 1

    def worker_three(self, lines):
        outdir = self.outdir.get()
        os.makedirs(outdir, exist_ok=True)
        out_path = self._unique_path(outdir, self._clean_name())
        gap_rep = silence_bytes(0.5)
        gap_line = silence_bytes(1.0)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            total = len(lines)
            with open(out_path, "wb") as fout:
                for i, line in enumerate(lines, 1):
                    self.set_status_key("status_generating_three", current=i, total=total)
                    for j, (voice, rate) in enumerate(REPEAT_SEQUENCE):
                        data = loop.run_until_complete(_speak_to_bytes(line, voice, rate))
                        fout.write(data)
                        if j < len(REPEAT_SEQUENCE) - 1:
                            fout.write(gap_rep)
                    if i < total:
                        fout.write(gap_line)
            self.set_status_key("status_done_file", path=out_path)
            messagebox.showinfo(self.tr("done_title"), self.tr("done_three_message", path=out_path))
        except Exception as e:
            self.set_status_key("status_error")
            messagebox.showerror(self.tr("error_title"), str(e))
        finally:
            loop.close()
            self._busy(False)

    def worker(self, lines):
        voice = self.current_voice_id
        rate = self.rate_combo.get()
        outdir = self.outdir.get()
        os.makedirs(outdir, exist_ok=True)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            base = self._clean_name()
            if self.merge.get():
                self.set_status_key("status_generating_merged")
                out = self._unique_path(outdir, base)
                loop.run_until_complete(_speak("\n".join(lines), out, voice, rate))
            else:
                stem = re.sub(r"[\s_]*\d+$", "", base) or base
                total = len(lines)
                for i, line in enumerate(lines, 1):
                    self.set_status_key("status_generating_single", current=i, total=total)
                    out = self._unique_path(outdir, f"{stem} {i:02d}")
                    loop.run_until_complete(_speak(line, out, voice, rate))
            self.set_status_key("status_done_dir", path=outdir)
            messagebox.showinfo(self.tr("done_title"), self.tr("done_dir_message", path=outdir))
        except Exception as e:
            self.set_status_key("status_error")
            messagebox.showerror(self.tr("error_title"), str(e))
        finally:
            loop.close()
            self._busy(False)

    def set_status_key(self, key, **kwargs):
        self.status_state = (key, kwargs)
        self._refresh_status()


if __name__ == "__main__":
    root = tk.Tk()
    try:
        App(root)
        root.mainloop()
    except Exception:
        import traceback

        traceback.print_exc()
        fallback_lang = detect_system_language()
        input(TEXTS.get(fallback_lang, TEXTS["zh"])["exit_prompt"])

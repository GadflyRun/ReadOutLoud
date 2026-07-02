#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
朗读音频生成器 —— Apple 风 · 浅色
基于 edge-tts。首次使用前在终端运行一次： pip install edge-tts
"""

import os
import re
import base64
import threading
import asyncio
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    import edge_tts
except ImportError:
    raise SystemExit("请先安装：pip install edge-tts")


# ===================== 主题 =====================
THEME = {       'accent': '#E8E8ED',
        'accent_hover': '#DDDDE3',
        'bg': '#F5F5F7',
        'btn_border': '#D2D2D7',
        'btn_disabled_bg': '#E8E8ED',
        'btn_disabled_fg': '#AEAEB2',
        'btn_font': ('Helvetica Neue', 13),
        'btn_small': ('Helvetica Neue', 11),
        'btn_h': 44,
        'card_bg': '#FFFFFF',
        'field_bg': '#FFFFFF',
        'field_border': '#D2D2D7',
        'field_bw': 1,
        'ghost_bg': '#FFFFFF',
        'ghost_fg': '#007AFF',
        'ghost_hover': '#F0F0F2',
        'link_fg': '#0066CC',
        'muted_fg': '#86868B',
        'on_accent': '#007AFF',
        'on_primary': '#FFFFFF',
        'pad': 24,
        'primary': '#007AFF',
        'primary_hover': '#0a6fe0',
        'radius': 12,
        'small_font': ('Helvetica Neue', 11),
        'tiny_font': ('Helvetica Neue', 10),
        'credit_font': ('Helvetica Neue', 11, 'bold'),
        'hint_font': ('Helvetica Neue', 10),
        'text_fg': '#1D1D1F',
        'text_font': ('Helvetica Neue', 12),
        'area_font': ('Helvetica Neue', 10),
        'title_fg': '#1D1D1F',
        'title_font': ('Helvetica Neue', 20, 'bold'),
        'title_en_font': ('Helvetica Neue', 14, 'bold')}
# ================================================


VOICES = {
    "美音女声 Aria":   "en-US-AriaNeural",
    "美音女声 Jenny":  "en-US-JennyNeural",
    "美音男声 Guy":    "en-US-GuyNeural",
    "英音女声 Sonia":  "en-GB-SoniaNeural",
    "英音男声 Ryan":   "en-GB-RyanNeural",
}

REPEAT_SEQUENCE = [
    ("en-US-AriaNeural",  "-20%"),
    ("en-US-GuyNeural",   "-30%"),
    ("en-US-JennyNeural", "-10%"),
]

_SILENCE_100MS_B64 = (
    "//NkxAAAAANIAAAAAExBTUVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NkxHwAAANIAAAAAFVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NkxHwAAANIAAAAAFVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NkxHwAAANIAAAAAFVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NkxHwAAANIAAAAAFVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NkxHwAAANIAAAAAFVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NkxHwAAANIAAAAAFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"
)
_SILENCE_100MS = base64.b64decode(_SILENCE_100MS_B64)


def silence_bytes(seconds):
    n = max(0, round(seconds / 0.1))
    return _SILENCE_100MS * n


def safe_name(text, idx):
    s = re.sub(r'[^\w\u4e00-\u9fff]+', '_', text).strip('_')[:40]
    return f"{idx:03d}_{s or 'line'}.mp3"


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
        super().__init__(parent, height=h, bd=0, highlightthickness=0,
                         bg=self.t["bg"], **kw)
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
        self.create_text(w // 2, h // 2, text=self._text,
                         fill=fg, font=self.t[self.font_key])

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        x2 -= 1; y2 -= 1
        pts = [x1+r,y1, x2-r,y1, x2,y1, x2,y1+r, x2,y2-r, x2,y2,
               x2-r,y2, x1+r,y2, x1,y2, x1,y2-r, x1,y1+r, x1,y1]
        self.create_polygon(pts, smooth=True, **kw)

    def _click(self, e):
        if self.enabled and self.command:
            self.command()

    def set_enabled(self, on):
        self.enabled = on
        self._draw()


# ===================== 主界面 =====================
class App:
    def __init__(self, root):
        self.root = root
        self.t = THEME
        root.title("朗读音频生成器")
        root.configure(bg=self.t["bg"])

        wrap = tk.Frame(root, bg=self.t["bg"])
        wrap.pack(fill="both", expand=True, padx=self.t["pad"], pady=self.t["pad"])

        # 标题
        title_row = tk.Frame(wrap, bg=self.t["bg"])
        title_row.pack(anchor="w")
        tk.Label(title_row, text="朗读音频生成器", bg=self.t["bg"], fg=self.t["title_fg"],
                 font=self.t["title_font"]).pack(side="left")
        tk.Label(title_row, text=" Audio Generator", bg=self.t["bg"], fg=self.t["muted_fg"],
                 font=self.t["title_en_font"]).pack(side="left", anchor="s", pady=(0, 3))
        tk.Label(wrap, text="Designed by Socranotes, Coded by Claude Code", bg=self.t["bg"],
                 fg=self.t["muted_fg"], font=self.t["credit_font"]).pack(anchor="w", pady=(2, 0))
        tk.Label(wrap, text="输入文本，每行一句或一个单词", bg=self.t["bg"],
                 fg=self.t["muted_fg"], font=self.t["hint_font"]).pack(anchor="w", pady=(16, 10))

        # 文本框
        txt_wrap = tk.Frame(wrap, bg=self.t["field_border"], bd=0)
        txt_wrap.pack(fill="both", expand=True)
        self.text = tk.Text(txt_wrap, height=8, wrap="word", font=self.t["area_font"],
                            bg=self.t["field_bg"], fg=self.t["text_fg"], bd=0,
                            highlightthickness=self.t["field_bw"],
                            highlightbackground=self.t["field_border"],
                            highlightcolor=self.t["primary"],
                            insertbackground=self.t["text_fg"],
                            spacing1=7, spacing2=4, spacing3=7,
                            padx=12, pady=10)
        self.text.pack(fill="both", expand=True, padx=self.t["field_bw"], pady=self.t["field_bw"])
        self.text.insert("1.0",
            "简单说 4 句：\n"
            "1. 本 App 由 叶晓凯，也就是我，与 Claude Code 制作，完全免费，供教培老师与英语学习者使用。\n"
            "2. 界面比较简陋，没顾上优化版式，凑合用吧 :)\n"
            "3. 如果你有优化本 App 的想法，或者你想根据自己的需求定制小型 App，欢迎通过邮箱 socranote@gmail.com 与我交流。\n"
            "4. 如果你想跟我学英文，欢迎通过微信 yxkenglish 咨询报名我的词汇、高考、雅思、DSE、外刊原著精读等课程 ^_^")

        # 文件行
        row_file = tk.Frame(wrap, bg=self.t["bg"])
        row_file.pack(fill="x", pady=(10, 4))
        self._mini(row_file, "导入 txt…", self.load_file).pack(side="left")
        self._mini(row_file, "清空", lambda: self.text.delete("1.0", "end")).pack(side="left", padx=8)

        # 参数卡片
        card = tk.Frame(wrap, bg=self.t["card_bg"])
        card.pack(fill="x", pady=8)
        inner = tk.Frame(card, bg=self.t["card_bg"])
        inner.pack(fill="x", padx=14, pady=12)

        self.voice = self._labeled_combo(inner, "语音", list(VOICES.keys()), 0, 0, width=16)
        self.voice.set(list(VOICES.keys())[0])
        self.rate = self._labeled_combo(inner, "语速",
                                        ["-30%", "-20%", "-10%", "+0%", "+10%", "+20%"], 0, 2, width=7)
        self.rate.set("-10%")
        self.merge = tk.BooleanVar(value=False)
        self._check(inner, "合并成一个音频", self.merge).grid(row=0, column=4, sticky="w", padx=(14, 0))

        # 输出目录
        row_out = tk.Frame(wrap, bg=self.t["bg"])
        row_out.pack(fill="x", pady=(4, 8))
        tk.Label(row_out, text="输出到", bg=self.t["bg"], fg=self.t["muted_fg"],
                 font=self.t["small_font"]).pack(side="left")
        self.outdir = tk.StringVar(value=os.path.abspath("audio"))
        ent = tk.Entry(row_out, textvariable=self.outdir, font=self.t["small_font"],
                       bg=self.t["field_bg"], fg=self.t["text_fg"], bd=0,
                       highlightthickness=1, highlightbackground=self.t["field_border"],
                       highlightcolor=self.t["primary"])
        ent.pack(side="left", fill="x", expand=True, padx=8, ipady=4)
        self._mini(row_out, "选择…", self.pick_dir).pack(side="left")

        # 文件名
        row_name = tk.Frame(wrap, bg=self.t["bg"])
        row_name.pack(fill="x", pady=(0, 8))
        tk.Label(row_name, text="文件名", bg=self.t["bg"], fg=self.t["muted_fg"],
                 font=self.t["small_font"]).pack(side="left")
        self.fname = tk.StringVar(value="tts_output 01")
        ent_name = tk.Entry(row_name, textvariable=self.fname, font=self.t["small_font"],
                            bg=self.t["field_bg"], fg=self.t["text_fg"], bd=0,
                            highlightthickness=1, highlightbackground=self.t["field_border"],
                            highlightcolor=self.t["primary"])
        ent_name.pack(side="left", fill="x", expand=True, padx=8, ipady=4)
        tk.Label(row_name, text=".mp3", bg=self.t["bg"], fg=self.t["muted_fg"],
                 font=self.t["small_font"]).pack(side="left")

        # 主按钮（等宽并列，居中）
        btn_row = tk.Frame(wrap, bg=self.t["bg"])
        btn_row.pack(pady=(10, 4))
        self.btn = FlatButton(btn_row, "按上方设置生成", self.start, kind="ghost",
                              width=160, font_key="btn_small")
        self.btn.pack(side="left", padx=(0, 10))
        self.btn3 = FlatButton(btn_row, "用我的强推设置生成", self.start_three, kind="primary",
                               width=160, font_key="btn_small")
        self.btn3.pack(side="left")

        # 强推设置的说明
        tk.Label(wrap,
                 text=("强推设置：每个单词/句子连读 3 遍，依次为 "
                       "Aria 慢速(-20%) → Guy 更慢(-30%) → Jenny 稍慢(-10%)，"
                       "三种声音交替，让耳朵适应不同音色；每遍之间停顿 0.5 秒、每字/句之间停顿 1 秒，"
                       "供学习者回顾刚听到的内容，或进行跟读。"),
                 bg=self.t["bg"], fg=self.t["muted_fg"], font=self.t["tiny_font"],
                 anchor="w", justify="left", wraplength=560).pack(fill="x", pady=(10, 0))

        self.status = tk.Label(wrap, text="就绪", bg=self.t["bg"], fg=self.t["muted_fg"],
                               font=self.t["small_font"], anchor="w")
        self.status.pack(fill="x", pady=(10, 0))

        # 固定窗口尺寸（宽度不可调）
        win_w = 800
        root.geometry(f"{win_w}x560")
        root.update_idletasks()
        need_h = wrap.winfo_reqheight() + 2 * self.t["pad"]
        root.geometry(f"{win_w}x{need_h}")
        root.resizable(False, False)

    # ---------- 小组件工厂 ----------
    def _mini(self, parent, text, cmd):
        b = tk.Label(parent, text=text, bg=self.t["bg"], fg=self.t["link_fg"],
                     font=self.t["small_font"], cursor="hand2")
        b.bind("<Button-1>", lambda e: cmd())
        return b

    def _labeled_combo(self, parent, label, values, r, c, width=10, pady=(0, 0)):
        from tkinter import ttk
        tk.Label(parent, text=label, bg=self.t["card_bg"], fg=self.t["muted_fg"],
                 font=self.t["small_font"]).grid(row=r, column=c, sticky="w", pady=pady, padx=(0, 6))
        cb = ttk.Combobox(parent, values=values, state="readonly", width=width)
        cb.grid(row=r, column=c+1, sticky="w", pady=pady, padx=(0, 16))
        return cb

    def _check(self, parent, text, var):
        return tk.Checkbutton(parent, text=text, variable=var, bg=self.t["card_bg"],
                              fg=self.t["text_fg"], selectcolor=self.t["field_bg"],
                              activebackground=self.t["card_bg"], font=self.t["small_font"],
                              bd=0, highlightthickness=0)

    # ---------- 行为 ----------
    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
        if path:
            with open(path, encoding="utf-8") as fh:
                self.text.delete("1.0", "end")
                self.text.insert("1.0", fh.read())

    def pick_dir(self):
        d = filedialog.askdirectory()
        if d:
            self.outdir.set(d)

    def _get_lines(self):
        return [ln.strip() for ln in self.text.get("1.0", "end").splitlines() if ln.strip()]

    def _busy(self, on):
        self.btn.set_enabled(not on)
        self.btn3.set_enabled(not on)

    def start(self):
        lines = self._get_lines()
        if not lines:
            messagebox.showwarning("提示", "请先输入文本")
            return
        self._busy(True)
        threading.Thread(target=self.worker, args=(lines,), daemon=True).start()

    def start_three(self):
        lines = self._get_lines()
        if not lines:
            messagebox.showwarning("提示", "请先输入文本")
            return
        self._busy(True)
        threading.Thread(target=self.worker_three, args=(lines,), daemon=True).start()

    def _clean_name(self):
        """取用户填写的文件名，去掉非法字符和已有的 .mp3 后缀。"""
        name = self.fname.get().strip() or "tts_output 01"
        name = re.sub(r'\.mp3$', '', name, flags=re.IGNORECASE)
        name = re.sub(r'[/\\:*?"<>|]', '_', name)
        return name

    def _unique_path(self, outdir, name):
        """返回 outdir/name.mp3，若已存在则自动加序号避免覆盖。"""
        path = os.path.join(outdir, name + ".mp3")
        if not os.path.exists(path):
            return path
        k = 2
        while True:
            p = os.path.join(outdir, f"{name}_{k}.mp3")
            if not os.path.exists(p):
                return p
            k += 1

    def worker_three(self, lines):
        outdir = self.outdir.get()
        os.makedirs(outdir, exist_ok=True)
        seq = REPEAT_SEQUENCE                # 固定 3 遍：Aria → Guy → Jenny
        out_path = self._unique_path(outdir, self._clean_name())
        gap_rep = silence_bytes(0.5)         # 每遍间停顿 0.5 秒
        gap_line = silence_bytes(1.0)        # 每句间停顿 1 秒
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            total = len(lines)
            with open(out_path, "wb") as fout:
                for i, line in enumerate(lines, 1):
                    self.set_status(f"正在生成 {i}/{total} 句（每句三遍）…")
                    for j, (voice, rate) in enumerate(seq):
                        data = loop.run_until_complete(_speak_to_bytes(line, voice, rate))
                        fout.write(data)
                        if j < len(seq) - 1:
                            fout.write(gap_rep)
                    if i < total:
                        fout.write(gap_line)
            self.set_status(f"完成！已保存到 {out_path}")
            messagebox.showinfo("完成",
                                f"已生成一个音频，每句按 Aria → Guy → Jenny 读三遍：\n\n{out_path}")
        except Exception as e:
            self.set_status("出错")
            messagebox.showerror("错误", str(e))
        finally:
            loop.close()
            self._busy(False)

    def worker(self, lines):
        voice = VOICES[self.voice.get()]
        rate = self.rate.get()
        outdir = self.outdir.get()
        os.makedirs(outdir, exist_ok=True)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            base = self._clean_name()
            if self.merge.get():
                self.set_status("正在生成合并音频…")
                out = self._unique_path(outdir, base)
                loop.run_until_complete(_speak("\n".join(lines), out, voice, rate))
            else:
                stem = re.sub(r'[\s_]*\d+$', '', base) or base
                for i, line in enumerate(lines, 1):
                    self.set_status(f"正在生成 {i}/{len(lines)} …")
                    out = self._unique_path(outdir, f"{stem} {i:02d}")
                    loop.run_until_complete(_speak(line, out, voice, rate))
            self.set_status(f"完成！已保存到 {outdir}")
            messagebox.showinfo("完成", f"音频已保存到：\n{outdir}")
        except Exception as e:
            self.set_status("出错")
            messagebox.showerror("错误", str(e))
        finally:
            loop.close()
            self._busy(False)

    def set_status(self, text):
        self.status.config(text=text)
        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    try:
        App(root)
        root.mainloop()
    except Exception as e:
        import traceback; traceback.print_exc()
        input("出错了，按回车关闭…")

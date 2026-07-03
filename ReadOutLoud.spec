# -*- mode: python ; coding: utf-8 -*-
import os

from PyInstaller.utils.hooks import collect_all

APP_NAME = os.environ.get("READOUTLOUD_APP_NAME", "ReadOutLoud")
BUNDLE_ID = os.environ.get("READOUTLOUD_BUNDLE_ID", "com.socranotes.readoutloud")
APP_VERSION = os.environ.get("READOUTLOUD_VERSION", "1.0.0")
BUILD_NUMBER = os.environ.get("READOUTLOUD_BUILD", "1")
MIN_MACOS = os.environ.get("READOUTLOUD_MIN_MACOS", "12.0")
APP_CATEGORY = os.environ.get("READOUTLOUD_CATEGORY", "public.app-category.education")
TARGET_ARCH = os.environ.get("READOUTLOUD_TARGET_ARCH") or None
CODE_SIGN_IDENTITY = os.environ.get("READOUTLOUD_CODESIGN_IDENTITY") or None
ENTITLEMENTS_FILE = os.environ.get("READOUTLOUD_ENTITLEMENTS_FILE") or None
ICON_FILE = "AppIcon.icns"

INFO_PLIST = {
    "CFBundleDisplayName": APP_NAME,
    "CFBundleName": APP_NAME,
    "CFBundleShortVersionString": APP_VERSION,
    "CFBundleVersion": BUILD_NUMBER,
    "LSMinimumSystemVersion": MIN_MACOS,
    "LSApplicationCategoryType": APP_CATEGORY,
    "NSHighResolutionCapable": True,
    "NSHumanReadableCopyright": "Copyright 2026 Socranotes. All rights reserved.",
}

datas = []
binaries = []
hiddenimports = []
tmp_ret = collect_all('edge_tts')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['AudioGenerator.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=TARGET_ARCH,
    codesign_identity=CODE_SIGN_IDENTITY,
    entitlements_file=ENTITLEMENTS_FILE,
    icon=[ICON_FILE],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)
app = BUNDLE(
    coll,
    name=f"{APP_NAME}.app",
    icon=ICON_FILE,
    bundle_identifier=BUNDLE_ID,
    info_plist=INFO_PLIST,
)

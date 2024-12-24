# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import tkinterdnd2

# Get tkdnd library path
tkdnd_path = os.path.join(os.path.dirname(tkinterdnd2.__file__), 'tkdnd')

block_cipher = None

a = Analysis(
    ['audio_converter.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('bin/ffmpeg/ffmpeg.exe', 'bin/ffmpeg'),
        ('bin/qaac/qaac64.exe', 'bin/qaac'),
        ('bin/qaac/QTfiles/*', 'bin/qaac/QTfiles'),
        (tkdnd_path, 'tkinterdnd2/tkdnd'),
    ],
    hiddenimports=['tkinterdnd2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AudioConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
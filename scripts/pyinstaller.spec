# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

project_dir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))

a = Analysis(
    [os.path.join(project_dir, 'src', 'main.py')],
    pathex=[os.path.join(project_dir, 'src')],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{{{PROJECT-NAME}}}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{{{PROJECT-NAME}}}',
)
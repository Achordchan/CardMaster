# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['card-master-gui.py'],
    pathex=[],
    binaries=[('C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python310\\DLLs\\tcl86t.dll', '.'), ('C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python310\\DLLs\\tk86t.dll', '.')],
    datas=[('config', 'config')],
    hiddenimports=['keyboard', 'pyautogui', 'tkinter', 'json'],
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
    a.binaries,
    a.datas,
    [],
    name='CardMaster',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
)

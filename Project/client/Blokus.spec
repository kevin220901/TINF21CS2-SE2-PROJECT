# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('C:/Users/info/Documents/GitHub/TINF21CS2-SE2-PROJECT/Project/client/account', 'account/'), ('C:/Users/info/Documents/GitHub/TINF21CS2-SE2-PROJECT/Project/client/game', 'game/'), ('C:/Users/info/Documents/GitHub/TINF21CS2-SE2-PROJECT/Project/client/lobby', 'lobby/'), ('C:/Users/info/Documents/GitHub/TINF21CS2-SE2-PROJECT/Project/client/network', 'network/'), ('C:/Users/info/Documents/GitHub/TINF21CS2-SE2-PROJECT/Project/client/jinglebells.mp3', '.'), ('C:/Users/info/Documents/GitHub/TINF21CS2-SE2-PROJECT/Project/client/main.py', '.'), ('C:/Users/info/Documents/GitHub/TINF21CS2-SE2-PROJECT/Project/client/menu.py', '.'), ('C:/Users/info/Documents/GitHub/TINF21CS2-SE2-PROJECT/Project/client/never_gonna_give_you_up.MP3', '.'), ('C:/Users/info/Documents/GitHub/TINF21CS2-SE2-PROJECT/Project/client/qt6networkadapter.py', '.'), ('C:/Users/info/Documents/GitHub/TINF21CS2-SE2-PROJECT/Project/client/requirements.txt', '.'), ('C:/Users/info/Documents/GitHub/TINF21CS2-SE2-PROJECT/Project/client/settings.py', '.')]
binaries = []
hiddenimports = []
tmp_ret = collect_all('PyQt6')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('json')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('queue')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('threading')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('typing')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('numpy')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('functools')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('datetime')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('logging')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('sys')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('contextvars')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['C:/Users/info/Documents/GitHub/TINF21CS2-SE2-PROJECT/Project/client/main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Blokus',
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
)

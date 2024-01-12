# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['DanmakuReader.py','dr_window.py','initial.py','iosetting.py','liveget.py','reader.py', 'global_setting.py',
    './ui/danmakureaderwindow.py','./ui/launchwindow.py','./ui/login_qrcode.py','./ui/loginwindow.py',
    './ui/updatecontent.py', './ui/settingswindow.py','./funcs/file_func.py','./funcs/launch_func.py',
    './funcs/login_func.py'],
    pathex=[],
    binaries=[],
    datas=[('README.md', '.'),('v1.2-alpha.md','.')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='DanmakuReader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DanmakuReader',
)

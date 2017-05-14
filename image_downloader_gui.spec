# -*- mode: python -*-

block_cipher = None


a = Analysis(['image_downloader_gui.py'],
             pathex=['./'],
             binaries=None,
             datas=[("bin/phantomjs.exe", "bin/")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='image_downloader_gui',
          debug=False,
          strip=False,
          upx=True,
          console=True )

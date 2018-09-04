# -*- mode: python -*-

block_cipher = None


a = Analysis(['plankton_toolbox_start.py'],
             pathex=['D:\\Arnold\\11a_plankton_toolbox_py3qt5\\w_ptbx\\plankton-toolbox'],
             binaries=[],
             datas=[],
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
          name='plankton_toolbox_start',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='img\\plankton_toolbox_icon.ico')

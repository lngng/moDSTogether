pyinstaller -n="rtools" --noconfirm ^
--icon="./icon.ico" ^
--add-data="./config.json;./" ^
--onefile ^
rtools.py
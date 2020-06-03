pyinstaller -n="debug-panel" --noconfirm ^
    --icon="./icon.ico" ^
    --add-data="./config.json;./" ^
    --onefile ^
    panel.py


echo "Bundling config.json and temp  with executable..."
copy config.json dist
copy temp dist

echo "Moving bundle..."
move dist\debug-panel.exe ..\
move dist\config.json ..\
move dist\temp ..\


echo "Cleaning up build artifacts..."
del debug-panel.spec
rmdir /s /q build
rmdir /s /q __pycache__
rmdir /s /q dist



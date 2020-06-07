pyinstaller -n="modops" --noconfirm ^
    --icon="./icon.ico" ^
    --add-data="./config.json;./" ^
    --onefile ^
    modops.py


echo "Bundling config.json and temp  with executable..."
copy config.json dist
copy temp dist

echo "Moving bundle..."
move dist\modops.exe ..\
move dist\config.json ..\
move dist\temp ..\


echo "Cleaning up build artifacts..."
del modops.spec
rmdir /s /q build
rmdir /s /q __pycache__
rmdir /s /q dist



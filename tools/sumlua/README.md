# sumlua

A simple tool that summarizes the functions in a given .lua file. Outputs to *.csv for viewing as a spreadsheet.

## Usage:

### Read luafile.lua and output to directory where the command is being run from (note the dot):
```
python sumlua.py C:\luafile.lua .
```
- C:\luafile.lua **-->** C:\luafile.csv
### Read luafile.lua and output to specific directory:
```
python sumlua.py C:\luafile.lua C:\users\me\desktop
```
- C:\luafile.lua **-->** C:\users\me\desktop\luafile.csv


## Patchnotes

v0.1 Initial Release
- outputs: name, parameters, scope as columns
- not tested extensively

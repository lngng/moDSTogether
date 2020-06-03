# Debug Panel
A suite of tools for rapid deployment/debugging of Don't Starve Together mods.


![Debug Panel](/docs/tools/debug-panel.png)
* * *
  
## Sample Configuration

```json
{
    "env": {
        "game": "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Don't Starve Together",
        "game_steamcmd": "C:\\steamcmd\\steamapps\\common\\Don't Starve Together Dedicated Server",
        "game_local": "C:\\Users\\ryanr\\Documents\\Klei\\DoNotStarveTogether\\4709694"
    },
    "mod": {
        "mod_name": "my-mod",
        "mod_path": "C:\\Users\\ryanr\\source\\moDSTogether\\mod",
        "partial_install_patterns": [
            "modinfo.lua",
            "modmain.lua",
            "prefabs/myprefab.lua"
        ],
        "ignore": [
            "external"
        ]
    }
}
```

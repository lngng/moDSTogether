import shutil, os, pathlib


def get_mod_dir():
    MOD_DIR_SEGMENT = "Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods"
    cwd = str(pathlib.Path.cwd())
    current_drive = cwd[:3]
    mod_dir = current_drive + MOD_DIR_SEGMENT
    while not os.path.exists(mod_dir):
        mod_dir = input("Path to mods not not found at [" + mod_dir + "] Please enter the correct path: ")
    return mod_dir

if __name__ == "__main__":
    dst_mods = get_mod_dir()
    mod_dir_list = os.listdir(dst_mods)

    for member in mod_dir_list:
        path = os.path.join(dst_mods, member)
        if os.path.isdir(path) and ".zip" not in path:
            info_path = os.path.join(path, 'modinfo.lua')
            if os.path.isfile(info_path):
                with open(os.path.normpath(info_path), encoding='utf-8') as item:
                    for line in item:
                        if "name=" in line or "name =" in line:
                            workshop_id = os.path.basename(member)
                            name = line.split("=")[1]
                            print(name + workshop_id + "\n")
                            break
                        
    input("> Press any key to exit: ")

                    

                    
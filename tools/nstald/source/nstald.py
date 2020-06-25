import shutil, os, pathlib, sys


def get_mod_dir():
    MOD_DIR_SEGMENT = r"Program Files (x86)\Steam\steamapps\common\Don't Starve Together\mods"
    cwd = str(pathlib.Path.cwd())
    current_drive = cwd[:3]
    mod_dir = current_drive + MOD_DIR_SEGMENT
    while not os.path.exists(mod_dir):
        mod_dir = input("Path to mods not not found at [" + mod_dir + "] Please enter the correct path: ")
    return mod_dir


def get_installed_mods() -> dict:
    dst_mods = get_mod_dir()
    mod_dir_list = os.listdir(dst_mods)
    mods = {}
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
                            name = (name.replace('"', "")).strip()
                            workshop_id = workshop_id.strip()
                            mods[name] = workshop_id
                            break
    return mods                        


if __name__ == "__main__":
    mods = get_installed_mods()
    for name, workshop_id in mods.items():
        print(name + '\n' + workshop_id + '\n')
                        
    input("> Press any key to exit: ")
    sys.exit()

                    

                    
import os
import shutil
import sys
import json
import subprocess
import pathlib

CWD = os.getcwd()

TOOL_ENVIRONMENT = {
    0 : "STANDALONE",
    1 : "MODSTOGETHER"
}

def write_file(file, text):
    """Writes text to file. Returns -1 on failure."""
    try:
        with open(file, "w") as f:
            f.write(text)
            f.close()
    except:
        return -1


def read_file(file):
    """Reads (file), returns text as a string. Returns -1 on failure."""
    
    text = str()
    try:
        with open(file, 'r') as f:
            text = str(f.read())
            f.close()
        return text
    except:
        return -1


def replace_element_name(file_text:str, new_name):
    """Replaces element names in xml files in accordance with DST autocompiler requirements"""
    
    start = file_text.find('<Element name=') + len('<Element name=') + 1    
    end = file_text.find('"', start)    

    existing_name = file_text[start:end]
    new_file_text = file_text.replace('<Element name="' + existing_name + '"', '<Element name="' + new_name + '"')
    
    msg = 'Replacing %s with %s' % (existing_name, new_name)
    print(msg)

    return new_file_text


def install_file(src, dest):
    print('> Installing ' + src + ' -> ' + dest)
    try:
        if os.path.isfile(dest):
            os.unlink(dest)
        shutil.copyfile(src, dest)
    except Exception as e:
        print('> Installing ' + src + ' -> ' + dest + ' failed with error: ' + str(e))


class Config:

    def __init__(self, path):
        self.path = path
        self.initialize_settings()

    def _get(self, section, key=None):
        """Gets specified section and key. Key is optional."""
        with open(self.path) as json_config_file:
            config = json.load(json_config_file)
            config_section = config[section]
            if key:
                return config_section[key]
            return config_section

    def _set(self, section, key, value):
        """Sets specified key."""
        config = None
        with open(self.path) as json_config_file:
            config = json.load(json_config_file)
            config[section][key] = value
        with open(self.path, "w") as json_config_file:
            json.dump(config, json_config_file, indent=4)
    
    def is_packaged(self):
        script_directory_path = pathlib.Path(__file__).parent.absolute()
        flag_path = os.path.join(script_directory_path, "PACKAGE_FLAG")
        if os.path.exists(flag_path):
            return True

    def initialize_settings(self):
        _game = self.game
        self.resolve_message("game", _game, os.path.exists(_game))

        _steamcmd_mods = self.steamcmd_mods #TODO: change to steamcmd_game
        self.resolve_message("steamcmd_mods", _steamcmd_mods, os.path.exists(_steamcmd_mods))

        _game_local = os.path.join(self.current_user, "Documents/Klei/DoNotStarveTogether/4709694")
        self.resolve_message("game_local", _game_local, os.path.exists(_game_local))
        
        _mod_path = self.mod_path
        _mod_name = self.mod_name
        if self.is_packaged():
            if self.mod_name == "UNSET":
                usr_input = input("moDSTogether package detected. Please enter a name for your mod. This name will be used as a directory name for debug installs: ")
                if usr_input != "" and not (("/") in usr_input) and not(('\\') in usr_input): 
                    _mod_name = usr_input
                    _mod_path = os.path.abspath(os.path.join("./", "./", "mod"))
                    self._set("mod", "mod_path", _mod_path)
                    self._set("mod", "mod_name", _mod_name)
        self.resolve_message("mod_path", _mod_path, os.path.exists(_mod_path))
        self.resolve_message("mod_name", _mod_name, True)

        
    def resolve_message(self, key, value, isOk):
        if isOk:
            print("[OK]: config <" + key + "> using : " + value)
        else:
            print("[WARNING]: could not resolve config <" + key + ">, please update configuration manually. EXPECTED: " + value)

    # Defined
    @property
    def game(self):
        """Defined local directory where Don't Starve Together is installed."""
        return self._get('env', 'game')
    
    @property
    def game_local(self):
        """Defined local game directory."""
        return self._get('env', 'game_local')

    @property
    def steamcmd_mods(self):
        """Defined Local directory where steamcmd DST mods are stored."""
        return self._get('env', 'steamcmd_mods')

    @property
    def mod_name(self):
        """Defined name of mod."""
        return self._get('mod', 'mod_name')
    
    @property
    def mod_path(self):
        """Defined path of mod directory."""
        return self._get('mod', 'mod_path')

    @property
    def partial_install_patterns(self):
        """Defined patterns to be included for rapid development installs."""
        return self._get('mod', 'partial_install_files')

    @property
    def ignore(self):
        """Defined patterns to be ignored for all installs."""
        return self._get('mod', 'ignore')

    @property
    def debug_world(self):
        return self._get('mod', 'debug_world')
    #Resolved
    @property
    def current_user(self):
        return os.path.expanduser('~')
    
    @property
    def target_mod_dir_steam(self):
        """Resolved destination directory for Steam installs."""
        mod_dir = os.path.join(self.game, "mods") 
        return os.path.join(mod_dir, self.mod_name)

    @property
    def target_mod_dir_steamcmd(self):
        """Resolved destination directory for SteamCMD installs."""
        return os.path.join(self.steamcmd_mods, self.mod_name)
    
    @property
    def cache_dir_steam(self):
        """Resolved Steam mod cache directory."""
        return os.path.join(self.game, "cached_mods")

    @property
    def cache_dir_steamcmd(self):
        """Resolved SteamCMD mod cache directory."""
        return os.path.join(self.game, "cached_mods")

    @property
    def game_executable(self):
        """Resolved dontstarve_steam.exe path."""
        return os.path.join(self.game, 'bin', 'dontstarve_steam.exe')

    @property
    def autocompiler(self):
        """Resolved Don't Starve Together autocompiler full path."""
        return os.path.join(self.game, "..", "Don't Starve Mod Tools", "mod_tools", "autocompiler.exe")
      
class App:
    def __init__(self):
        self.config = Config(os.path.join(pathlib.Path(__file__).parent.absolute(), "config.json"))
        self.main_menu_options = {
            '0' : ([self.clear_cache, self.clear_existing_mod_installation, self.install_mod], "Normal (Clear cache, clear existing installation, install from current branch)"),
            '1' : ([self.clear_cache], "Clear cache"),
            '2' : ([self.clear_existing_mod_installation], "Clear existing installation"),
            '3' : ([self.install_mod], "Install from working directory"),
            '4' : ([self.run_autocompiler], "Run autocompiler"),
            '5' : ([self.compile_working_anims], "Compile working anims"),
            '6' : ([self.update_bigportraits_xml], "Update xml files (bigportraits)"),
            '7' : ([self.partial_install], "Partial install"),
            '8' : ([self.refresh_cluster], "Refresh cluster..."),
            '9' : ([self.launch_game], "Launch Don't Starve Together"),
            'c' : ([self.edit_config], "Edit config"),
            'q' : ([self.quit_app], "Quit")
        }

    def main(self):
        while True:
            print("""
            ////////////////////////
            //RYANS MOD TOOL v0.1//
            //////////////////////
            """)

            for key, tup in self.main_menu_options.items():
                print('[' + key + '] ' + tup[1])
                
            user_option_selection = input("\n> Choose an option [0-9]:\n")
            if user_option_selection not in self.main_menu_options.keys():
                print("\nInvalid option!")
                next
            else:
                functions_to_call = self.main_menu_options[user_option_selection][0]
                for func in functions_to_call:
                    func()
        
    def update_bigportraits_xml(self):
        """Updates bigportraits xml files in WORKING directory using current config and DST autocompiler v1.2.4 specs"""
        
        char = input("Character name: ")
        target_mod_dir = self.config.target_mod_dir_steam

        # bigportraits
        bigportrait_none = target_mod_dir + ("/bigportraits/%s_none.xml" % (char))
        text_bigportrait_none = read_file(bigportrait_none)
        new_text_bigportrait_none = replace_element_name(text_bigportrait_none, char + "_none_oval.tex")
        write_file(bigportrait_none, new_text_bigportrait_none)

    def update_names_xml(self):
        """Updates names xml files in WORKING directory using current config and DST autocompiler v1.2.4 specs"""

        char = input("Character name: ")
        target_mod_dir = self.config.target_mod_dir_steam

        # names
        names_nicole = target_mod_dir + "/images/names_nicole.xml"
        text_names = read_file(names_nicole)
        new_text_names = replace_element_name(text_names, char + ".tex")
        write_file(names_nicole, new_text_names)
        
        # names_gold
        names_gold_nicole = target_mod_dir + "/images/names_gold_nicole.xml"
        text_names_gold = read_file(names_gold_nicole)
        new_text_names_gold = replace_element_name(text_names_gold, char)
        write_file(names_gold_nicole, new_text_names_gold)

    def clear_cache(self):
        """Deletes all subdirectories & files found in DST mod CACHE directory"""
        print("\n> Clearing cache...")
        cache_dir = self.config.cache_dir_steam
        shutil.rmtree(cache_dir)
        os.mkdir(cache_dir)

    def clear_existing_mod_installation(self):
        """Deletes TARGET mod directory & steamcmd DST Dedicated Server mod folder"""

        print("\n> Clearing existing mod installation...")
        path = self.config.target_mod_dir_steam.replace("/", "\\")
        if not os.path.lexists(path):
            print("> No existing installation!")
        else:
            try:
                shutil.rmtree(path, ignore_errors=True)
                print("> REMOVED installation (" + path + ")")
            except Exception as e:
                print('Failed to remove %s. Reason: %s' % (path, e))
        
        print("\n> Clearing existing steamcmd mod installation...")
        path = self.config.target_mod_dir_steamcmd.replace("/", "\\")
        if not os.path.lexists(path):
            print("> No existing steamcmd installation!")
        else:
            try:
                shutil.rmtree(path, ignore_errors=True)
                print("> REMOVED steamcmd installation (" + path + ")")
            except Exception as e:
                print('Failed to remove %s. Reason: %s' % (path, e))

    def install_mod(self):
        """Copies WORKING mod directory to DST mod folder & steamcmd DST Dedicated Server mod folder"""

        # # Create temp build dir...
        build_dir_path = os.getcwd() + "/temp/"
        if os.path.isdir(build_dir_path):
            shutil.rmtree(build_dir_path)
            print("\n> Build directory cleared...")
        else:
            os.mkdir(build_dir_path)

        # Copy subdirs (except .git and .vscode into build folder)
        try:
            working_mod_dir = self.config.mod_path
            ignore_patterns = ['.git*', '.vscode']
            for pattern in self.config.ignore:
                ignore_patterns.append(pattern)
            shutil.copytree(working_mod_dir, build_dir_path, ignore=shutil.ignore_patterns(*ignore_patterns))
            print("> Build created successfully! ")
        except Exception as e:
            print('> Failed to populate build folder. Reason: ' + str(e))
        
        # Copy build contents to target mod dir
        mod_dir = self.config.target_mod_dir_steam
        try:
            shutil.copytree(build_dir_path, mod_dir)
            print("\n>Installation of build to target steam mod directory was successful!")
        except Exception as e:
            print(str(e))
        
        # Copy build contents to steamcmd mod dir
        steamcmd_mod_dir = self.config.target_mod_dir_steamcmd
        try:
            shutil.copytree(build_dir_path, steamcmd_mod_dir)
            print("> Installation of build to steamcmd mod directory was successful!")
        except Exception as e:
            print(str(e))

    def run_autocompiler(self):
        os.startfile(self.config.autocompiler)

    def refresh_cluster(self):
        user_input = input("> Enter the saveslot of the cluster you would like to refresh [1-5], or press enter to refresh '" + os.path.basename(self.config.debug_world) + "': ")

        if user_input.isnumeric() and (0 < int(user_input) <= 5):
            print("\n> Refreshing cluster %s..."%(str(user_input)))
            local_cluster_dir = self.config.game_local
            target_cluster_path = "%s/Cluster_%s"%(local_cluster_dir, str(user_input))
            target_cluster_master_save_path = "%s/master/save"%(target_cluster_path)
            target_cluster_caves_save_path = "%s/caves/save"%(target_cluster_path)
            for path in [target_cluster_master_save_path, target_cluster_caves_save_path]:
                print("> Attempting to delete %s..."%(path))
                try:
                    shutil.rmtree(path)
                except:
                    print("> %s not found."%(path))
                else:
                    print("> %s deleted."%(path))
            print("> Cluster %s successfully refreshed."%(str(user_input)))
        elif user_input == "":
            target_cluster_path = self.config.debug_world
            target_cluster_master_save_path = "%s/master/save"%(target_cluster_path)
            target_cluster_caves_save_path = "%s/caves/save"%(target_cluster_path)
            for path in [target_cluster_master_save_path, target_cluster_caves_save_path]:
                print("> Attempting to delete %s..."%(path))
                try:
                    shutil.rmtree(path)
                except:
                    print("> %s not found."%(path))
                else:
                    print("> %s deleted."%(path))
            print("> Cluster %s successfully refreshed."%(str(user_input)))
        else:
            print("> Invalid input. Returning to main menu.")

    def partial_install(self):
        print("\n> Performing partial install...")
        for file_ in self.config.partial_install_patterns:
            src = os.path.join(self.config.mod_path, file_)

            dest_steam = os.path.join(self.config.target_mod_dir_steam, file_)
            dest_steamcmd = os.path.join(self.config.target_mod_dir_steamcmd, file_)
            
            install_file(src, dest_steam)
            install_file(src, dest_steamcmd)

    def compile_working_anims(self):
        """Compiles exported directories to populate anim directory of working mod.
        """
        working_exported = os.path.join(self.config.mod_path, "exported")
        working_anim = os.path.join(self.config.mod_path, "anim")
        temp_exported = os.path.join(self.config.game, "mods", "_compile", "exported")
        temp_anim = os.path.join(self.config.game, "mods", "_compile", "anim")
        # Delete temp exported if it exists 
        if os.path.isdir(temp_exported):
            shutil.rmtree(temp_exported)
        # Delete temp anim if it exists 
        if os.path.isdir(temp_anim):
            shutil.rmtree(temp_anim)
        # Copy working exported to temp exported
        shutil.copytree(working_exported, temp_exported)
        # Run autocompiler
        subprocess.call([self.config.autocompiler])
        # Copy compiled anims back to working anim folder
        anims = os.listdir(temp_anim)
        if len(anims) > 0:
            for anim in anims:
                src_anim = os.path.join(temp_anim, anim)
                dst_anim = os.path.join(working_anim, anim)
                if os.path.exists(dst_anim):
                    if input("> WARNING: Overwrite " + anim + "? [y/n]: ") == "y":
                        os.unlink(dst_anim)
                    else:
                        print("> Skipping... " + anim)
                        next
                    shutil.copyfile(src_anim, dst_anim)
                    print("> Compiled... " + anim)  
        
    def launch_game(self):
        subprocess.Popen(self.config.game_executable)
        
    def edit_config(self):
        file = os.path.join(CWD, 'config.json')
        if sys.platform == 'linux2':
            subprocess.call(["xdg-open", file])
        else:
            os.startfile(file)
        
    def quit_app(self):
        quit()


if __name__ == "__main__":
    app = App()
    app.main()
import os
import shutil
import sys
import json
import subprocess
import pathlib

DEBUG = True

CWD = os.getcwd()
SCRIPT_PATH = str(pathlib.Path(__file__).parent.absolute())
PATHING_ERROR = "ERROR: Could not resolve path(s) with current config." #TODO: refactor for detailed error. custom exception or strict pathlib use

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


def uninstall_mod(path):
    if not os.path.lexists(path):
        return "OK: No existing installation."
    else:
        try:
            shutil.rmtree(path, ignore_errors=True)
            return "OK: Uninstalled " + path 
        except Exception as e:
            return 'ERROR: Failed to uninstall %s. Reason: %s' % (path, e)


class Config:
    def __init__(self, path):
        self.path = path


    def _get(self, section, key=None):
        """Gets specified section and key. Key is optional."""
        with open(os.path.join(pathlib.Path(__file__).parent.absolute(), "config.json")) as json_config_file:
            config = json.load(json_config_file)
            config_section = config[section]
            if key:
                return config_section[key]
            return config_section
    

    def is_packaged(self):
        script_directory_path = pathlib.Path(__file__).parent.absolute()
        flag_path = os.path.join(script_directory_path, "PACKAGE_FLAG")
        return os.path.exists(flag_path)
            

    def path_is_valid(self, path, must_contain_segments=None):
        exists = os.path.exists(path)
        if must_contain_segments and must_contain_segments != []:
            contains_segments = all(segment in path for segment in must_contain_segments)
            return exists and contains_segments
        return exists

#* Defined
    @property
    def game(self):
        """Defined local directory where Don't Starve Together is installed."""
        _game = self._get('env', 'game')
        if self.path_is_valid(_game, ["steamapps", "common","Don't Starve Together"]):
            return _game
    

    @property
    def game_local(self):
        """Defined local game directory."""
        _game_local = self._get('env', 'game_local')
        if self.path_is_valid(_game_local, ["Documents","Klei","DoNotStarveTogether"]) and os.path.basename(_game_local).isnumeric():
            return _game_local


    @property
    def game_steamcmd(self):
        """Defined Local directory where steamcmd DST mods are stored."""
        _game_steamcmd = self._get('env', 'game_steamcmd')
        if self.path_is_valid(_game_steamcmd, ["steamcmd","steamapps","Don't Starve Together Dedicated Server"]):
            return _game_steamcmd

    @property
    def mod_name(self):
        """Defined name of mod."""
        _mod_name = self._get('mod', 'mod_name')
        return _mod_name

    @property
    def mod_path(self):
        """Defined path of mod directory."""
        _mod_path = self._get('mod', 'mod_path')
        if self.path_is_valid(_mod_path):
            return _mod_path

    @property
    def partial_install_patterns(self):
        """Defined patterns to be included for rapid development installs."""
        return self._get('mod', 'partial_install_patterns')


    @property
    def ignore(self):
        """Defined patterns to be ignored for all installs."""
        return self._get('mod', 'ignore')


    @property
    def debug_world(self):
        return self._get('mod', 'debug_world')

#* Resolved
    @property
    def current_user(self):
        return os.path.expanduser('~')
    
    @property
    def target_mod_steam(self):
        """Resolved destination directory for Steam installs."""
        _game = self.game
        if _game:
            mod_dir = os.path.join(_game, "mods") 
            return os.path.join(mod_dir, self.mod_name)

    @property
    def target_mod_steamcmd(self):
        """Resolved destination directory for SteamCMD installs."""
        if self.game_steamcmd:
            mod_dir = os.path.join(self.game_steamcmd, "mods") 
            return os.path.join(mod_dir, self.mod_name)
    
    @property
    def cache_dir_steam(self):
        """Resolved Steam mod cache directory."""
        if self.game:
            return os.path.join(self.game, "cached_mods")

    @property
    def cache_dir_steamcmd(self):
        """Resolved SteamCMD mod cache directory."""
        if self.game:
            return os.path.join(self.game, "cached_mods")

    @property
    def game_executable(self):
        """Resolved dontstarve_steam.exe path."""
        if self.game:
            return os.path.join(self.game, 'bin', 'dontstarve_steam.exe')

    @property
    def autocompiler(self):
        """Resolved Don't Starve Together autocompiler full path."""
        auto = os.path.join(pathlib.Path(self.game).parent.absolute(), "Don't Starve Mod Tools", "mod_tools", "autocompiler.exe")
        if self.path_is_valid(auto):
            return auto
      

class App:
    def __init__(self):
        self.config = Config("config.json")
        self.main_menu_options = {
            '0' : ([self.clear_cache, self.clear_existing_mod_installation, self.install_mod], "Normal (Clear cache, clear existing installation, install from current branch)"),
            '1' : ([self.clear_cache], "Clear cache"),
            '2' : ([self.clear_existing_mod_installation], "Clear existing installation"),
            '3' : ([self.install_mod], "Install from working directory"),
            '4' : ([self.run_autocompiler], "Run autocompiler"),
            '5' : ([self.compile_working_anims], "Compile working anims"),
            '6' : ([self.partial_install], "Partial install"),
            '7' : ([self.refresh_cluster], "Refresh cluster..."),
            '8' : ([self.launch_game], "Launch Don't Starve Together"),
            '9' : ([self.edit_config], "Edit config"),
            'q' : ([self.quit_app], "Quit")
        }

    def main(self):
        while True:
            print("""
            /////////////////////
            //DEBUG PANEL v0.1//
            ///////////////////
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

    def clear_cache(self):
        """Deletes all subdirectories & files found in DST mod CACHE directory"""
        status = "> Clearing cache..."
        cache_dir = self.config.cache_dir_steam
        if cache_dir:
            try:
                shutil.rmtree(cache_dir)
                os.mkdir(cache_dir)
                status += " SUCCESS."
            except Exception as e:
                status += " ERROR: " + str(e)
        else:
            status += "ERROR: Could not resolve path(s) with current config."
        print(status)

                
    def clear_existing_mod_installation(self):
        """Deletes mod from steam DST mod folder & steamcmd DST Dedicated Server mod folder.
        """
        
        status = "\n> Clearing existing mod installation (steam)..."
        target_mod_steam = self.config.target_mod_steam
        if target_mod_steam:
            print(status + uninstall_mod(target_mod_steam))
        else:
            print(status + "ERROR: Could not resolve path(s) with current config.")

        status = "\n> Clearing existing steamcmd mod installation (steamcmd)..."
        target_mod_steamcmd = self.config.target_mod_steamcmd
        if target_mod_steamcmd:
            print(status + uninstall_mod(target_mod_steamcmd))
        else:
            print(status + " ERROR: Could not resolve path(s) with current config.")
            

    def install_mod(self):
        """Copies WORKING mod directory to DST mod folder & steamcmd DST Dedicated Server mod folder"""
        status = "\n> Installing mod..."
        mod_name = self.config.mod_name
        if not mod_name:
            print(status + " FAILED: Mod name improperly supplied/resolved.")
            return
        
        status += "[%s]"%(mod_name) 
        build_dir_path = pathlib.Path(os.path.join(SCRIPT_PATH + "\\temp"))
        if os.path.isdir(build_dir_path):
            shutil.rmtree(build_dir_path)
            print(status + " OK: Build directory cleared.")
        else:
            os.mkdir(build_dir_path)
            print(status + " OK: Build directory created.")

        mod_path = self.config.mod_path
        if not mod_path:
            print(status + PATHING_ERROR)
        try:
            ignore_patterns = ['.git*', '.vscode']
            if self.config.ignore:
                for pattern in self.config.ignore:
                    ignore_patterns.append(pattern)
            shutil.copytree(mod_path, build_dir_path, ignore=shutil.ignore_patterns(*ignore_patterns))
            print(status + " OK: Build populated.")
        except Exception as e:
            print(status + " FAILED: could not populate build folder. Reason: " + str(e))
        
        target_mod_steam = self.config.target_mod_steam
        if not target_mod_steam:
            print(status + PATHING_ERROR)
        try:
            shutil.copytree(build_dir_path, target_mod_steam)
            print(status + " SUCCESS: Installation (steam) complete.")
        except Exception as e:
            print(str(e))
        
        steamcmd_mod_dir = self.config.target_mod_steamcmd
        if not steamcmd_mod_dir:
            print(status + PATHING_ERROR)
        try:
            shutil.copytree(build_dir_path, steamcmd_mod_dir)
            print(status + " SUCCESS: Installation (steamcmd) complete.")
        except Exception as e:
            print(str(e))


    def run_autocompiler(self):
        status = "\n> Running autocompiler..."
        compiler = self.config.autocompiler
        if not compiler:
            print(PATHING_ERROR)
        os.startfile(compiler)
        print(status + "OK Successfully ran autocompiler.")


    def refresh_cluster(self):
        status = "> Refreshing cluster... "
        game_local = self.config.game_local
        if not game_local:
            print(status + PATHING_ERROR)

        user_input = input("> Enter the saveslot of the cluster you would like to refresh [1-5]")
        if user_input.isnumeric() and (0 < int(user_input) <= 5):
            print(status + (str(user_input)))
            cluster_path = "%s/Cluster_%s"%(game_local, str(user_input))
            master_save_path = "%s/master/save"%(cluster_path)
            caves_save_path = "%s/caves/save"%(cluster_path)
            for path in [master_save_path, caves_save_path]:
                try:
                    shutil.rmtree(path)
                except:
                    print(status + (str(user_input)) + ": OK %s not found."%(path))
                else:
                    print(status + (str(user_input)) + ": OK %s deleted."%(path))
            print(status + (str(user_input)) + ": OK Successfully refreshed.")


    def partial_install(self):
        print("\n> Performing partial install...")
        for file_ in self.config.partial_install_patterns:
            src = os.path.join(self.config.mod_path, file_)

            dest_steam = os.path.join(self.config.target_mod_steam, file_)
            dest_steamcmd = os.path.join(self.config.target_mod_steamcmd, file_)
            
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
        file = os.path.join(pathlib.Path(__file__).parent.absolute(), 'config.json')
        if sys.platform == 'linux2':
            subprocess.call(["xdg-open", file])
        else:
            os.startfile(file)
        

    def quit_app(self):
        sys.exit()


if __name__ == "__main__":
    app = App()
    app.main()
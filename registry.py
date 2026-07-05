import winreg

class Registry:

    def __init__(self):
        #First create the registry in this path and by this all values
        self.key_path = 'SOFTWARE\LightAI'
        self.apps_paths = self.read_apps_registry()
        self.ai_name = self.read_light_ai_registry("AssistantName", "Light AI")
        self.ai_version = self.read_light_ai_registry("Version", "2.5-Alpha")
        self.ai_volume = int(self.read_light_ai_registry("VolumeLevel", "80"))

    def read_apps_registry(self):
        master_apps_dict = {}
    
        subkey_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"
        
        root_hives = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]
        
        for hive in root_hives:
            try:
                key = winreg.OpenKey(hive, subkey_path)
                total_subkeys = winreg.QueryInfoKey(key)[0]
                
                for i in range(total_subkeys):
                    try:
                        exe_name = winreg.EnumKey(key, i)
                        sub_key = winreg.OpenKey(key, exe_name)
                        absolute_path = winreg.QueryValue(sub_key, None)
                        
                        if absolute_path:
                            app_keyword = exe_name.lower().replace(".exe", "").strip()
                            master_apps_dict[app_keyword] = absolute_path.strip()
                    except Exception:
                        continue
                winreg.CloseKey(key)
            except Exception:
                continue
            
        return master_apps_dict
    
    def read_light_ai_registry(self, value_name, default):
        """Reads configuration properties securely from HKCU without admin blocks"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path)
            value, _ = winreg.QueryValueEx(key, value_name)
            winreg.CloseKey(key)
            return value
        except Exception:
            return default
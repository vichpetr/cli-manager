import os
import json
import subprocess
from pathlib import Path

class GeminiSkillManager:
    """Správce Gemini skillů, který automatizuje sběr dat a volání CLI."""

    def __init__(self, skills_root="skills"):
        self.base_path = Path(__file__).parent
        self.skills_path = self.base_path / skills_root
        
    def list_available_skills(self):
        """Vrátí seznam složek v adresáři skills, které obsahují config.json."""
        skills = []
        if not self.skills_path.exists():
            return skills
            
        for item in self.skills_path.iterdir():
            if item.is_dir() and (item / "config.json").exists():
                skills.append(item.name)
        return sorted(skills)

    def load_skill_config(self, skill_name):
        """Načte JSON konfiguraci daného skillu."""
        config_file = self.skills_path / skill_name / "config.json"
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config for {skill_name}: {e}")
            return None

    def run_wizard(self, config):
        """Interaktivní sběr dat na základě definice v config.json."""
        print(f"
--- Konfigurační průvodce pro {config.get('name', 'skill')} ---")
        user_data = {}
        
        params = config.get("parameters", {})
        for key, description in params.items():
            value = input(f"{description} ({key}): ").strip()
            user_data[key] = value
            
        return user_data

    def execute_gemini(self, skill_name, params):
        """Volání gemini CLI přes subprocess."""
        command = ["gemini"]
        
        for key, value in params.items():
            command.extend([f"--{key}", value])

        print(f"
Spouštím příkaz: {' '.join(command)}")
        
        try:
            result = subprocess.run(command, capture_output=False, text=True)
            if result.returncode == 0:
                print("
✅ Skill úspěšně spuštěn.")
            else:
                print(f"
❌ Chyba: Příkaz skončil s kódem {result.returncode}")
        except FileNotFoundError:
            print("
❌ Chyba: Příkaz 'gemini' nebyl nalezen.")
        except Exception as e:
            print(f"
❌ Neočekávaná chyba: {e}")

    def main_menu(self):
        """Hlavní rozhraní pro výběr skillu."""
        skills = self.list_available_skills()
        
        if not skills:
            print("
V adresáři /skills nebyly nalezeny žádné skilly s config.json.")
            return

        print("
Dostupné Gemini skilly:")
        for idx, skill in enumerate(skills, 1):
            print(f"{idx}. {skill}")

        try:
            choice = input("
Vyberte číslo skillu (nebo 'q' pro konec): ").strip().lower()
            if choice == 'q':
                return
            
            idx = int(choice) - 1
            if 0 <= idx < len(skills):
                selected = skills[idx]
                config = self.load_skill_config(selected)
                
                if config:
                    user_params = self.run_wizard(config)
                    self.execute_gemini(selected, user_params)
            else:
                print("Neplatná volba.")
        except ValueError:
            print("Prosím zadejte platné číslo.")

if __name__ == "__main__":
    manager = GeminiSkillManager()
    manager.main_menu()

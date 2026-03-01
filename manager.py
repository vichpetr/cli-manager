import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

class GeminiSkillManager:
    """Správce Gemini skillů se dvěma režimy: Modernizace a Nový Vývoj."""

    def __init__(self, local_skills_root="skills"):
        self.base_path = Path(__file__).parent
        self.local_skills_path = self.base_path / local_skills_root
        self.default_output_root = self.base_path / "output"
        self.external_paths = [
            Path(os.path.expanduser("~/.antigravity-awesome-skills")),
            Path(os.path.expanduser("~/my-gemini-skills/skills"))
        ]

    def find_skill_dir(self, skill_name):
        search_paths = [
            Path(os.path.expanduser(f"~/.antigravity-awesome-skills/{skill_name}")),
            Path(os.path.expanduser(f"~/my-gemini-skills/skills/{skill_name}")),
            self.local_skills_path / skill_name
        ]
        for p in search_paths:
            if p.exists() and p.is_dir(): return p
        return None

    def list_available_skills(self):
        skills = set()
        for path in self.external_paths + [self.local_skills_path]:
            if path.exists() and path.is_dir():
                for item in path.iterdir():
                    if item.is_dir() and (item / "config.json").exists():
                        # project-manager v menu schováme a nahradíme ho našimi dvěma procesy
                        if item.name != "project-manager":
                            skills.add(item.name)
        return sorted(list(skills))

    def load_skill_config(self, skill_dir):
        config_file = skill_dir / "config.json"
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Chyba při načítání konfigurace: {e}")
            return None

    def run_wizard(self, config):
        """Wizard s popisy parametrů v závorkách."""
        print(f"\n--- Konfigurační průvodce: {config.get('name', 'Skill')} ---")
        user_data = {}
        params = config.get("parameters", {})
        for key, description in params.items():
            value = input(f"{description} ({key}): ").strip()
            user_data[key] = value
        return user_data

    def execute_gemini_command(self, skill_dir, params, capture_output=False):
        """Volání Gemini CLI přes -p a -y pro automatizaci."""
        if not skill_dir: return None
        
        system_content = ""
        system_file = skill_dir / "system.md"
        if system_file.exists():
            with open(system_file, "r", encoding="utf-8") as f:
                system_content = f.read()

        full_prompt = f"### SYSTEM ROLE/INSTRUCTIONS ###\n{system_content}\n\n### TASK PARAMETERS ###\n"
        for key, value in params.items():
            full_prompt += f"{key}: {value}\n"

        command = ["gemini", "-y", "-p", full_prompt]
        
        if not capture_output:
            print(f"\n🚀 Spouštím: {skill_dir.name}...")
        
        try:
            result = subprocess.run(command, capture_output=capture_output, text=True)
            if capture_output: return result.stdout
            return result.returncode == 0
        except Exception as e:
            print(f"\n❌ Chyba při spuštění gemini CLI: {e}")
            return None

    def prepare_project_dir(self, name, custom_path=None):
        clean_name = name.replace('.', '_').replace(' ', '_').replace('/', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_base = Path(os.path.expanduser(custom_path)) if custom_path else self.default_output_root
        project_dir = output_base / f"{clean_name}_{timestamp}"
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir

    def run_modernization_pipeline(self, url, requirements, languages, custom_path=None):
        """Pipeline pro vylepšení existujícího webu (URL)."""
        project_dir = self.prepare_project_dir(urlparse(url if "://" in url else f"http://{url}").netloc or url, custom_path)
        print(f"\n🏗️ MODERNIZE: {url}\n📁 Cíl: {project_dir}")

        # 1. Analýza URL
        analysis = self.execute_gemini_command(self.find_skill_dir("web-analyzer"), {"url": url}, capture_output=True)
        # 2. Byznys Case
        business = self.execute_gemini_command(self.find_skill_dir("business-analyst"), {"url": url}, capture_output=True)
        # 3. Návrh & Stack
        modern_plan = self.execute_gemini_command(self.find_skill_dir("web-modernizer"), {"current_features": analysis, "business_goals": business}, capture_output=True)
        tech_stack = self.execute_gemini_command(self.find_skill_dir("tech-stack-advisor"), {"app_description": modern_plan}, capture_output=True)
        # 4. Kontrola
        seo = self.execute_gemini_command(self.find_skill_dir("seo-structure-check"), {"url_or_description": modern_plan}, capture_output=True)
        # 5. Obsah
        content = self.execute_gemini_command(self.find_skill_dir("content-writer"), {"topic_or_analysis": modern_plan, "target_languages": languages, "seo_keywords": seo}, capture_output=True)
        # 6. Kód
        self.execute_gemini_command(self.find_skill_dir("web-developer"), {"plan": modern_plan, "tech_stack": tech_stack, "constraints": content, "output_path": str(project_dir / "src")})
        
        print(f"\n✨ Modernizace dokončena: {project_dir}")

    def run_new_project_pipeline(self, name, description, languages, custom_path=None):
        """Pipeline pro nový projekt (Zelená louka)."""
        project_dir = self.prepare_project_dir(name, custom_path)
        print(f"\n🌱 NOVÝ VÝVOJ: {name}\n📁 Cíl: {project_dir}")

        # 1. Byznys Analýza nápadu
        business = self.execute_gemini_command(self.find_skill_dir("business-analyst"), {"market_context": description}, capture_output=True)
        # 2. Architektonický Návrh (místo modernizace)
        modern_plan = self.execute_gemini_command(self.find_skill_dir("web-modernizer"), {"current_features": f"ZADÁNÍ PRO NOVÝ WEB: {description}", "business_goals": business}, capture_output=True)
        # 3. Tech Stack
        tech_stack = self.execute_gemini_command(self.find_skill_dir("tech-stack-advisor"), {"app_description": modern_plan}, capture_output=True)
        # 4. SEO & Struktura
        seo = self.execute_gemini_command(self.find_skill_dir("seo-structure-check"), {"url_or_description": modern_plan}, capture_output=True)
        # 5. Tvorba obsahu
        content = self.execute_gemini_command(self.find_skill_dir("content-writer"), {"topic_or_analysis": modern_plan, "target_languages": languages, "seo_keywords": seo}, capture_output=True)
        # 6. Implementace
        self.execute_gemini_command(self.find_skill_dir("web-developer"), {"plan": modern_plan, "tech_stack": tech_stack, "constraints": content, "output_path": str(project_dir / "src")})
        
        print(f"\n✨ Nový projekt dokončen: {project_dir}")

    def main_menu(self):
        skills = self.list_available_skills()
        print("\n--- GEMINI SKILL MANAGER (Orchestrator v2) ---")
        print("M1. Modernizace existujícího webu (URL)")
        print("M2. Nový vývoj systému (Zelená louka)")
        for idx, skill in enumerate(skills, 1):
            print(f"{idx:2}. {skill}")

        choice = input("\nVolba: ").strip().upper()
        if choice == 'Q': return
        
        if choice == 'M1':
            url = input("Vstupní URL webu (url): ").strip()
            langs = input("Cílové jazyky (např. CZ, EN) (langs): ").strip()
            path = input("Výstupní cesta (optional) (out): ").strip()
            self.run_modernization_pipeline(url, "", langs, path or None)
        elif choice == 'M2':
            name = input("Název nového projektu (name): ").strip()
            desc = input("Popis systému a funkcí (description): ").strip()
            langs = input("Cílové jazyky (langs): ").strip()
            path = input("Výstupní cesta (optional) (out): ").strip()
            self.run_new_project_pipeline(name, desc, langs, path or None)
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(skills):
                skill = skills[idx]
                config = self.load_skill_config(self.find_skill_dir(skill))
                params = self.run_wizard(config)
                self.execute_gemini_command(self.find_skill_dir(skill), params)

if __name__ == "__main__":
    manager = GeminiSkillManager()
    manager.main_menu()

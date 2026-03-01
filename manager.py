import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

class GeminiSkillManager:
    """Orchestrátor s inteligentní detekcí prázdného adresáře pro výstup."""

    def __init__(self, local_skills_root="skills"):
        self.base_path = Path(__file__).parent.resolve()
        self.local_skills_path = self.base_path / local_skills_root
        self.default_output_root = Path.cwd()
        
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

    def execute_gemini_command(self, skill_dir, params, capture_output=False):
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
            print(f"\n❌ Chyba při volání gemini CLI: {e}")
            return None

    def prepare_project_dir(self, name, custom_path=None):
        """Pokud je cílový adresář prázdný, použije ho přímo. Jinak vytvoří podsložku."""
        target_base = Path(os.path.expanduser(custom_path)) if custom_path else self.default_output_root
        target_base.mkdir(parents=True, exist_ok=True)

        # Kontrola, zda je adresář prázdný (ignorujeme skryté soubory jako .DS_Store nebo .git)
        is_empty = not any(item for item in target_base.iterdir() if not item.name.startswith('.'))

        if is_empty:
            print(f"✨ Cílový adresář je prázdný, používám: {target_base}")
            return target_base
        else:
            clean_name = name.replace('.', '_').replace(' ', '_').replace('/', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            project_dir = target_base / f"{clean_name}_{timestamp}"
            project_dir.mkdir(parents=True, exist_ok=True)
            print(f"📁 Adresář není prázdný, vytvářím podsložku: {project_dir}")
            return project_dir

    def run_modernization_pipeline(self, url, languages, custom_path=None):
        project_dir = self.prepare_project_dir(urlparse(url if "://" in url else f"http://{url}").netloc or url, custom_path)
        
        # Pipeline execution...
        analysis = self.execute_gemini_command(self.find_skill_dir("web-analyzer"), {"url": url}, capture_output=True)
        with open(project_dir / "01_analysis.md", "w") as f: f.write(analysis or "")
        
        business = self.execute_gemini_command(self.find_skill_dir("business-analyst"), {"url": url}, capture_output=True)
        with open(project_dir / "02_business.md", "w") as f: f.write(business or "")
        
        modern_plan = self.execute_gemini_command(self.find_skill_dir("web-modernizer"), {"current_features": analysis, "business_goals": business}, capture_output=True)
        tech_stack = self.execute_gemini_command(self.find_skill_dir("tech-stack-advisor"), {"app_description": modern_plan}, capture_output=True)
        with open(project_dir / "03_modernization_plan.md", "w") as f: f.write(modern_plan or "")
        
        ux = self.execute_gemini_command(self.find_skill_dir("ux-audit"), {"focus": modern_plan}, capture_output=True)
        seo = self.execute_gemini_command(self.find_skill_dir("seo-structure-check"), {"url_or_description": modern_plan}, capture_output=True)
        with open(project_dir / "04_audit_reports.md", "w") as f: f.write(f"UX: {ux}\n\nSEO: {seo}")
        
        content = self.execute_gemini_command(self.find_skill_dir("content-writer"), {"topic_or_analysis": modern_plan, "target_languages": languages, "seo_keywords": seo}, capture_output=True)
        with open(project_dir / "05_content.md", "w") as f: f.write(content or "")
        
        self.execute_gemini_command(self.find_skill_dir("web-developer"), {"plan": modern_plan, "tech_stack": tech_stack, "constraints": content, "output_path": str(project_dir / "src")})
        
        print(f"\n✨ Pipeline dokončena v: {project_dir}")

    def run_new_project_pipeline(self, name, description, languages, custom_path=None):
        project_dir = self.prepare_project_dir(name, custom_path)
        
        business = self.execute_gemini_command(self.find_skill_dir("business-analyst"), {"market_context": description}, capture_output=True)
        modern_plan = self.execute_gemini_command(self.find_skill_dir("web-modernizer"), {"current_features": description, "business_goals": business}, capture_output=True)
        tech_stack = self.execute_gemini_command(self.find_skill_dir("tech-stack-advisor"), {"app_description": modern_plan}, capture_output=True)
        seo = self.execute_gemini_command(self.find_skill_dir("seo-structure-check"), {"url_or_description": modern_plan}, capture_output=True)
        content = self.execute_gemini_command(self.find_skill_dir("content-writer"), {"topic_or_analysis": modern_plan, "target_languages": languages, "seo_keywords": seo}, capture_output=True)
        self.execute_gemini_command(self.find_skill_dir("web-developer"), {"plan": modern_plan, "tech_stack": tech_stack, "constraints": content, "output_path": str(project_dir / "src")})
        
        print(f"\n✨ Projekt dokončen v: {project_dir}")

    def handle_cli_args(self, args):
        mode = args[0].upper()
        if mode == "M1":
            if len(args) < 3:
                url = input("URL webu: ").strip()
                langs = input("Jazyky: ").strip()
                path = input(f"Cesta (Enter pro aktuální): ").strip()
                self.run_modernization_pipeline(url, langs, path or None)
            else:
                self.run_modernization_pipeline(args[1], args[2], args[3] if len(args) > 3 else None)
        elif mode == "M2":
            if len(args) < 4:
                name = input("Název: ").strip()
                desc = input("Popis: ").strip()
                langs = input("Jazyky: ").strip()
                path = input(f"Cesta (Enter pro aktuální): ").strip()
                self.run_new_project_pipeline(name, desc, langs, path or None)
            else:
                self.run_new_project_pipeline(args[1], args[2], args[3], args[4] if len(args) > 4 else None)
        else:
            skill_dir = self.find_skill_dir(mode)
            if skill_dir:
                config = self.load_skill_config(skill_dir)
                params = {k: input(f"{v} ({k}): ") for k, v in config.get("parameters", {}).items()}
                self.execute_gemini_command(skill_dir, params)

    def main_menu(self):
        skills = self.list_available_skills()
        print("\n--- GEMINI SKILL MANAGER (Orchestrator v2.1) ---")
        print(f"Aktuální adresář: {Path.cwd()}")
        print("-" * 45)
        print("M1. Modernizace existujícího webu (URL)")
        print("M2. Nový vývoj systému (Zelená louka)")
        for idx, skill in enumerate(skills, 1):
            print(f"{idx:2}. {skill}")

        try:
            choice = input("\nVolba (q pro konec): ").strip().upper()
            if choice == 'Q': return
            if choice == 'M1': self.handle_cli_args(["M1"])
            elif choice == 'M2': self.handle_cli_args(["M2"])
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(skills): self.handle_cli_args([skills[idx]])
            elif choice.lower() in [s.lower() for s in skills]:
                self.handle_cli_args([choice.lower()])
        except KeyboardInterrupt: pass

if __name__ == "__main__":
    manager = GeminiSkillManager()
    if len(sys.argv) > 1:
        manager.handle_cli_args(sys.argv[1:])
    else:
        manager.main_menu()

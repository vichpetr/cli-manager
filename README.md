# Gemini Skill Manager 🚀

Senior Orchestrátor pro modernizaci a vývoj webových aplikací pomocí Gemini CLI. Tento nástroj umožňuje automatizovat celý proces od byznys analýzy až po generování zdrojového kódu.

## 🛠 Instalace

Aby bylo možné manager spouštět z jakéhokoliv adresáře pod příkazem `gemini-manager`:

1.  Ujistěte se, že máte nainstalované `gemini` CLI.
2.  V adresáři projektu spusťte instalační skript (vyžaduje `sudo` pro vytvoření symlinku):
    ```bash
    chmod +x install.sh
    sudo ./install.sh
    ```

## 📋 Způsoby spuštění

### 1. Interaktivní menu (Wizard)
Stačí spustit příkaz bez parametrů. Zobrazí se menu s výběrem orchestrace nebo jednotlivých skillů.
```bash
gemini-manager
```

### 2. Rychlá orchestrace z CLI
Můžete spustit celý proces přímo s parametry:
- **Modernizace webu (URL):**
  ```bash
  gemini-manager M1 <url> <jazyky> [cílová_cesta]
  ```
- **Nový vývoj (Zelená louka):**
  ```bash
  gemini-manager M2 <název> <popis> <jazyky> [cílová_cesta]
  ```

### 3. Spuštění konkrétního skillu
```bash
gemini-manager ux-audit
```

## 📁 Inteligentní správa výstupů

- **Prázdný adresář:** Pokud spustíte `gemini-manager` v prázdné složce, veškeré výstupy (reporty a složka `src/`) se vytvoří **přímo v ní**.
- **Existující obsah:** Pokud adresář není prázdný, vytvoří se nová podsložka s názvem projektu a časovým razítkem, aby nedošlo k promíchání souborů.

## 🤖 Agent Team (Skills)

- **Business Analyst**: Průzkum majitele a ROI modernizace.
- **Web Analyzer**: Mapování funkcí stávajícího webu.
- **Tech Stack Advisor**: Výběr technologií pro rok 2026.
- **UX & Accessibility Audit**: Kontrola WCAG a UX best practices.
- **SEO Structure Check**: Sémantická analýza a meta tagy.
- **Content Writer**: Copywriting a multijazyčná lokalizace.
- **Web Developer**: Generování kódu včetně GA4 a Cookie Consent.

## 🏗 Rozšiřitelnost

Nové skilly přidáte vytvořením složky v `skills/` obsahující `config.json` (parametry) a `system.md` (instrukce).

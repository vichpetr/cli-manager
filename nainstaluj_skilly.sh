#!/bin/bash

# Zajištění existence složky skills
mkdir -p skills

# Inicializace git pokud ještě není (nebo reset)
if [ ! -d .git ]; then
    git init
fi

# Přidání souborů a první commit
git add .
git commit -m "Initial commit: Gemini Skill Manager"

echo "✅ Projekt úspěšně připraven v aktuálním adresáři."
echo "💡 Spusť 'python3 manager.py' pro výběr skillu."

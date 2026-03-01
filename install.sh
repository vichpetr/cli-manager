#!/bin/bash

# Zjištění absolutní cesty k adresáři, kde je manager.py
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_EXEC="$(which python3)"
INSTALL_NAME="gemini-manager"
BINARY_PATH="/usr/local/bin/$INSTALL_NAME"

echo "🚀 Instaluji Gemini Skill Manager jako $INSTALL_NAME..."

# Vytvoření wrapper skriptu v /usr/local/bin
cat <<EOF > "$INSTALL_NAME_TEMP"
#!/bin/bash
$PYTHON_EXEC "$PROJECT_DIR/manager.py" "\$@"
EOF

# Přesun do systému (vyžaduje sudo)
if [[ $EUID -ne 0 ]]; then
   echo "⚠️ Instalace vyžaduje sudo práva pro zápis do /usr/local/bin."
   sudo cp -f "$PROJECT_DIR/manager.py" "/usr/local/bin/gemini-manager-script.py"
   sudo bash -c "echo '#!/bin/bash' > $BINARY_PATH"
   sudo bash -c "echo '$PYTHON_EXEC $PROJECT_DIR/manager.py "\$@"' >> $BINARY_PATH"
   sudo chmod +x $BINARY_PATH
else
   echo "#!/bin/bash" > $BINARY_PATH
   echo "$PYTHON_EXEC $PROJECT_DIR/manager.py "\$@"" >> $BINARY_PATH
   chmod +x $BINARY_PATH
fi

echo "✅ Hotovo! Nyní můžete spustit 'gemini-manager' z jakéhokoliv adresáře."
echo "📁 Výchozí adresář pro výstup bude 'gemini_output/' v místě spuštění."

#!/bin/bash
# ============================================
# Script para gerar executavel com PyInstaller
# Para Linux/Mac
# ============================================

echo ""
echo "===================================="
echo "  GERANDO EXECUTAVEL"
echo "===================================="
echo ""

# Verificar se PyInstaller está instalado
if ! pip show pyinstaller > /dev/null 2>&1; then
    echo "[!] PyInstaller não encontrado. Instalando..."
    pip install pyinstaller
fi

# Caminho da pasta do config.json
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ORGANIZADOR_PATH="$SCRIPT_DIR/organizador"
CONFIG_PATH="$ORGANIZADOR_PATH/config.json"

echo "[+] Caminho do organizador: $ORGANIZADOR_PATH"
echo "[+] Caminho do config: $CONFIG_PATH"
echo ""

# Criar executavel
echo "[*] Gerando executável..."
pyinstaller --onefile \
  --console \
  --name organizador \
  --add-data "$CONFIG_PATH:organizador" \
  --distpath "./dist" \
  --buildpath "./build" \
  --specpath "./specs" \
  --noconfirm \
  -m organizador.cli

# Verificar resultado
if [ $? -ne 0 ]; then
    echo ""
    echo "[X] ERRO ao gerar executável!"
    exit 1
else
    echo ""
    echo "[✓] SUCESSO! Executável criado em: dist/organizador"
    echo ""
    echo "PRÓXIMOS PASSOS:"
    echo "1. Copie 'dist/organizador' para outro computador"
    echo "2. Dê permissão: chmod +x dist/organizador"
    echo "3. Execute: ./dist/organizador /caminho/dos/arquivos"
    echo "4. Use '--dry-run' para simular: ./dist/organizador /caminho --dry-run"
    echo ""
fi

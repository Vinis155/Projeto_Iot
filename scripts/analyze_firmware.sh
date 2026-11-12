#!/usr/bin/env bash
# Uso (na raiz do repositorio):  ./scripts/analyze_firmware.sh firmware/original/sketch.bin
# Preserva a imagem original, registra SHA-256 e gera saidas de analise em firmware/work/
set -u
ORIG="${1:?Informe o caminho do .bin original}"
OUT="firmware/work"
mkdir -p "$OUT"

NAME=$(basename "$ORIG")
SIZE=$(stat -c %s "$ORIG")
DATE=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
HASH=$(sha256sum "$ORIG" | awk '{print $1}')

# 1) Registro de integridade da imagem original
{
  echo "arquivo : $NAME"
  echo "tamanho : $SIZE bytes"
  echo "data    : $DATE"
  echo "origem  : (preencha: ex. Wokwi, F1 > Download firmware, link do projeto)"
  echo "sha256  : $HASH"
} > firmware/hashes.txt
chmod a-w "$ORIG"          # original somente leitura

# 2) Copia de trabalho + verificacao de que e identica
cp "$ORIG" "$OUT/$NAME"
HASH2=$(sha256sum "$OUT/$NAME" | awk '{print $1}')
if [ "$HASH" = "$HASH2" ]; then
  echo "copia_de_trabalho_sha256_confere : SIM" >> firmware/hashes.txt
else
  echo "copia_de_trabalho_sha256_confere : NAO (!)" >> firmware/hashes.txt
fi

# 3) Estrutura da imagem (esptool, se instalado: pip install esptool)
if command -v esptool >/dev/null 2>&1; then
  esptool image-info "$OUT/$NAME" > "$OUT/image_info.txt" 2>&1
elif command -v esptool.py >/dev/null 2>&1; then
  esptool.py image_info "$OUT/$NAME" > "$OUT/image_info.txt" 2>&1
else
  echo "esptool nao encontrado (pip install esptool)" > "$OUT/image_info.txt"
fi

# 4) Textos embutidos
strings -n 6 "$OUT/$NAME" > "$OUT/strings_all.txt"
grep -iE 'pass|user|mqtt|http://|https://|ssid|token|key|secret|\[DBG\]|\[OTA\]|ota|broker|nexa' \
  "$OUT/strings_all.txt" > "$OUT/strings_interesting.txt"

# 5) Estrutura/assinaturas (binwalk, se instalado)
if command -v binwalk >/dev/null 2>&1; then
  binwalk "$OUT/$NAME" > "$OUT/binwalk.txt" 2>&1
else
  echo "binwalk nao encontrado (opcional)" > "$OUT/binwalk.txt"
fi

echo "OK. Veja firmware/hashes.txt e firmware/work/"

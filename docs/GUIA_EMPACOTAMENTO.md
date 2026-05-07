# 📦 Guia de Empacotamento como Executável (.exe)

## O que é PyInstaller?
PyInstaller converte seu código Python em um executável que funciona em qualquer Windows, sem necessidade de ter Python instalado.

---

## 🎯 Passo a Passo para Gerar o .exe

### **Passo 1: Instalar PyInstaller**
```bash
pip install pyinstaller
```

### **Passo 2: Usar o Script de Build**

**No Windows, execute:**
```bash
.\build_exe.bat
```

Ou manualmente:
```bash
pyinstaller --onefile `
  --console `
  --name organizador `
  --add-data "organizador/config.json:organizador" `
  --distpath "./dist" `
  --buildpath "./build" `
  --specpath "./specs" `
  --noconfirm `
  -m organizador.cli
```

### **Passo 3: Resultado**
Após alguns segundos, você terá:
- `dist/organizador.exe` ← **Seu executável pronto para usar!**

---

## 📋 O que faz cada flag?

| Flag | Significado |
|------|-----------|
| `--onefile` | Cria um único arquivo .exe (em vez de pasta) |
| `--console` | Mantém janela de console para ver mensagens |
| `--name organizador` | Nome do executável gerado |
| `--add-data` | Inclui config.json dentro do .exe |
| `--distpath "./dist"` | Pasta onde o .exe será salvo |

---

## 🚀 Como Usar o .exe

### **No computador onde foi gerado:**
```bash
dist\organizador.exe C:\Users\User\Downloads
dist\organizador.exe C:\Users\User\Downloads --dry-run
dist\organizador.exe C:\Users\User\Downloads --verbose
```

### **Em outro computador:**
1. Copie apenas o arquivo `dist\organizador.exe`
2. Crie uma pasta chamada `organizador`
3. Coloque o .exe dentro dela
4. Execute:
   ```bash
   organizador.exe C:\caminho\dos\arquivos
   ```

---

## 📍 Localização do config.json

O `config.json` está **embutido** no .exe, então você não precisa copiar arquivo de configuração separadamente.

Se quiser usar um config customizado:
```bash
# Copiar config.json para a mesma pasta do .exe
organizador.exe C:\caminho\dos\arquivos --config config.json
```

---

## 🐛 Troubleshooting

### **Problema:** "PyInstaller não encontrado"
**Solução:** `pip install pyinstaller`

### **Problema:** ".exe não inicia"
**Solução:** Tente com `--console` para ver mensagens de erro

### **Problema:** Arquivo é muito grande
**Solução:** Isso é normal - Python + bibliotecas = ~50-100 MB

### **Problema:** Antivírus detecta como malware
**Solução:** É falso positivo. PyInstaller às vezes é detectado. Você pode adicionar à exceção do antivírus.

---

## 📊 Tamanho do Executável

Esperado: **~50-100 MB** (Python + bibliotecas)

Se quiser reduzir:
```bash
pyinstaller --onefile --console --name organizador \
  --add-data "organizador/config.json:organizador" \
  -m organizador.cli \
  --optimize 2
```

---

## 🔄 Atualizando o .exe

Se mudar o código:
1. Exclua as pastas `build/` e `dist/`
2. Execute `build_exe.bat` novamente
3. Novo .exe estará em `dist/organizador.exe`

---

## ✅ Checklist Final

- [ ] PyInstaller instalado
- [ ] Todos os testes passam
- [ ] Teste manual com `--dry-run` funciona
- [ ] Arquivo `build_exe.bat` está no diretório raiz
- [ ] Executou `build_exe.bat` com sucesso
- [ ] Novo .exe gerado em `dist/organizador.exe`
- [ ] Testou o .exe em outro diretório
- [ ] README atualizado com instruções

---

## 📝 Próximos Passos

1. **Gerar o .exe**: Execute `build_exe.bat`
2. **Testar localmente**: `dist\organizador.exe ./arquivos_teste --dry-run`
3. **Copiar para outro PC**: Copie `dist\organizador.exe`
4. **Distribuir**: Envie por email, coloque em pen drive, suba na nuvem, etc!

---

**Pronto! Seu executável está distribuível em qualquer Windows!** 🎉

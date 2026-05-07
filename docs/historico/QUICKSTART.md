# ⚡ Início Rápido - Organizador de Arquivos

Quer começar já? Aqui estão os 3 comandos essenciais:

---

## 🚀 Uso Rápido

```bash
# 1️⃣ SIMULAR (veja o que seria feito)
python -m organizador ./minha_pasta --dry-run

# 2️⃣ EXECUTAR (realmente organiza)
python -m organizador ./minha_pasta

# 3️⃣ MODO DETALHA (veja tudo que acontece)
python -m organizador ./minha_pasta --verbose
```

---

## 📂 Exemplo Real

Imagine que você tem uma pasta `Downloads` bagunçada:
```
Downloads/
├── foto.jpg
├── documento.pdf
├── musica.mp3
├── planilha.xlsx
└── video.mp4
```

**Execute:**
```bash
python -m organizador Downloads
```

**Resultado:**
```
Downloads/
├── Imagens/
│   └── foto.jpg
├── Documentos/
│   └── documento.pdf
├── Audio/
│   └── musica.mp3
├── Planilhas/
│   └── planilha.xlsx
└── Videos/
    └── video.mp4
```

---

## 🎯 Primeiros Passos

1. **Instale Python 3.8+** (se não tiver)
   - Windows: https://python.org
   - Mac: `brew install python3`
   - Linux: `sudo apt install python3`

2. **Coloque arquivos numa pasta**
   ```bash
   mkdir meus_arquivos
   # ... coloque arquivos nela ...
   ```

3. **Teste com --dry-run**
   ```bash
   python -m organizador ./meus_arquivos --dry-run
   ```

4. **Se estiver OK, execute de verdade**
   ```bash
   python -m organizador ./meus_arquivos
   ```

---

## ⚙️ Configurar Comportamento

Edite `organizador/config.json` para:
- Mudar categorias
- Adicionar extensões
- Alterar estratégia de duplicados

Exemplo:
```json
{
  "options": {
    "handle_duplicates": "skip"     // não copia duplicados
    // "handle_duplicates": "rename" // renomeia (padrão)
    // "handle_duplicates": "overwrite" // sobrescreve
  }
}
```

---

## 📊 Ver Resumo

Após cada execução, vê um resumo:
```
✅ Movidos: 45
📝 Renomeados: 3
⏭️  Pulados: 2
❌ Erros: 0
```

---

## 🐛 Algo deu errado?

1. **Verifique o log:**
   ```bash
   cat organizer.log
   ```

2. **Rode com --verbose:**
   ```bash
   python -m organizador ./pasta --verbose
   ```

3. **Sempre use --dry-run primeiro!**
   ```bash
   python -m organizador ./pasta --dry-run
   ```

---

## 📦 Gerar Executável (.exe)

Quer um arquivo .exe para levar em outro PC?

```bash
# Windows
.\build_exe.bat

# Mac/Linux
bash build_exe.sh
```

Depois, copie `dist/organizador.exe` para outro computador e use:
```bash
organizador.exe C:\Users\User\Downloads
```

**Sem precisar de Python instalado!**

---

## 📖 Mais Informações

- **Documentação completa:** Veja [README.md](README.md)
- **Como empacotar:** Veja [GUIA_EMPACOTAMENTO.md](GUIA_EMPACOTAMENTO.md)
- **Testar código:** `python -m unittest discover -s organizador/tests`

---

**Ficou fácil? Comece a organizar! 🎉**

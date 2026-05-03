# 🗂️ Automação de Organização de Arquivos em Python

Um sistema modular, robusto e pronto para produção que automatiza a organização de arquivos em pastas por tipo de extensão. Pode ser empacotado como executável (.exe) para usar em qualquer computador sem dependências Python.

## 📌 Características Principais

✅ **Arquitetura Modular** - Componentes bem separados: `config`, `organizer`, `cli`, `utils`  
✅ **Totalmente Configurável** - Arquivo `config.json` com categorias e extensões personalizáveis  
✅ **3 Estratégias de Duplicados** - Skip (pula), Rename (renomeia), Overwrite (sobrescreve)  
✅ **Sistema de Logging Robusto** - Logs em arquivo + console com níveis configuráveis  
✅ **Modo Simulação (Dry-Run)** - Teste operações sem realmente mover arquivos  
✅ **Modo Verbose** - Visualize todos os detalhes da execução  
✅ **Interface CLI Intuitiva** - Fácil de usar via linha de comando  
✅ **Cobertura de Testes** - Suite completa com testes unitários para todas as funcionalidades  
✅ **Empacotamento Executável** - Gera `.exe` pronto para usar em qualquer Windows  
✅ **Tratamento de Erros Completo** - Permissões, caminhos inválidos, caracteres especiais

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** - Linguagem base do projeto
- **Bibliotecas Padrão**: `pathlib`, `shutil`, `logging`, `argparse`, `json`, `re`
- **PyInstaller** - Empacotamento em executável (.exe)
- **Pytest/Unittest** - Testes automáticos

## 🚀 Como Usar

### **Opção 1: Executar como módulo Python**

```bash
# Uso básico
python -m organizador ./arquivos

# Com simulação (não move arquivos)
python -m organizador ./arquivos --dry-run

# Com detalhes (modo verbose)
python -m organizador ./arquivos --verbose

# Com simulação + detalhes
python -m organizador ./arquivos --dry-run --verbose

# Com arquivo config customizado
python -m organizador ./arquivos --config meu_config.json

# Ver versão
python -m organizador --version
```

### **Opção 2: Usar como executável (.exe)**

```bash
# Após gerar o .exe (ver seção "Empacotamento")
organizador.exe ./arquivos
organizador.exe ./arquivos --dry-run
organizador.exe ./arquivos --verbose
```

## 📖 Exemplos Práticos

### **Exemplo 1: Organizar pasta com simulação**

```bash
python -m organizador C:\Users\User\Downloads --dry-run
```

Resultado na tela:

```
[INFO] 🚀 Iniciando organização (modo: SIMULAÇÃO)
[INFO] 📁 Pasta de origem: C:\Users\User\Downloads
[INFO] ✅ Movido: photo.jpg → Imagens/
[INFO] ✅ Movido: documento.pdf → Documentos/
...
```

### **Exemplo 2: Organizar com modo detalhado**

```bash
python -m organizador C:\Users\User\Downloads --verbose
```

Resultado:

```
[DEBUG] Logger configurado em nível DEBUG
[INFO] 🚀 Iniciando organização (modo: NORMAL)
[DEBUG] 📂 Pasta criada: Imagens
[INFO] ✅ Movido: photo.jpg → Imagens/
[DEBUG] Arquivo processed successfully
...
```

### **Exemplo 3: Tratar duplicados com rename**

Editar `config.json`:

```json
{
  "options": {
    "handle_duplicates": "rename"
  }
}
```

Resultado ao organizar:

```
[INFO] ✅ Movido: photo.jpg → Imagens/
[INFO] 📝 Renomeado: photo.jpg → photo_1.jpg
[INFO] 📝 Renomeado: photo.jpg → photo_2.jpg
```

### **Exemplo 4: Usar estratégia overwrite**

```json
{
  "options": {
    "handle_duplicates": "overwrite"
  }
}
```

## 📁 Estrutura do Projeto

```
organizador/
├── __init__.py           # Inicialização do pacote
├── __main__.py           # Ponto de entrada (python -m organizador)
├── cli.py                # Interface de linha de comando
├── organizer.py          # Classe principal FileOrganizer
├── config.py             # Carregador de configuração
├── logger.py             # Sistema de logging
├── utils.py              # Funções auxiliares
├── config.json           # Arquivo de configuração
└── tests/
    ├── __init__.py
    └── test_organizer.py # Testes unitários (9 testes)

organizador.py           # Script legado (compatibilidade)
README.md               # Este arquivo
```

## ⚙️ Configuração (config.json)

O arquivo `config.json` controla o comportamento do programa:

```json
{
  "categories": {
    "Imagens": {
      "extensions": [".jpg", ".jpeg", ".png", ".gif"],
      "create_if_missing": true
    },
    "Documentos": {
      "extensions": [".pdf", ".txt", ".docx"],
      "create_if_missing": true
    },
    "Planilhas": {
      "extensions": [".xlsx", ".csv"],
      "create_if_missing": true
    }
  },
  "logging": {
    "enabled": true,
    "console_enabled": true,
    "level": "INFO",
    "log_file": "organizer.log"
  },
  "options": {
    "handle_duplicates": "rename",
    "preserve_source": false,
    "ask_on_overwrite": false
  }
}
```

### **Parâmetros Explicados**

| Parâmetro           | Valores                    | Descrição                           |
| ------------------- | -------------------------- | ----------------------------------- |
| `extensions`        | `[".jpg", ".png"]`         | Extensões que pertencen à categoria |
| `create_if_missing` | `true/false`               | Criar pasta se não existir          |
| `console_enabled`   | `true/false`               | Exibir logs no console              |
| `level`             | `DEBUG/INFO/WARNING/ERROR` | Nível de detalhe                    |
| `log_file`          | `"organizer.log"`          | Arquivo para salvar logs            |
| `handle_duplicates` | `skip/rename/overwrite`    | Estratégia para arquivos duplicados |

## 🧪 Executar Testes

```bash
# Rodar todos os testes
python -m unittest discover -s organizador/tests -p "test_*.py" -v

# Ou usando pytest (se instalado)
pytest organizador/tests/ -v

# Rodar um teste específico
python -m unittest organizador.tests.test_organizer.TestFileOrganizer.test_organize -v
```

**Testes Inclusos:**

1. ✅ Organizar arquivos básicos
2. ✅ Modo dry-run (simulação)
3. ✅ Duplicados - estratégia SKIP
4. ✅ Duplicados - estratégia RENAME
5. ✅ Duplicados - estratégia OVERWRITE
6. ✅ Tratamento de caminho inválido
7. ✅ Arquivo sem categoria
8. ✅ Contador de estatísticas
9. ✅ Extensões insensíveis a maiúsculas

## 📦 Empacotamento como Executável (.exe)

### **Passo 1: Instalar PyInstaller**

```bash
pip install pyinstaller
```

### **Passo 2: Gerar .exe (uma arquivo)**

```bash
pyinstaller --onefile --console --name organizador ^
  --add-data "organizador/config.json:organizador" ^
  --icon organizador/icon.ico ^
  -m organizador.cli
```

### **Passo 3: Usar o executável**

```bash
# No Windows
dist\organizador.exe C:\Users\User\Downloads --verbose

# Em outro computador, copie apenas a pasta dist/
```

**Resultado:**

- `dist/organizador.exe` - Executável pronto para usar
- Pode rodar em qualquer Windows (sem necessidade de Python instalado)

## 📊 Resumo de Execução

Ao rodar, você verá um resumo assim:

```
╔═══════════════════════════════════════════╗
║  📊 RESUMO DA ORGANIZAÇÃO                ║
╠═══════════════════════════════════════════╣
║  ✅ Movidos: 45                           ║
║  📝 Renomeados: 3                         ║
║  ⏭️  Pulados: 2                           ║
║  ❌ Erros: 0                              ║
╚═══════════════════════════════════════════╝
```

## 📝 Arquivo de Log

Um arquivo `organizer.log` é criado automaticamente:

```
26/04/2026 14:30:45 - organizador - INFO - 🚀 Iniciando organização (modo: NORMAL)
26/04/2026 14:30:45 - organizador - INFO - 📁 Pasta de origem: C:\Users\User\Downloads
26/04/2026 14:30:46 - organizador - INFO - ✅ Movido: photo.jpg → Imagens/
26/04/2026 14:30:46 - organizador - INFO - ✅ Movido: document.pdf → Documentos/
26/04/2026 14:30:47 - organizador - INFO - 📝 Renomeado: photo.jpg → photo_1.jpg
```

## 🔧 Customizações

### **Adicionar Nova Categoria**

Editar `config.json`:

```json
{
  "categories": {
    "Projetos": {
      "extensions": [".py", ".js", ".java", ".cpp"],
      "create_if_missing": true
    }
  }
}
```

### **Mudar Estratégia de Duplicados**

```json
{
  "options": {
    "handle_duplicates": "skip" // ou "rename", "overwrite"
  }
}
```

### **Aumentar Detalhes de Log**

```json
{
  "logging": {
    "level": "DEBUG"
  }
}
```

## 📝 Notas Importantes

⚠️ **Sempre faça um backup** antes de organizar pastas importantes  
⚠️ **Use `--dry-run` primeiro** para simular e validar  
⚠️ **Verifique o `organizer.log`** para detalhes de cada operação  
⚠️ **Extensões são case-insensitive** (`.PDF` e `.pdf` são iguais)

## 🐛 Troubleshooting

**Problema:** "Caminho não encontrado"  
**Solução:** Verifique se a pasta existe. Use caminho absoluto se necessário.

**Problema:** Arquivo não é movido  
**Solução:** Verifique `config.json` - a extensão pode não estar registrada.

**Problema:** Permissão negada ao mover arquivo  
**Solução:** Feche o arquivo em outro programa ou execute como administrador.

## 📧 Contato & Suporte

Para dúvidas ou bugs, verifique o arquivo `organizer.log` para detalhes completos.

---

**Versão:** 1.1.0  
**Última atualização:** 3 de maio de 2026  
**Status:** ✅ Pronto para produção

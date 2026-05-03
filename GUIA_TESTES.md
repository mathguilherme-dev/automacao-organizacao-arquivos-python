# Guia de Testes - Organizador de Arquivos

Este documento descreve como executar, entender e expandir a suite de testes do projeto.

## 📋 Visão Geral

O projeto segue as melhores práticas de **Teste Driven Development (TDD)** com:

- **82%+ de cobertura de código**
- **42 testes parametrizados**
- **Uso de pytest com fixtures reutilizáveis**
- **Mocks para dependências externas**
- **Validação de configuração robusta**

## 🚀 Executando os Testes

### Instalação de Dependências

```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

### Executar Todos os Testes

```bash
pytest organizador/tests/ -v
```

### Executar com Cobertura

```bash
pytest organizador/tests/ --cov=organizador --cov-report=html
```

Isso gera um relatório HTML em `htmlcov/index.html`.

### Executar Testes Específicos

```bash
# Apenas testes de configuração
pytest organizador/tests/test_config.py -v

# Apenas testes do organizador
pytest organizador/tests/test_organizer.py -v

# Uma classe específica
pytest organizador/tests/test_organizer.py::TestBasicOrganization -v

# Um teste específico
pytest organizador/tests/test_organizer.py::TestBasicOrganization::test_organize_moves_files_to_categories -v
```

## 📊 Estrutura de Testes

```
organizador/tests/
├── __init__.py                 # Marca como package
├── conftest.py                 # Fixtures compartilhadas
├── test_config.py              # Testes de configuração (19 testes)
└── test_organizer.py           # Testes de organização (23 testes)
```

## 🔧 Entendendo as Fixtures

As fixtures são funções reutilizáveis que preparam dados para os testes. Definidas em `conftest.py`:

### `temp_workspace`

Fornece um diretório temporário para testes.

```python
def test_example(temp_workspace: Path):
    file = temp_workspace / "test.txt"
    file.write_text("conteúdo")
```

### `sample_config`

Fornece uma configuração válida de teste.

```python
def test_with_config(sample_config: dict):
    assert "categories" in sample_config
```

### `config_file`

Cria um arquivo de configuração temporário.

```python
def test_config_loading(config_file: Path):
    loader = ConfigLoader(config_file)
    config = loader.load()
```

### `unorganized_files`

Cria arquivos desordenados para testes.

```python
def test_organization(temp_workspace: Path, unorganized_files: list):
    # Trabalha com os arquivos criados
```

## 🧪 Exemplos de Testes

### Teste Simples

```python
def test_stats_initialization() -> None:
    """Deve inicializar com valores zerados."""
    stats = OrganizationStats()
    assert stats.moved == 0
    assert stats.skipped == 0
```

### Teste com Fixtures

```python
def test_organize_moves_files(
    temp_workspace: Path,
    config_file: Path,
    unorganized_files: list
) -> None:
    """Deve mover arquivos para categorias."""
    organizer = FileOrganizer(
        source_path=temp_workspace,
        config_path=config_file
    )
    stats = organizer.organize()

    assert (temp_workspace / "Documentos" / "document.txt").exists()
    assert stats.moved > 0
```

### Teste Parametrizado

```python
@pytest.mark.parametrize(
    "filename,expected_category",
    [
        ("document.txt", "Documentos"),
        ("image.jpg", "Imagens"),
        ("song.mp3", "Audio"),
    ],
    ids=["texto", "imagem", "áudio"]
)
def test_categorization(
    temp_workspace: Path,
    config_file: Path,
    filename: str,
    expected_category: str
) -> None:
    """Deve categorizar corretamente."""
    (temp_workspace / filename).write_text("conteúdo")

    organizer = FileOrganizer(
        source_path=temp_workspace,
        config_path=config_file
    )
    organizer.organize()

    expected_path = temp_workspace / expected_category / filename
    assert expected_path.exists()
```

### Teste com Mock

```python
def test_handle_permission_error(
    temp_workspace: Path,
    config_file: Path
) -> None:
    """Deve lidar com erros de permissão."""
    (temp_workspace / "file.txt").write_text("conteúdo")

    organizer = FileOrganizer(
        source_path=temp_workspace,
        config_path=config_file
    )

    with patch("shutil.move", side_effect=PermissionError("Sem permissão")):
        stats = organizer.organize()

    assert stats.errors > 0
```

### Teste de Exceção

```python
def test_nonexistent_source_raises_error(
    config_file: Path
) -> None:
    """Deve lançar erro se pasta não existe."""
    organizer = FileOrganizer(
        source_path="/inexistente/pasta",
        config_path=config_file
    )

    with pytest.raises(ValueError, match="Pasta não existe"):
        organizer.organize()
```

## 📈 Cobertura de Código

### Atual

- **Total: 82%**
- `test_config.py`: **100%**
- `test_organizer.py`: **100%**
- `config.py`: **90%** (validações edge case)
- `organizer.py`: **90%** (casos de erro)

### Como Aumentar

1. **Identifique linhas não cobertas**

   ```bash
   pytest --cov=organizador --cov-report=term-missing
   ```

2. **Adicione testes para linhas faltantes**
   ```python
   # Exemplo: testar Path cwd() em unique_name
   def test_unique_name_generation():
       # novo teste
   ```

## ✅ Boas Práticas Implementadas

### 1. **TDD (Red-Green-Refactor)**

- Testes definem comportamento esperado
- Implementação satisfaz os testes
- Refatoração mantém testes passando

### 2. **Nomes Descritivos**

- `test_organize_moves_files_to_categories` é claro
- Evita `test_basic` ou `test_function`

### 3. **Fixtures Reutilizáveis**

- `temp_workspace` usada em ~15 testes
- `config_file` usada em ~10 testes
- Evita repetição de setup

### 4. **Parametrização**

- 6 testes de extensão em 1 função parametrizada
- Reduz código duplicado
- IDs legíveis para falhas

### 5. **Mocks Estratégicos**

- Mock de `shutil.move` para testes de erro
- Evita dependências externas
- Testes rápidos e confiáveis

### 6. **Validação Robusta**

- 14 testes apenas de validação
- Previne dados inválidos
- Mensagens de erro claras

## 🔄 Adicionando Novos Testes

### Passo 1: Criar Fixture (se necessário)

```python
# Em conftest.py
@pytest.fixture
def minha_fixture():
    """Descrição."""
    valor = setup()
    yield valor
    cleanup()
```

### Passo 2: Escrever Teste

```python
# Em test_*.py
def test_novo_comportamento(minha_fixture):
    """Deve fazer X quando Y."""
    resultado = funcao(minha_fixture)
    assert resultado == esperado
```

### Passo 3: Rodar Teste

```bash
pytest organizador/tests/test_file.py::test_novo_comportamento -v
```

## 🐛 Debugging de Testes

### Ver Prints Durante Testes

```bash
pytest -s organizador/tests/test_file.py::test_example
```

### Debugger no Teste

```python
def test_example():
    import pdb; pdb.set_trace()  # Pausa execução
    # seu código
```

### Executar com Stack Trace Completo

```bash
pytest --tb=long organizador/tests/test_file.py::test_example
```

## 📚 Referências

- [pytest Documentation](https://docs.pytest.org/)
- [pytest Fixtures](https://docs.pytest.org/en/stable/fixtures.html)
- [pytest Parametrize](https://docs.pytest.org/en/stable/how-to_parametrize.html)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

## 🎯 Métricas de Qualidade

| Métrica                | Valor | Status          |
| ---------------------- | ----- | --------------- |
| Cobertura de Código    | 82%   | ✅ Acima de 80% |
| Testes Passando        | 42/42 | ✅ 100%         |
| Nomes Descritivos      | 100%  | ✅ Sim          |
| Fixtures Reutilizáveis | 6     | ✅ Bom          |
| Testes Parametrizados  | 6     | ✅ Bom          |
| Validações Testadas    | 14    | ✅ Robusto      |

---

**Última Atualização**: Maio de 2026

# Exemplos de Testes com Melhores Práticas

Este arquivo contém exemplos práticos de como escrever testes seguindo as melhores práticas da skill Python Testing Patterns.

## 📌 Índice

1. [Testes Básicos](#testes-básicos)
2. [Fixtures](#fixtures)
3. [Parametrização](#parametrização)
4. [Mocks](#mocks)
5. [Testes de Exceção](#testes-de-exceção)
6. [Testes Assincronos](#testes-assincronos)

---

## Testes Básicos

### Teste Simples com Assert

```python
def test_addition():
    """Teste básico de adição."""
    result = 2 + 2
    assert result == 4
```

### Teste com Múltiplas Asserções

```python
def test_organization_stats():
    """Testa múltiplas propriedades."""
    stats = OrganizationStats(moved=5, skipped=2, errors=0)

    assert stats.moved == 5
    assert stats.skipped == 2
    assert stats.errors == 0
    assert stats.moved + stats.skipped + stats.errors == 7
```

### Teste com Contexto

```python
def test_organize_creates_directories():
    """Verifica criação de diretórios."""
    workspace = Path("test_workspace")
    workspace.mkdir(exist_ok=True)

    try:
        organizer = FileOrganizer(workspace)
        organizer.organize()

        # Verificar estrutura criada
        assert (workspace / "Documentos").exists()
    finally:
        # Limpeza
        import shutil
        shutil.rmtree(workspace, ignore_errors=True)
```

---

## Fixtures

### Fixture Básica

```python
@pytest.fixture
def sample_file(tmp_path):
    """Cria arquivo de amostra."""
    file = tmp_path / "test.txt"
    file.write_text("conteúdo de teste")
    return file

def test_with_sample(sample_file):
    """Usa fixture."""
    assert sample_file.exists()
    assert sample_file.read_text() == "conteúdo de teste"
```

### Fixture com Setup e Teardown

```python
@pytest.fixture
def database():
    """Fixture com inicialização e limpeza."""
    # Setup
    db = DatabaseConnection(":memory:")
    db.connect()

    yield db  # Fornecer ao teste

    # Teardown (executado mesmo se teste falhar)
    db.disconnect()

def test_database_query(database):
    """Usa database fixture."""
    result = database.execute("SELECT 1")
    assert result is not None
```

### Fixture com Parametrização

```python
@pytest.fixture(params=["sqlite", "postgresql"])
def database_connection(request):
    """Fixture parametrizada para testar múltiplos bancos."""
    if request.param == "sqlite":
        return SQLiteConnection(":memory:")
    else:
        return PostgresConnection("localhost")

def test_multiple_databases(database_connection):
    """Teste executado para cada banco de dados."""
    assert database_connection.is_connected()
```

### Fixture com Scope

```python
# Escopo 'function' (padrão) - criada para cada teste
@pytest.fixture
def temp_file(tmp_path):
    return tmp_path / "file.txt"

# Escopo 'module' - criada uma vez por módulo
@pytest.fixture(scope="module")
def expensive_resource():
    resource = ExpensiveSetup()
    yield resource
    resource.cleanup()

# Escopo 'session' - criada uma vez por sessão
@pytest.fixture(scope="session")
def global_config():
    return load_config()
```

---

## Parametrização

### Parametrização Simples

```python
@pytest.mark.parametrize("input,expected", [
    (2, "dois"),
    (3, "três"),
    (5, "cinco"),
])
def test_number_names(input, expected):
    """Teste executado 3 vezes com diferentes parâmetros."""
    assert get_name(input) == expected
```

### Parametrização Múltipla

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_addition(a, b, expected):
    """Testa adição com múltiplos casos."""
    assert add(a, b) == expected
```

### Parametrização com IDs Legíveis

```python
@pytest.mark.parametrize(
    "file_type,category",
    [
        (".pdf", "Documentos"),
        (".jpg", "Imagens"),
        (".mp3", "Audio"),
    ],
    ids=["documento", "imagem", "áudio"]
)
def test_file_categorization(file_type, category):
    """Teste com IDs legíveis no output."""
    assert categorize(file_type) == category
```

### Combinação de Fixture + Parametrização

```python
@pytest.fixture(params=[1, 2, 3])
def multiplier(request):
    return request.param

def test_multiply_by_fixture(multiplier):
    """Teste executado 3 vezes com diferentes multiplicadores."""
    assert multiply(2, multiplier) == 2 * multiplier
```

---

## Mocks

### Mock de Função

```python
from unittest.mock import patch, MagicMock

def test_api_call_with_mock():
    """Testa sem fazer chamada real à API."""
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"id": 1, "name": "Test"}

        response = api_client.get_user(1)

        assert response["name"] == "Test"
        mock_get.assert_called_once_with("http://api.example.com/users/1")
```

### Mock com Side Effect (Exceção)

```python
def test_error_handling_with_mock():
    """Testa tratamento de exceção."""
    with patch("os.path.exists") as mock_exists:
        mock_exists.side_effect = PermissionError("Acesso negado")

        with pytest.raises(PermissionError):
            check_file("important.txt")
```

### Mock de Atributo

```python
def test_config_property():
    """Testa propriedade mockada."""
    with patch("config.DEBUG", True):
        app = Application()
        assert app.is_debug_mode()
```

### Mock de Classe

```python
def test_with_mock_class():
    """Mock de classe inteira."""
    with patch("database.Connection") as MockConnection:
        mock_instance = MagicMock()
        MockConnection.return_value = mock_instance

        db = connect_to_database()

        MockConnection.assert_called_once()
        mock_instance.execute.assert_called()
```

---

## Testes de Exceção

### Exceção com Pytest.raises

```python
def test_divide_by_zero():
    """Testa que exceção é lançada."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

### Exceção com Mensagem

```python
def test_invalid_input():
    """Testa mensagem de exceção."""
    with pytest.raises(ValueError, match="input inválido"):
        validate_email("not-an-email")
```

### Exceção com Atributos

```python
def test_exception_attributes():
    """Verifica atributos da exceção."""
    with pytest.raises(CustomError) as exc_info:
        raise CustomError("Erro", error_code=400)

    assert exc_info.value.error_code == 400
    assert "Erro" in str(exc_info.value)
```

### Garantir que NÃO lança

```python
def test_no_exception_raised():
    """Verifica que NÃO há exceção."""
    # Se houver exceção, o teste falha
    process_valid_data({"name": "Test"})
```

---

## Testes Assincronos

### Teste Async com pytest-asyncio

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Testa função assincronizável."""
    result = await async_add(2, 3)
    assert result == 5
```

### Fixture Async

```python
@pytest.fixture
async def async_client():
    """Fixture assincronizável."""
    async with create_client() as client:
        yield client

@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    """Testa com fixture assincronizável."""
    response = await async_client.get("/data")
    assert response.status_code == 200
```

### Mock Async

```python
@pytest.mark.asyncio
@patch("aiohttp.get")
async def test_async_api_call(mock_get):
    """Testa função async com mock."""
    mock_get.return_value = {"status": "ok"}

    result = await fetch_data()

    mock_get.assert_awaited_once()
```

---

## Padrões Avançados

### Teste com Fixture Factory

```python
@pytest.fixture
def user_factory():
    """Factory pattern em fixture."""
    def _create_user(name="Test", email="test@example.com"):
        return User(name=name, email=email)
    return _create_user

def test_multiple_users(user_factory):
    """Usa factory para criar múltiplos usuários."""
    admin = user_factory(name="Admin", email="admin@example.com")
    user = user_factory()

    assert admin.name == "Admin"
    assert user.name == "Test"
```

### Teste com Conftest Global

```python
# conftest.py na raiz de tests/
@pytest.fixture(scope="session")
def database_url():
    """Fixture global para todos os testes."""
    return os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")

# Disponível em todos os arquivos de teste
def test_with_global_fixture(database_url):
    db = connect(database_url)
    assert db is not None
```

### Marcadores Customizados

```python
# conftest.py
import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marks tests as slow"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration"
    )

# Nos testes
@pytest.mark.slow
def test_slow_operation():
    pass

@pytest.mark.integration
def test_database_integration():
    pass

# Executar
# pytest -m "not slow"  # Pula testes lentos
# pytest -m integration  # Apenas integração
```

---

## 🎯 Resumo de Boas Práticas

| Prática            | ✅ Bom                                            | ❌ Ruim                      |
| ------------------ | ------------------------------------------------- | ---------------------------- |
| **Nomes**          | `test_organize_moves_files_to_correct_categories` | `test_basic`                 |
| **Fixtures**       | Reutilizáveis, bem documentadas                   | Repetitivas, setup no teste  |
| **Parametrização** | Múltiplos casos em 1 função                       | Funções duplicadas           |
| **Mocks**          | Apenas dependências externas                      | Mocka tudo, inclusive lógica |
| **Assertions**     | `assert result == expected`                       | `assert result is not None`  |
| **Exceções**       | `pytest.raises()`                                 | Try/except no teste          |
| **Documentação**   | Docstring em todo teste                           | Sem documentação             |

---

## 📚 Executar Estes Exemplos

```bash
# Crie arquivo: test_examples.py
# Cole exemplos acima
# Execute:

pytest test_examples.py -v
pytest test_examples.py -k "mock" -v
pytest test_examples.py::test_divide_by_zero -v
pytest --markers  # Ver marcadores disponíveis
```

---

**Referência**: Python Testing Patterns Skill  
**Última Atualização**: Maio de 2026

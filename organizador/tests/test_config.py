"""
Testes para a classe ConfigLoader.

Este módulo testa o carregamento e validação de arquivos de configuração,
incluindo validações de estrutura e tratamento de erros.
"""

import json
from pathlib import Path

import pytest

from organizador.config import ConfigLoader


class TestConfigLoaderInitialization:
    """Testes de inicialização do ConfigLoader."""

    def test_initialization_with_default_config(
        self, config_file: Path
    ) -> None:
        """Deve inicializar com arquivo de configuração válido."""
        loader = ConfigLoader(config_file)
        assert loader.config_path == config_file

    def test_initialization_with_nonexistent_file_raises_error(
        self,
    ) -> None:
        """Deve lançar erro se arquivo não existir."""
        with pytest.raises(FileNotFoundError):
            ConfigLoader("/inexistente/config.json")


class TestConfigLoading:
    """Testes de carregamento de configuração."""

    def test_load_valid_config(self, config_file: Path) -> None:
        """Deve carregar configuração válida."""
        loader = ConfigLoader(config_file)
        config = loader.load()

        assert isinstance(config, dict)
        assert "categories" in config
        assert "options" in config

    def test_load_config_has_categories(self, config_file: Path) -> None:
        """Configuração carregada deve ter categorias."""
        loader = ConfigLoader(config_file)
        config = loader.load()

        assert len(config["categories"]) > 0
        assert "Documentos" in config["categories"]

    def test_load_config_with_invalid_json_raises_error(
        self, tmp_path: Path
    ) -> None:
        """Deve lançar erro ao carregar JSON inválido."""
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("{invalid json content")

        loader = ConfigLoader(invalid_file)

        with pytest.raises(json.JSONDecodeError):
            loader.load()


class TestConfigValidation:
    """Testes de validação de configuração."""

    def test_validate_rejects_non_dict_config(
        self, tmp_path: Path
    ) -> None:
        """Deve rejeitar configuração que não é dicionário."""
        invalid_file = tmp_path / "invalid_config.json"
        invalid_file.write_text('["not", "a", "dict"]')

        loader = ConfigLoader(invalid_file)

        with pytest.raises(ValueError, match="Configuração deve ser um dicionário"):
            loader.load()

    def test_validate_rejects_missing_categories_key(
        self, tmp_path: Path
    ) -> None:
        """Deve rejeitar se falta chave 'categories'."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({"options": {}}))

        loader = ConfigLoader(config_file)

        with pytest.raises(ValueError, match="Chaves obrigatórias ausentes"):
            loader.load()

    def test_validate_rejects_missing_options_key(
        self, tmp_path: Path
    ) -> None:
        """Deve rejeitar se falta chave 'options'."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps({
                "categories": {"Documentos": {"extensions": [".txt"]}}
            })
        )

        loader = ConfigLoader(config_file)

        with pytest.raises(ValueError, match="Chaves obrigatórias ausentes"):
            loader.load()

    def test_validate_rejects_empty_categories(
        self, tmp_path: Path, invalid_config: dict
    ) -> None:
        """Deve rejeitar categorias vazias."""
        config_file = tmp_path / "config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(invalid_config, f)

        loader = ConfigLoader(config_file)

        with pytest.raises(ValueError, match="'categories' não pode estar vazio"):
            loader.load()

    def test_validate_rejects_non_dict_categories_value(
        self, tmp_path: Path
    ) -> None:
        """Deve rejeitar se categorias não é dicionário."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps({"categories": ["not", "dict"], "options": {}})
        )

        loader = ConfigLoader(config_file)

        with pytest.raises(ValueError, match="'categories' deve ser um dicionário"):
            loader.load()


class TestCategoryValidation:
    """Testes de validação de categorias."""

    def test_validate_rejects_category_without_extensions(
        self, tmp_path: Path
    ) -> None:
        """Deve rejeitar categoria sem 'extensions'."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps({
                "categories": {"Documentos": {"create_if_missing": True}},
                "options": {},
            })
        )

        loader = ConfigLoader(config_file)

        with pytest.raises(ValueError, match="não tem 'extensions'"):
            loader.load()

    def test_validate_rejects_non_list_extensions(
        self, tmp_path: Path
    ) -> None:
        """Deve rejeitar extensions que não é lista."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps({
                "categories": {
                    "Documentos": {"extensions": ".txt"}  # String em vez de lista
                },
                "options": {},
            })
        )

        loader = ConfigLoader(config_file)

        with pytest.raises(ValueError, match="'extensions' em"):
            loader.load()

    def test_validate_rejects_empty_extensions(
        self, tmp_path: Path
    ) -> None:
        """Deve rejeitar extensions vazia."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps({
                "categories": {"Documentos": {"extensions": []}},
                "options": {},
            })
        )

        loader = ConfigLoader(config_file)

        with pytest.raises(ValueError, match="'extensions' em"):
            loader.load()

    def test_validate_rejects_non_dict_category_info(
        self, tmp_path: Path
    ) -> None:
        """Deve rejeitar categoria que não é dicionário."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps({
                "categories": {"Documentos": ["extensions"]},
                "options": {},
            })
        )

        loader = ConfigLoader(config_file)

        with pytest.raises(ValueError, match="deve ser um dicionário"):
            loader.load()


@pytest.mark.parametrize(
    "extension,should_fail",
    [
        ([".txt"], False),  # Válido
        ([".txt", ".pdf"], False),  # Válido múltiplas
        ([], True),  # Vazio, inválido
        ("", True),  # String em vez de lista, inválido
        (None, True),  # None, inválido
    ],
    ids=[
        "extensão única",
        "múltiplas extensões",
        "extensions vazia",
        "extensions string",
        "extensions None",
    ],
)
def test_extension_validation(
    tmp_path: Path, extension, should_fail
) -> None:
    """Deve validar corretamente diferentes formatos de extensions."""
    config = {
        "categories": {"Documentos": {"extensions": extension}},
        "options": {},
    }

    config_file = tmp_path / "config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f)

    loader = ConfigLoader(config_file)

    if should_fail:
        with pytest.raises((ValueError, TypeError)):
            loader.load()
    else:
        config = loader.load()
        assert config is not None


class TestConfigResolution:
    """Testes de resolução de caminho de configuração."""

    def test_resolve_config_path_with_explicit_path(
        self, config_file: Path
    ) -> None:
        """Deve usar caminho explícito fornecido."""
        loader = ConfigLoader(config_file)
        assert loader.config_path == config_file

    def test_resolve_config_path_with_string_path(
        self, config_file: Path
    ) -> None:
        """Deve converter string para Path."""
        loader = ConfigLoader(str(config_file))
        assert isinstance(loader.config_path, Path)
        assert loader.config_path == config_file

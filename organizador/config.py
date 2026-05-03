"""
Módulo responsável pelo carregamento e validação de configurações.

Este módulo fornece a classe ConfigLoader que lê o arquivo de configuração
JSON e o valida contra um esquema esperado.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Carregador e validador de arquivo de configuração JSON."""

    DEFAULT_CONFIG_NAME = "config.json"
    REQUIRED_KEYS = {"categories", "options"}

    def __init__(self, config_path: Optional[Path | str] = None) -> None:
        """
        Inicializa o carregador de configuração.

        Args:
            config_path: Caminho do arquivo de configuração.
                        Se None, procura no diretório do módulo.

        Raises:
            FileNotFoundError: Se o arquivo de configuração não existir.
        """
        self.config_path = self._resolve_config_path(config_path)
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Arquivo de configuração não encontrado: {self.config_path}"
            )

    def _resolve_config_path(
        self, config_path: Optional[Path | str]
    ) -> Path:
        """
        Resolve o caminho da configuração.

        Args:
            config_path: Caminho fornecido ou None.

        Returns:
            Path: Caminho resolvido da configuração.
        """
        if config_path is not None:
            return Path(config_path)

        # Procura no diretório do módulo
        module_dir = Path(__file__).parent
        default_path = module_dir / self.DEFAULT_CONFIG_NAME

        if default_path.exists():
            return default_path

        # Fallback para diretório atual
        return Path(self.DEFAULT_CONFIG_NAME)

    def load(self) -> Dict[str, Any]:
        """
        Carrega o arquivo de configuração.

        Returns:
            Dict: Configuração carregada.

        Raises:
            json.JSONDecodeError: Se o JSON for inválido.
            ValueError: Se a configuração não for válida.
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Erro ao decodificar JSON em {self.config_path}: {e.msg}",
                e.doc,
                e.pos,
            ) from e

        self._validate_config(config)
        return config

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Valida a estrutura da configuração.

        Args:
            config: Configuração a validar.

        Raises:
            ValueError: Se a configuração não for válida.
        """
        if not isinstance(config, dict):
            raise ValueError("Configuração deve ser um dicionário")

        missing_keys = self.REQUIRED_KEYS - set(config.keys())
        if missing_keys:
            raise ValueError(
                f"Chaves obrigatórias ausentes: {missing_keys}"
            )

        if not isinstance(config.get("categories"), dict):
            raise ValueError("'categories' deve ser um dicionário")

        if not config["categories"]:
            raise ValueError("'categories' não pode estar vazio")

        self._validate_categories(config["categories"])

    def _validate_categories(
        self, categories: Dict[str, Dict[str, Any]]
    ) -> None:
        """
        Valida a estrutura das categorias.

        Args:
            categories: Dicionário de categorias.

        Raises:
            ValueError: Se alguma categoria for inválida.
        """
        for category_name, category_info in categories.items():
            if not isinstance(category_info, dict):
                raise ValueError(
                    f"Categoria '{category_name}' deve ser um dicionário"
                )

            if "extensions" not in category_info:
                raise ValueError(
                    f"Categoria '{category_name}' não tem 'extensions'"
                )

            if not isinstance(category_info["extensions"], list):
                raise ValueError(
                    f"'extensions' em '{category_name}' deve ser lista"
                )

            if not category_info["extensions"]:
                raise ValueError(
                    f"'extensions' em '{category_name}' não pode ser vazia"
                )

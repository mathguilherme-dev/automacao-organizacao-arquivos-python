"""
Módulo responsável pela organização de arquivos em categorias.

Este módulo contém a lógica principal para mover arquivos para pastas
organizadas de acordo com suas extensões.
"""

import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from organizador.config import ConfigLoader


@dataclass
class OrganizationStats:
    """Estatísticas de organização de arquivos."""

    moved: int = 0
    skipped: int = 0
    errors: int = 0

    def __str__(self) -> str:
        """Retorna representação em string das estatísticas."""
        return (
            f"\n{'='*40}\n"
            f"✅ Movidos: {self.moved}\n"
            f"⏭️  Pulados: {self.skipped}\n"
            f"❌ Erros: {self.errors}\n"
            f"{'='*40}\n"
        )


class FileOrganizer:
    """Organizador de arquivos em categorias baseado em extensão."""

    def __init__(
        self,
        source_path: Path | str,
        config_path: Optional[Path | str] = None,
        verbose: bool = False,
    ) -> None:
        """
        Inicializa o organizador de arquivos.

        Args:
            source_path: Caminho da pasta a organizar.
            config_path: Caminho do arquivo de configuração.
            verbose: Se True, exibe logs de debug.

        Raises:
            FileNotFoundError: Se o arquivo de configuração não existir.
        """
        self.source_path = Path(source_path)
        self.config_loader = ConfigLoader(config_path)
        self.config = self.config_loader.load()
        self.stats = OrganizationStats()
        self._setup_logging(verbose)

    def _setup_logging(self, verbose: bool) -> None:
        """Configura o sistema de logging."""
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(message)s",
            force=True,  # Garante que a config seja aplicada
        )
        self.logger = logging.getLogger(__name__)

    def organize(self, dry_run: bool = False) -> OrganizationStats:
        """
        Organiza os arquivos da pasta de origem.

        Args:
            dry_run: Se True, simula a organização sem mover arquivos.

        Returns:
            OrganizationStats: Estatísticas da organização.

        Raises:
            ValueError: Se a pasta de origem não existir.
        """
        if not self.source_path.exists():
            raise ValueError(f"Pasta não existe: {self.source_path}")

        mode = "Simulando" if dry_run else "Organizando"
        self.logger.info(f"🚀 {mode}: {self.source_path}")

        try:
            for file_path in self.source_path.iterdir():
                if file_path.is_file():
                    self._move_file(file_path, dry_run)
        except Exception as e:
            self.stats.errors += 1
            self.logger.error(f"❌ Erro ao organizar: {e}")

        self.logger.info(str(self.stats))
        return self.stats

    def _move_file(self, file_path: Path, dry_run: bool = False) -> bool:
        """
        Move um arquivo para sua categoria apropriada.

        Args:
            file_path: Caminho do arquivo a mover.
            dry_run: Se True, simula a ação sem mover.

        Returns:
            bool: True se o arquivo foi movido, False caso contrário.
        """
        category = self._find_category(file_path)

        if category is None:
            self.logger.warning(f"⚠️  {file_path.name} - sem categoria")
            return False

        destination_dir = self._ensure_category_dir(category, dry_run)
        if destination_dir is None:
            return False

        destination_path = self._resolve_destination(
            file_path, destination_dir
        )

        # Se destination_path é None, significa que a ação foi pulada
        if destination_path is None:
            return False

        if not dry_run:
            try:
                shutil.move(str(file_path), str(destination_path))
            except Exception as e:
                self.stats.errors += 1
                self.logger.error(f"❌ Erro ao mover {file_path.name}: {e}")
                return False

        self.logger.info(f"✅ {file_path.name} → {category}/")
        self.stats.moved += 1
        return True

    def _find_category(self, file_path: Path) -> Optional[str]:
        """
        Encontra a categoria apropriada para um arquivo.

        Args:
            file_path: Caminho do arquivo.

        Returns:
            str: Nome da categoria ou None se não encontrada.
        """
        file_extension = file_path.suffix.lower()

        for category, info in self.config["categories"].items():
            if file_extension in info["extensions"]:
                return category

        return None

    def _ensure_category_dir(
        self, category: str, dry_run: bool = False
    ) -> Optional[Path]:
        """
        Garante que a pasta da categoria existe.

        Args:
            category: Nome da categoria.
            dry_run: Se True, não cria a pasta.

        Returns:
            Path: Caminho da pasta da categoria ou None se erro.
        """
        category_dir = self.source_path / category

        if not category_dir.exists():
            if not dry_run:
                try:
                    category_dir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    self.logger.error(
                        f"❌ Erro ao criar pasta {category}: {e}"
                    )
                    self.stats.errors += 1
                    return None

        return category_dir

    def _resolve_destination(
        self, file_path: Path, destination_dir: Path
    ) -> Path:
        """
        Resolve o caminho de destino, tratando duplicatas.

        Args:
            file_path: Caminho do arquivo original.
            destination_dir: Diretório de destino.

        Returns:
            Path: Caminho final de destino.
        """
        destination_path = destination_dir / file_path.name
        handle_duplicates = self.config["options"].get(
            "handle_duplicates", "skip"
        )

        if not destination_path.exists():
            return destination_path

        if handle_duplicates == "skip":
            self.stats.skipped += 1
            self.logger.info(f"⏭️  {file_path.name} - já existe (skip)")
            return None

        if handle_duplicates == "rename":
            # Trata nomes duplicados adicionando _1, _2, etc
            return self._generate_unique_name(
                destination_dir, file_path
            )

        return destination_path

    def _generate_unique_name(
        self, destination_dir: Path, file_path: Path
    ) -> Path:
        """
        Gera um nome único para arquivo duplicado.

        Args:
            destination_dir: Diretório de destino.
            file_path: Arquivo original.

        Returns:
            Path: Caminho com nome único.
        """
        counter = 1
        stem = file_path.stem
        suffix = file_path.suffix

        while True:
            new_name = f"{stem}_{counter}{suffix}"
            new_path = destination_dir / new_name
            if not new_path.exists():
                return new_path
            counter += 1

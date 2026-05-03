"""
Testes para a classe FileOrganizer.

Este módulo testa a lógica principal de organização de arquivos,
incluindo casos normais, edge cases e tratamento de erros.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from organizador.organizer import FileOrganizer, OrganizationStats


class TestFileOrganizerInitialization:
    """Testes de inicialização do FileOrganizer."""

    def test_initialization_with_valid_config(
        self, temp_workspace: Path, config_file: Path
    ) -> None:
        """Deve inicializar com configuração válida."""
        organizer = FileOrganizer(
            source_path=temp_workspace, config_path=config_file
        )
        assert organizer.source_path == temp_workspace
        assert organizer.config is not None

    def test_initialization_with_invalid_path_raises_error(
        self, config_file: Path
    ) -> None:
        """Deve lançar erro se a configuração não existir."""
        with pytest.raises(FileNotFoundError):
            FileOrganizer(
                source_path="/inexistente/path",
                config_path="/inexistente/config.json",
            )

    def test_initialization_sets_logging_level(
        self, temp_workspace: Path, config_file: Path
    ) -> None:
        """Deve configurar logging corretamente."""
        organizer_verbose = FileOrganizer(
            source_path=temp_workspace,
            config_path=config_file,
            verbose=True,
        )
        assert organizer_verbose.logger is not None


class TestBasicOrganization:
    """Testes básicos de organização de arquivos."""

    def test_organize_moves_files_to_categories(
        self, temp_workspace: Path, config_file: Path, unorganized_files: list
    ) -> None:
        """Deve mover arquivos para suas categorias corretas."""
        organizer = FileOrganizer(
            source_path=temp_workspace, config_path=config_file
        )
        stats = organizer.organize()

        assert (temp_workspace / "Documentos" / "document.txt").exists()
        assert (temp_workspace / "Imagens" / "image.jpg").exists()
        assert (temp_workspace / "Audio" / "song.mp3").exists()
        assert stats.moved > 0

    def test_organize_nonexistent_source_raises_error(
        self, config_file: Path
    ) -> None:
        """Deve lançar erro se pasta de origem não existe."""
        organizer = FileOrganizer(
            source_path="/inexistente/pasta", config_path=config_file
        )

        with pytest.raises(ValueError, match="Pasta não existe"):
            organizer.organize()

    def test_organize_returns_stats(
        self, temp_workspace: Path, config_file: Path
    ) -> None:
        """Deve retornar estatísticas da organização."""
        (temp_workspace / "test.txt").write_text("conteúdo")

        organizer = FileOrganizer(
            source_path=temp_workspace, config_path=config_file
        )
        stats = organizer.organize()

        assert isinstance(stats, OrganizationStats)
        assert stats.moved > 0
        assert stats.skipped == 0
        assert stats.errors == 0


class TestDryRunMode:
    """Testes do modo de simulação (dry-run)."""

    def test_dry_run_does_not_move_files(
        self, temp_workspace: Path, config_file: Path, unorganized_files: list
    ) -> None:
        """Modo dry-run não deve mover arquivos."""
        organizer = FileOrganizer(
            source_path=temp_workspace, config_path=config_file
        )
        stats = organizer.organize(dry_run=True)

        # Arquivos devem permanecer no local original
        assert (temp_workspace / "document.txt").exists()
        assert (temp_workspace / "image.jpg").exists()

        # Diretórios de categoria não devem ser criados
        assert not (temp_workspace / "Documentos").exists()

    def test_dry_run_still_counts_movements(
        self, temp_workspace: Path, config_file: Path
    ) -> None:
        """Dry-run deve contar movimentos sem fazer."""
        (temp_workspace / "file.txt").write_text("conteúdo")

        organizer = FileOrganizer(
            source_path=temp_workspace, config_path=config_file
        )
        stats = organizer.organize(dry_run=True)

        assert stats.moved > 0


class TestDuplicateHandling:
    """Testes de tratamento de arquivos duplicados."""

    def test_duplicate_skip_strategy(
        self,
        temp_workspace: Path,
        config_file: Path,
        duplicate_files: tuple,
    ) -> None:
        """Estratégia SKIP deve pular arquivos duplicados."""
        organizer = FileOrganizer(
            source_path=temp_workspace, config_path=config_file
        )
        stats = organizer.organize()

        # Arquivo duplicado não deve ser movido
        assert (temp_workspace / "report.txt").exists()
        assert stats.skipped > 0

    def test_duplicate_rename_strategy(
        self, temp_workspace: Path, config_file: Path, sample_config: dict
    ) -> None:
        """Estratégia RENAME deve renomear arquivos duplicados."""
        # Criar arquivo original
        original = temp_workspace / "report.txt"
        original.write_text("novo conteúdo")

        # Criar arquivo existente
        dest_dir = temp_workspace / "Documentos"
        dest_dir.mkdir()
        existing = dest_dir / "report.txt"
        existing.write_text("conteúdo existente")

        # Atualizar config para rename
        sample_config["options"]["handle_duplicates"] = "rename"
        config_path = temp_workspace / "config_rename.json"
        import json

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(sample_config, f)

        organizer = FileOrganizer(
            source_path=temp_workspace, config_path=config_path
        )
        stats = organizer.organize()

        # Arquivo deve ter sido renomeado
        renamed_files = list(dest_dir.glob("report_*"))
        assert len(renamed_files) > 0
        assert stats.moved > 0


@pytest.mark.parametrize(
    "filename,expected_category",
    [
        ("document.txt", "Documentos"),
        ("image.jpg", "Imagens"),
        ("photo.png", "Imagens"),
        ("song.mp3", "Audio"),
        ("data.csv", "Planilhas"),
        ("video.mp4", "Videos"),
    ],
    ids=[
        "texto para documentos",
        "jpg para imagens",
        "png para imagens",
        "mp3 para audio",
        "csv para planilhas",
        "mp4 para videos",
    ],
)
def test_file_categorization(
    temp_workspace: Path, config_file: Path, filename: str, expected_category: str
) -> None:
    """Deve categorizar arquivos corretamente por extensão."""
    (temp_workspace / filename).write_text("conteúdo teste")

    organizer = FileOrganizer(
        source_path=temp_workspace, config_path=config_file
    )
    stats = organizer.organize()

    expected_path = temp_workspace / expected_category / filename
    assert expected_path.exists(), f"{filename} não foi movido para {expected_category}"
    assert stats.moved > 0


class TestUncategorizedFiles:
    """Testes para arquivos sem categoria."""

    def test_uncategorized_files_remain_in_source(
        self, temp_workspace: Path, config_file: Path
    ) -> None:
        """Arquivos sem categoria devem permanecer na origem."""
        uncategorized = temp_workspace / "unknown.xyz"
        uncategorized.write_text("conteúdo desconhecido")

        organizer = FileOrganizer(
            source_path=temp_workspace, config_path=config_file
        )
        organizer.organize()

        # Arquivo deve permanecer
        assert uncategorized.exists()

    def test_uncategorized_file_statistics(
        self, temp_workspace: Path, config_file: Path
    ) -> None:
        """Arquivos não categorizados não devem incrementar estatísticas."""
        (temp_workspace / "unknown.xyz").write_text("conteúdo")

        organizer = FileOrganizer(
            source_path=temp_workspace, config_path=config_file
        )
        stats = organizer.organize()

        assert stats.moved == 0
        assert stats.skipped == 0


class TestOrganizationStats:
    """Testes da classe OrganizationStats."""

    def test_stats_initialization(self) -> None:
        """Deve inicializar com valores zerados."""
        stats = OrganizationStats()
        assert stats.moved == 0
        assert stats.skipped == 0
        assert stats.errors == 0

    def test_stats_string_representation(self) -> None:
        """Deve ter representação em string formatada."""
        stats = OrganizationStats(moved=5, skipped=2, errors=1)
        stats_str = str(stats)

        assert "5" in stats_str
        assert "2" in stats_str
        assert "1" in stats_str


class TestErrorHandling:
    """Testes de tratamento de erros."""

    def test_organize_handles_permission_error(
        self, temp_workspace: Path, config_file: Path
    ) -> None:
        """Deve lidar com erros de permissão."""
        (temp_workspace / "file.txt").write_text("conteúdo")

        organizer = FileOrganizer(
            source_path=temp_workspace, config_path=config_file
        )

        # Mock para simular erro de permissão
        with patch("shutil.move", side_effect=PermissionError("Sem permissão")):
            stats = organizer.organize()

        assert stats.errors > 0


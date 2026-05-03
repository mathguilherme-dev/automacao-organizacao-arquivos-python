"""
Arquivo de configuração de testes compartilhadas.

Este módulo define fixtures reutilizáveis para todos os testes do projeto.
As fixtures aqui definidas estão disponíveis automaticamente em todos os
arquivos de teste.
"""

import json
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_workspace(tmp_path: Path) -> Path:
    """
    Fornece um diretório temporário para testes.

    Args:
        tmp_path: Fixture do pytest que fornece diretório temporário.

    Yields:
        Path: Caminho do diretório temporário.
    """
    return tmp_path


@pytest.fixture
def sample_config() -> dict:
    """
    Fornece uma configuração de exemplo para testes.

    Returns:
        dict: Configuração de teste.
    """
    return {
        "categories": {
            "Documentos": {
                "extensions": [".pdf", ".txt", ".docx"],
                "create_if_missing": True,
            },
            "Imagens": {
                "extensions": [".jpg", ".png", ".gif"],
                "create_if_missing": True,
            },
            "Planilhas": {
                "extensions": [".csv", ".xlsx"],
                "create_if_missing": True,
            },
            "Audio": {
                "extensions": [".mp3", ".wav"],
                "create_if_missing": True,
            },
            "Videos": {
                "extensions": [".mp4", ".avi"],
                "create_if_missing": True,
            },
        },
        "options": {"handle_duplicates": "skip"},
    }


@pytest.fixture
def config_file(
    tmp_path: Path, sample_config: dict
) -> Path:
    """
    Cria um arquivo de configuração temporário.

    Args:
        tmp_path: Diretório temporário.
        sample_config: Configuração de teste.

    Returns:
        Path: Caminho do arquivo de configuração.
    """
    config_path = tmp_path / "config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(sample_config, f)
    return config_path


@pytest.fixture
def organized_files(
    temp_workspace: Path,
) -> dict[str, Path]:
    """
    Cria uma estrutura de arquivos de teste já organizados.

    Args:
        temp_workspace: Diretório de trabalho temporário.

    Returns:
        dict: Mapeamento de categoria para caminho da pasta.
    """
    categories = {
        "Documentos": temp_workspace / "Documentos",
        "Imagens": temp_workspace / "Imagens",
        "Audio": temp_workspace / "Audio",
    }

    for cat_path in categories.values():
        cat_path.mkdir(parents=True, exist_ok=True)

    # Criar alguns arquivos de exemplo
    (categories["Documentos"] / "doc1.txt").write_text("conteúdo doc")
    (categories["Imagens"] / "img1.jpg").write_text("conteúdo img")
    (categories["Audio"] / "song1.mp3").write_text("conteúdo audio")

    return categories


@pytest.fixture
def unorganized_files(temp_workspace: Path) -> list[Path]:
    """
    Cria uma estrutura de arquivos desordenados.

    Args:
        temp_workspace: Diretório de trabalho temporário.

    Returns:
        list: Lista de arquivos criados.
    """
    files = [
        temp_workspace / "document.txt",
        temp_workspace / "image.jpg",
        temp_workspace / "song.mp3",
        temp_workspace / "video.mp4",
        temp_workspace / "spreadsheet.csv",
        temp_workspace / "photo.png",
        temp_workspace / "audio.wav",
    ]

    for file_path in files:
        file_path.write_text(f"conteúdo de {file_path.name}")

    return files


@pytest.fixture
def duplicate_files(temp_workspace: Path) -> tuple[Path, Path]:
    """
    Cria dois arquivos com mesmo nome em locais diferentes.

    Args:
        temp_workspace: Diretório de trabalho temporário.

    Returns:
        tuple: (arquivo original, arquivo existente no destino)
    """
    # Arquivo original
    original = temp_workspace / "report.txt"
    original.write_text("conteúdo original")

    # Arquivo já existente
    dest_dir = temp_workspace / "Documentos"
    dest_dir.mkdir(exist_ok=True)
    existing = dest_dir / "report.txt"
    existing.write_text("conteúdo existente")

    return original, existing


@pytest.fixture
def invalid_config() -> dict:
    """
    Fornece uma configuração inválida para testes.

    Returns:
        dict: Configuração inválida.
    """
    return {
        "categories": {},  # Vazio, inválido
        "options": {"handle_duplicates": "skip"},
    }


@pytest.fixture
def incomplete_config() -> dict:
    """
    Fornece uma configuração incompleta para testes.

    Returns:
        dict: Configuração faltando chaves obrigatórias.
    """
    return {
        "categories": {
            "Documentos": {
                "extensions": [".txt"],
            }
        }
        # Falta 'options'
    }

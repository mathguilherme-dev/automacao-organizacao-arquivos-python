#!/usr/bin/env python3
"""
Ponto de entrada para o organizador de arquivos.

Este módulo fornece a interface de linha de comando para organizar arquivos.
"""

import argparse
import logging
import sys
from pathlib import Path
from tkinter import Tk, filedialog

from organizador.organizer import FileOrganizer


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Cria o parser de argumentos da linha de comando.

    Returns:
        ArgumentParser: Parser configurado.
    """
    parser = argparse.ArgumentParser(
        description="Organizador de arquivos automático",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python -m organizador /caminho/para/pasta
  python -m organizador /caminho/para/pasta --config config.json
  python -m organizador /caminho/para/pasta --dry-run
  python -m organizador /caminho/para/pasta --verbose
        """,
    )

    parser.add_argument(
        "path",
        nargs="?",
        type=str,
        help="Caminho da pasta a organizar (optional, abre dialog se omitido)",
    )

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=None,
        help="Caminho do arquivo de configuração (default: config.json)",
    )

    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Simula a organização sem mover arquivos",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Exibe logs detalhados",
    )

    return parser


def select_folder_dialog() -> Path | None:
    """
    Abre um diálogo para seleção de pasta.

    Returns:
        Path: Caminho selecionado ou None se cancelado.
    """
    root = Tk()
    root.withdraw()  # Esconde a janela principal

    folder_path = filedialog.askdirectory(
        title="Selecione a pasta a organizar"
    )

    root.destroy()

    if not folder_path:
        return None

    return Path(folder_path)


def main() -> int:
    """
    Função principal da aplicação.

    Returns:
        int: Código de saída (0 para sucesso, 1 para erro).
    """
    parser = create_argument_parser()
    args = parser.parse_args()

    # Se não forneceu caminho, abre diálogo
    if not args.path:
        path = select_folder_dialog()
        if path is None:
            print("❌ Nenhuma pasta foi selecionada")
            return 1
    else:
        path = Path(args.path)

    try:
        organizer = FileOrganizer(
            source_path=path,
            config_path=args.config,
            verbose=args.verbose,
        )

        stats = organizer.organize(dry_run=args.dry_run)

        # Retorna código de erro se houve erros
        return 1 if stats.errors > 0 else 0

    except FileNotFoundError as e:
        logging.error(f"❌ {e}")
        return 1
    except ValueError as e:
        logging.error(f"❌ Erro de validação: {e}")
        return 1
    except Exception as e:
        logging.error(f"❌ Erro inesperado: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
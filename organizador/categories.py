"""
Módulo com definições padrão de categorias e extensões.

Este módulo contém as configurações padrão de categorias que são usadas
quando não há arquivo config.json personalizado.
"""

from typing import Dict, Any

# Configuração padrão de categorias e extensões
DEFAULT_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "Imagens": {
        "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".webp", ".tiff", ".tif", ".psd", ".ai", ".eps", ".raw", ".cr2", ".nef", ".orf", ".sr2", ".heic"],
        "create_if_missing": True
    },
    "Documentos": {
        "extensions": [".pdf", ".txt", ".docx", ".doc", ".pptx", ".ppt", ".pps", ".ppsx", ".odt", ".rtf", ".dot", ".dotx", ".md", ".epub", ".mobi", ".wpd", ".wps", ".pages", ".key", ".numbers"],
        "create_if_missing": True
    },
    "Planilhas": {
        "extensions": [
            ".xlsx", ".xls", ".xlsm", ".xlt", ".xltx", ".csv", ".ods", ".ots", 
            ".wks", ".wk1", ".wk3", ".wk4", ".123", ".dbf", ".gnumeric", ".qpw", ".xlw"
        ],
        "create_if_missing": True
    },
    "Videos": {
        "extensions": [".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".rmvb", ".rm", ".mpg", ".mpeg", ".m4v", ".vob", ".3gp", ".webm", ".ts", ".asf"],
        "create_if_missing": True
    },
    "Audio": {
        "extensions": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".wma", ".ogg", ".mid", ".midi", ".amr", ".aiff", ".au", ".alac", ".ape"],
        "create_if_missing": True
    },
    "Compactados": {
        "extensions": [".zip", ".rar", ".7z", ".tar", ".gz", ".arj", ".bz2", ".cab", ".tgz", ".z", ".lz", ".lzh"],
        "create_if_missing": True
    },
    "Executáveis": {
        "extensions": [".exe", ".msi", ".app", ".deb", ".apk", ".bat", ".cmd", ".sh", ".bin", ".run"],
        "create_if_missing": True
    },
    "Código": {
        "extensions": [
            ".py", ".js", ".java", ".cpp", ".c", ".ts", ".go", ".rb", ".php", 
            ".html", ".css", ".htm", ".scss", ".less", ".cs", ".swift", ".kt", ".rs", ".pl", ".sh"
        ],
        "create_if_missing": True
    },
    "Dados": {
        "extensions": [
            ".json", ".xml", ".sql", ".db", ".yml", ".yaml", ".ini", ".conf", ".sqlite", ".sqlite3", ".mdb", ".accdb"
        ],
        "create_if_missing": True
    },
    "Fontes": {
        "extensions": [".ttf", ".otf", ".woff", ".woff2", ".eot", ".fon", ".fnt"],
        "create_if_missing": True
    },
    "Discos": {
        "extensions": [".iso", ".dmg", ".img", ".vhd", ".vmdk", ".ova", ".bin", ".cue"],
        "create_if_missing": True
    },
    "Outros": {
        "extensions": [".winmd", ".dll", ".sys", ".tmp", ".bak", ".log", ".crdownload", ".part", ".torrent"],
        "create_if_missing": True
    }
}

# Configurações padrão de logging
DEFAULT_LOGGING: Dict[str, Any] = {
    "enabled": True,
    "console_enabled": True,
    "level": "INFO",
    "log_file": "organizer.log"
}

# Configurações padrão de opções
DEFAULT_OPTIONS: Dict[str, Any] = {
    "handle_duplicates": "rename",
    "preserve_source": False,
    "ask_on_overwrite": False
}

# Configuração completa padrão
DEFAULT_CONFIG: Dict[str, Any] = {
    "categories": DEFAULT_CATEGORIES,
    "logging": DEFAULT_LOGGING,
    "options": DEFAULT_OPTIONS
}
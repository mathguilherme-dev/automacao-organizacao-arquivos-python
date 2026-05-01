import unittest
from pathlib import Path
import shutil
import json
import tempfile
from organizador.organizer import FileOrganizer
from organizador.config import ConfigLoader


class TestFileOrganizer(unittest.TestCase):
    """Testes para a classe FileOrganizer"""
    
    def setUp(self):
        """Prepara ambiente para cada teste"""
        self.test_dir = Path('test_workspace')
        self.test_dir.mkdir(exist_ok=True)
        self.config_path = Path(__file__).parent.parent / 'config.json'
    
    def tearDown(self):
        """Limpa após cada teste"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def _create_test_files(self):
        """Cria arquivos de teste em diferentes tipos"""
        (self.test_dir / 'test.txt').write_text('documento')
        (self.test_dir / 'photo.jpg').write_text('imagem')
        (self.test_dir / 'data.csv').write_text('planilha')
        (self.test_dir / 'video.mp4').write_text('video')
        (self.test_dir / 'song.mp3').write_text('audio')
    
    def test_organize_basic(self):
        """Teste 1: Organizar arquivos básicos"""
        self._create_test_files()
        
        org = FileOrganizer(self.test_dir, self.config_path)
        org.organize()
        
        # Verificar se os arquivos foram movidos para suas categorias
        self.assertTrue((self.test_dir / 'Documentos' / 'test.txt').exists())
        self.assertTrue((self.test_dir / 'Imagens' / 'photo.jpg').exists())
        self.assertTrue((self.test_dir / 'Planilhas' / 'data.csv').exists())
        self.assertTrue((self.test_dir / 'Videos' / 'video.mp4').exists())
        self.assertTrue((self.test_dir / 'Audio' / 'song.mp3').exists())
    
    def test_dry_run(self):
        """Teste 2: Modo dry-run (simular sem mover)"""
        self._create_test_files()
        
        org = FileOrganizer(self.test_dir, self.config_path)
        org.organize(dry_run=True)
        
        # Verificar que os arquivos NÃO foram movidos
        self.assertTrue((self.test_dir / 'test.txt').exists())
        self.assertTrue((self.test_dir / 'photo.jpg').exists())
        self.assertFalse((self.test_dir / 'Documentos').exists())
    
    def test_duplicate_skip(self):
        """Teste 3: Tratamento de duplicados - SKIP"""
        # Criar arquivo original
        (self.test_dir / 'test.txt').write_text('original')
        (self.test_dir / 'Documentos').mkdir()
        (self.test_dir / 'Documentos' / 'test.txt').write_text('existente')
        
        # Modificar config para skip
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        config['options']['handle_duplicates'] = 'skip'
        temp_config = self.test_dir / 'config_skip.json'
        with open(temp_config, 'w', encoding='utf-8') as f:
            json.dump(config, f)
        
        org = FileOrganizer(self.test_dir, temp_config)
        org.organize()
        
        # Verificar que o arquivo original não foi movido
        self.assertTrue((self.test_dir / 'test.txt').exists())
        # E o existente permanece intacto
        self.assertEqual((self.test_dir / 'Documentos' / 'test.txt').read_text(), 'existente')
        self.assertEqual(org.stats['skipped'], 1)
    
    def test_duplicate_rename(self):
        """Teste 4: Tratamento de duplicados - RENAME"""
        # Criar arquivo original
        (self.test_dir / 'test.txt').write_text('novo')
        (self.test_dir / 'Documentos').mkdir()
        (self.test_dir / 'Documentos' / 'test.txt').write_text('existente')
        
        # Modificar config para rename
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        config['options']['handle_duplicates'] = 'rename'
        temp_config = self.test_dir / 'config_rename.json'
        with open(temp_config, 'w', encoding='utf-8') as f:
            json.dump(config, f)
        
        org = FileOrganizer(self.test_dir, temp_config)
        org.organize()
        
        # Verificar que o arquivo foi renomeado
        self.assertTrue((self.test_dir / 'Documentos' / 'test_1.txt').exists())
        self.assertEqual((self.test_dir / 'Documentos' / 'test_1.txt').read_text(), 'novo')
        self.assertEqual(org.stats['renamed'], 1)
    
    def test_duplicate_overwrite(self):
        """Teste 5: Tratamento de duplicados - OVERWRITE"""
        # Criar arquivo original
        (self.test_dir / 'test.txt').write_text('novo')
        (self.test_dir / 'Documentos').mkdir()
        (self.test_dir / 'Documentos' / 'test.txt').write_text('antigo')
        
        # Modificar config para overwrite
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        config['options']['handle_duplicates'] = 'overwrite'
        temp_config = self.test_dir / 'config_overwrite.json'
        with open(temp_config, 'w', encoding='utf-8') as f:
            json.dump(config, f)
        
        org = FileOrganizer(self.test_dir, temp_config)
        org.organize()
        
        # Verificar que o arquivo foi sobrescrito
        self.assertEqual((self.test_dir / 'Documentos' / 'test.txt').read_text(), 'novo')
        self.assertEqual(org.stats['moved'], 1)
    
    def test_invalid_path(self):
        """Teste 6: Caminho inválido deve lançar erro"""
        invalid_path = self.test_dir / 'nao_existe'
        
        org = FileOrganizer(invalid_path, self.config_path)
        
        with self.assertRaises(FileNotFoundError):
            org.organize()
    
    def test_unmatched_extension(self):
        """Teste 7: Arquivo sem categoria correspondente"""
        (self.test_dir / 'arquivo.xyz').write_text('desconhecido')
        
        org = FileOrganizer(self.test_dir, self.config_path)
        org.organize()
        
        # Arquivo deve permanecer na pasta raiz
        self.assertTrue((self.test_dir / 'arquivo.xyz').exists())
        self.assertEqual(org.stats['moved'], 0)
    
    def test_stats_counter(self):
        """Teste 8: Contador de estatísticas"""
        self._create_test_files()
        
        org = FileOrganizer(self.test_dir, self.config_path)
        org.organize()
        
        # Verificar estatísticas
        self.assertEqual(org.stats['moved'], 5)
        self.assertEqual(org.stats['errors'], 0)
        self.assertEqual(org.stats['skipped'], 0)
    
    def test_case_insensitive_extension(self):
        """Teste 9: Extensões insensíveis a maiúsculas"""
        (self.test_dir / 'document.TXT').write_text('teste')
        (self.test_dir / 'IMAGE.JPG').write_text('teste')
        
        org = FileOrganizer(self.test_dir, self.config_path)
        org.organize()
        
        # Deve reconhecer extensões em maiúsculas
        self.assertTrue((self.test_dir / 'Documentos' / 'document.TXT').exists())
        self.assertTrue((self.test_dir / 'Imagens' / 'IMAGE.JPG').exists())


if __name__ == '__main__':
    unittest.main()


import argparse
import json
import sys
import shutil
import logging
from pathlib import Path

class Org:
    def __init__(self, path, cfg_path=None, verbose=False, dry=False):
        self.src = Path(path)
        self.dry = dry
        self.cfg = json.loads((Path(__file__).parent / (cfg_path or 'config.json')).read_text(encoding='utf-8'))
        self.stats = {'moved': 0, 'skip': 0, 'err': 0}
        
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(level=level, format='%(message)s')
        self.log = logging.getLogger()
    
    def organize(self):
        if not self.src.exists():
            print(f'❌ Pasta não existe: {self.src}')
            return
        
        print(f"🚀 {'Simulando' if self.dry else 'Organizando'}: {self.src}")
        
        try:
            for f in self.src.iterdir():
                if f.is_file():
                    self._move(f)
        except Exception as e:
            self.stats['err'] += 1
            print(f'❌ Erro: {e}')
        
        self._summary()
    
    def _move(self, f):
        for cat, info in self.cfg['categories'].items():
            if any(str(f).lower().endswith(ext) for ext in info['extensions']):
                dst_dir = self.src / cat
                
                if not dst_dir.exists() and not self.dry:
                    dst_dir.mkdir()
                
                dst = dst_dir / f.name
                
                if dst.exists():
                    if self.cfg['options']['handle_duplicates'] == 'skip':
                        self.stats['skip'] += 1
                        return
                    elif self.cfg['options']['handle_duplicates'] == 'rename':
                        dst = dst_dir / f"{f.stem}_{Path.cwd().name}{f.suffix}"
                        self.stats['moved'] += 1
                
                if not self.dry:
                    shutil.move(str(f), str(dst))
                
                print(f"✅ {f.name} → {cat}/")
                self.stats['moved'] += 1
                return
        
        print(f"⚠️  {f.name} - sem categoria")
    
    def _summary(self):
        print(f"\n{'='*40}")
        print(f"✅ Movidos: {self.stats['moved']}")
        print(f"⏭️  Pulados: {self.stats['skip']}")
        print(f"❌ Erros: {self.stats['err']}")
        print(f"{'='*40}\n")

def main():
    p = argparse.ArgumentParser(description='Organizador de Arquivos')
    p.add_argument('path', help='Caminho da pasta')
    p.add_argument('-c', '--config', help='Arquivo config', default=None)
    p.add_argument('-v', '--verbose', action='store_true', help='Modo verbose')
    p.add_argument('--dry-run', action='store_true', help='Simular')
    
    args = p.parse_args()
    org = Org(args.path, args.config, args.verbose, args.dry_run)
    org.organize()

if __name__ == '__main__':
    main()

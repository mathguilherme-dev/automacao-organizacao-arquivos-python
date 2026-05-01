#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup.py para o Organizador de Arquivos
Facilita instalação e distribuição do pacote
"""

from setuptools import setup, find_packages
from pathlib import Path

# Ler README
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ''

setup(
    name='organizador',
    version='1.0.0',
    author='Seu Nome',
    author_email='seu.email@example.com',
    description='Sistema automático de organização de arquivos por extensão',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/seu-usuario/organizador',
    packages=find_packages(),
    package_data={
        'organizador': ['config.json'],
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'organizador=organizador.cli:main',
        ],
    },
)

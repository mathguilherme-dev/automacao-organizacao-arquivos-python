Plano: Refatoração e Modularização do Organizador de Arquivos

Resumo:  
O objetivo é transformar o script monolítico em um projeto modular, robusto e pronto para empacotamento como executável (.exe), facilitando o uso em múltiplos computadores e cenários. O novo design será orientado a configuração, com tratamento de erros, logging, interface de linha de comando e estrutura de pastas clara.

---

Etapas

Fase 1: Estrutura Modular e Configuração
1. Corrigir typo: renomear "Panilhas" para "Planilhas" em código e pastas.
2. Criar estrutura de pacotes:
   - organizador/
     - __init__.py
     - config.py (carregar config.json)
     - organizer.py (classe FileOrganizer)
     - cli.py (interface argparse)
     - logger.py (logging)
     - utils.py (funções auxiliares)
     - config.json (categorias, extensões, opções)
     - tests/ (testes unitários)
3. Implementar arquivo de configuração externo (config.json) para categorias e extensões.
4. Refatorar lógica principal para classe `FileOrganizer` com métodos: organizar, validar caminho, dry-run.
5. Adicionar tratamento básico de erros (try-except, validação de caminhos).

Fase 2: Usabilidade e Robustez
6. Implementar logging estruturado (arquivo e console).
7. Adicionar argparse para CLI: argumentos para pasta origem, dry-run, config customizada, verbose.
8. Implementar modo dry-run (simulação sem mover arquivos).
9. Adicionar tratamento para arquivos duplicados (skip, renomear, sobrescrever).

Fase 3: Testes, Documentação e Empacotamento
10. Criar testes unitários para funções principais.
11. Escrever README detalhado (uso, configuração, empacotamento).
12. Empacotar com PyInstaller (instruções e ajustes para incluir config.json).

---

Arquivos relevantes
- organizador.py (será dividido em vários módulos)
- arquivos/ (estrutura de exemplo, corrigir nome da pasta Planilhas)
- config.json (novo)
- README.md (atualizar)

---

Verificação
1. Testar organização em diferentes pastas e tipos de arquivos.
2. Validar logs e tratamento de erros.
3. Testar empacotamento e execução do .exe em outro computador.
4. Conferir documentação e exemplos de uso.

---

Decisões
- Modularização para facilitar manutenção e testes.
- Configuração externa para flexibilidade.
- CLI para automação e integração.
- PyInstaller para empacotamento.

---

Considerações Finais
1. Caso deseje interface gráfica, pode ser planejada após CLI estável.
2. Para monitoramento em tempo real, considerar watchdog em versões futuras.
3. O empacotamento pode exigir ajustes de paths relativos/absolutos.

Se desejar, posso detalhar cada etapa ou priorizar alguma fase específica!
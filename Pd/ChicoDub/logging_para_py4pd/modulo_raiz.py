# Em modulo_raiz.py
# Este módulo foi criado para debug de Py4Pd com pacote logging do Python.

import logging

def funcao_teste(logger=None):
    logger = logger or logging.getLogger(__name__)
    logger.info("Esta é uma mensagem de teste do modulo_raiz.")
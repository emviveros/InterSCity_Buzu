import logging

class LogTest:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def funcao_teste(self):
        self.logger.info("Esta é uma mensagem de teste do modulo_raiz_classe.")
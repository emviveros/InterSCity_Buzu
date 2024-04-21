# Falta implementar um mapeamento automático para os níveis de log
# do Python para os níveis de log do Pure Data.
# Também quero que uma vez que eu tenha esse mapeamento, eu possa
# habilitar ou desabilitar os logs de debug de forma dinâmica.


# Em logging_handlers.py
import logging
import pd

class PdErrorHandler(logging.Handler):
    def emit(self, record):
        message = self.format(record)
        pd.error(message)

class PdPrintHandler(logging.Handler):
    def emit(self, record):
        message = self.format(record)
        pd.logpost(3, f"DEBUG (PdPrintHandler): Logger Name: {record.name}")
        pd.print(message)

class PdLogpostHandler(logging.Handler):
    def __init__(self, level=1):
        super().__init__()
        self.level = level

        # Mapeamento de níveis de log
        self.level_map = {
            logging.CRITICAL: 0,  # Fatal
            logging.ERROR: 1,    # Erro
            logging.WARNING: 1,  # Erro (considerando warning como erro no Pd)
            logging.INFO: 2,     # Normal
            logging.DEBUG: 3,    # Debugar
            # logging.NOTSET: 4  # Todos (não é necessário mapear)
        }

    def emit(self, record):
        message = self.format(record)
        pd_level = self.level_map.get(record.levelno, self.level)
        pd.logpost(pd_level, message)



class LogManager:
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)

        # Adicionar atributo para controlar o estado dos logs de debug
        self.debug_enabled = False

        pd.logpost(3,f"Configurando logger {logger_name}. Handlers atuais: {self.logger.handlers}")

        # Verificar se o PdPrintHandler já está configurado
        if not any(isinstance(h, PdPrintHandler) for h in self.logger.handlers):
            self.post_handler = PdPrintHandler()
            self.post_handler.setLevel(logging.INFO)
            self.logger.addHandler(self.post_handler)

        # Evitar propagação de logs
        self.logger.propagate = False

    def get_logger(self):
        return self.logger
    
    def set_debug_enabled(self, enabled):
        """
        Habilita ou desabilita os logs de debug.
        """
        self.debug_enabled = enabled

        # Encontrar o PdPrintHandler
        for handler in self.logger.handlers:
            if isinstance(handler, PdPrintHandler):
                # Definir o nível do handler de acordo com o estado
                if enabled:
                    handler.setLevel(logging.DEBUG)
                else:
                    handler.setLevel(logging.INFO)
                break  # Sair do loop após encontrar o handler
    

# class LogManager:
#     def __init__(self, logger_name):
#         self.logger = logging.getLogger(logger_name)  # Nome do logger a ser manipulado
#         self.logger.setLevel(logging.INFO)

#         # Criar handlers
#         self.console_handler = logging.StreamHandler()
#         self.console_handler.setLevel(logging.INFO)
#         self.error_handler = PdErrorHandler()
#         self.error_handler.setLevel(logging.ERROR)  # Apenas mensagens de erro
#         self.post_handler = PdPrintHandler()
#         self.post_handler.setLevel(logging.INFO)  # Mensagens de INFO e acima

#         # # Formato do log (opcional)
#         formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s - %(message)s')
#         self.console_handler.setFormatter(formatter)
#         self.error_handler.setFormatter(formatter)
#         self.post_handler.setFormatter(formatter)

#         # Adicionar handlers ao logger
#         self.logger.addHandler(self.console_handler)
#         self.logger.addHandler(self.error_handler)
#         self.logger.addHandler(self.post_handler)

#         # Evitar propagação de logs
#         self.logger.propagate = False  # Adicionar esta linha
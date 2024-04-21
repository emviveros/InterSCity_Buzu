# Funciona bem já, porém falta implementar loggs com mapeamento automático para níveis de logs
# do Pure Data. Para isso, será necessário codificar um handler personalizado para o logging do Python. 

import pd
import modulo_raiz
import modulo_raiz_classe

# Importar LogManager
from logging_handlers import LogManager

def logging_teste():
    # Obter o logger
    log_manager_test = LogManager('teste')
    logger = log_manager_test.get_logger()

    # Chamar a função de teste do modulo_raiz
    modulo_raiz.funcao_teste(logger)

    # Registrar uma mensagem de log em buzuDados.py
    # logger.info("Esta é uma mensagem de teste do buzuDados.py.")

def logging_teste_classe():
    # Obter o logger
    log_manager_test = LogManager('teste_classe')
    logger = log_manager_test.get_logger()

    # Criar instancia do modulo_raiz_classe com o logger
    modulo_raiz_classe_instancia = modulo_raiz_classe.LogTest(logger)
    
    # Chamar a função de teste do modulo_raiz_classe
    modulo_raiz_classe_instancia.funcao_teste()

def py4pdLoadObjects():
    """
    Carrega os objetos Python para o Py4PD.
    """
    teste_logging = pd.new_object("logging_teste")
    teste_logging.addmethod_bang(logging_teste)
    teste_logging.add_object()

    teste_logging_classe = pd.new_object("logging_teste_classe")
    teste_logging_classe.addmethod_bang(logging_teste_classe)
    teste_logging_classe.add_object()

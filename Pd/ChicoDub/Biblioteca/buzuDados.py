# Estou terminando buscar_linha, apenas que o retorno da função está sendo feito de forma estranha por comportamento do Py4PD
# Sendo discutido em: https://github.com/charlesneimog/py4pd/discussions/91
# Fazer o Help file do objeto para seguir para o próximo

# Em buzuDados.py
import pd
import os
from dotenv import load_dotenv
import api_olhovivo
import pd

# Obter o caminho absoluto para o arquivo .env
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path=dotenv_path)

# Obter o token da API
api_token = os.getenv("API_TOKEN")

# Criar uma instância de api_olhovivo 
api = api_olhovivo.OlhoVivoAPI(api_token)

def autenticar_OlhoVivoAPI():
    return api.authenticate()  # Chamar o método authenticate do módulo api_olhovivo

def buscar_linha(termosBusca):
    info = api.buscar_linha(termosBusca)
    if info != "":
        # Filtrar itens onde 'sl' é 1 (sentido de ida)
        sl1_items = list(filter(lambda item: item['sl'] == 1, info))

        # Filtrar itens onde 'sl' é 2 (sentido de volta)
        sl2_items = list(filter(lambda item: item['sl'] == 2, info))
        
        # Imprimir os resultados
        for item1, item2 in zip(sl1_items, sl2_items):
            pd.out(f"{item1['cl']} {item1['lc']} {item1['lt']}-{item1['tl']} {item1['tp']}", symbol="", out_n=0)
            pd.out(f"{item2['cl']} {item2['lc']} {item2['lt']}-{item2['tl']} {item2['ts']}", symbol="", out_n=1)    
    else:
        return pd.logpost(1, 'Nenhum resultado encontrado')

def buscar_linha_sentido(codigoLinha_sentido):
    codigoLinha, sentido = codigoLinha_sentido
    info = api.buscar_linha_sentido(codigoLinha, sentido)
    if info != "":        
        # Imprimir os resultados
        for item in info:
            pd.out(f"{item['cl']} {item['lc']} {item['lt']}-{item['tl']} {item['tp']}")  
    else:
        return pd.logpost(1, 'Nenhum resultado encontrado')



def py4pdLoadObjects():
    """
    Carrega os objetos Python para o Py4PD.
    """

    # Adiciona os objetos Python para o Py4PD
    autenticar = pd.new_object("autenticar_OlhoVivoAPI")
    autenticar.addmethod_bang(autenticar_OlhoVivoAPI)
    autenticar.add_object()

    buzuLinha = pd.new_object("buzu.linha")
    buzuLinha.addmethod_anything(buscar_linha)
    # buzuLinha.help_patch = "buzu.linha-help.pd"
    buzuLinha.n_extra_outlets = 1
    buzuLinha.add_object()

    buzuLinhaSentido = pd.new_object("buzu.linha.sentido")
    buzuLinhaSentido.addmethod_list(buscar_linha_sentido)
    # buzuLinhaSentido.help_patch = "buzu.linha.sentido-help.pd"
    buzuLinhaSentido.add_object()




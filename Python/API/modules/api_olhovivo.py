# ToDo:
#  - Verificar como chegam esses arquivos KMZ e fazer com que os métodos:
#       velocidade_media_cidade
#       velocidade_media_corredor
#       velocidade_media_outras_vias
#    retornem dicionários como os outros métodos.

import requests

class OlhoVivoAPI:
    """
    Classe para interagir com a API do Olho Vivo.
    Ref.: https://www.sptrans.com.br/desenvolvedores/api-do-olho-vivo-guia-de-referencia/documentacao-api/#docApi-acesso
    Acesso em: 24/03/2024
    """

    def __init__(self, token):
        """
        Inicializa a classe com o token fornecido e autentica o usuário.

        Args:
            token (str): O token de autenticação para a API do Olho Vivo.
        """
        self.base_url = 'http://api.olhovivo.sptrans.com.br/v2.1'
        self.token = token
        self.headers = {'Content-Type': 'application/json'}
        self.authenticate()

    def post(self, endpoint, data={}):
        """
        Faz uma requisição POST para o endpoint fornecido com os dados fornecidos e retorna a resposta como JSON.

        Args:
            endpoint (str): O endpoint da API para o qual a requisição POST deve ser feita.
            data (dict, opcional): Um dicionário contendo os dados a serem enviados na requisição POST.

        Returns:
            dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
        """
        response = requests.post(f'{self.base_url}{endpoint}', headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Falha na requisição POST para {endpoint}.')
            return None

    def authenticate(self):
        """
        Autentica o usuário usando o token fornecido.

        Returns:
            None. Imprime uma mensagem indicando se a autenticação foi bem-sucedida ou não.
        """
        response = requests.post(f'{self.base_url}/Login/Autenticar?token={self.token}')
        if response.status_code == 200:
            print('Autenticação bem-sucedida!')
            self.headers['Cookie'] = response.headers['Set-Cookie']
        else:
            print('Falha na autenticação.')

    def get(self, endpoint):
        """
        Faz uma requisição GET para o endpoint fornecido e retorna a resposta como JSON.

        Args:
            endpoint (str): O endpoint da API para o qual a requisição GET deve ser feita.

        Returns:
            dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
        """
        response = requests.get(f'{self.base_url}{endpoint}', headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Falha na requisição GET para {endpoint}.')
            return None

    def buscar_linha(self, termosBusca):
        """
        Realiza uma busca das linhas do sistema com base no parâmetro informado.
        Se a linha não é encontrada então é realizada uma busca fonetizada na denominação das linhas.

        Args:
            termosBusca (str): Aceita denominação ou número da linha (total ou parcial).
                               Exemplo: 8000, Lapa ou Ramos

        Returns:
            dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
                [int]      cl: Código identificador da linha. Este é um código identificador único de cada
                               linha do sistema (por sentido de operação)
                [bool]     lc: Indica se uma linha opera no modo circular (sem um terminal secundário)
                [string]   lt: Informa a primeira parte do letreiro numérico da linha
                [int]      tl: Informa a segunda parte do letreiro numérico da linha, que indica se a linha opera nos modos:
                               BASE (10), ATENDIMENTO (21, 23, 32, 41)
                [int]      sl: Informa o sentido ao qual a linha atende, onde 1 significa Terminal Principal para 
                               Terminal Secundário e 2 para Terminal Secundário para Terminal Principal
                [string]   tp: Informa o letreiro descritivo da linha no sentido Terminal Principal para Terminal Secundário
                [string]   ts: Informa o letreiro descritivo da linha no sentido Terminal Secundário para Terminal Principal
        """
        return self.get(f'/Linha/Buscar?termosBusca={termosBusca}')
    
    def buscar_linha_sentido(self, codigoLinha, sentido):
        """
        Busca informações sobre o sentido da linha fornecida.

        Args:
            codigoLinha (str): O código da linha.
            sentido (str): O sentido da linha (1- ida ou 2-volta).

        Returns:
            dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
                [int]      cl: Código identificador da linha. Este é um código identificador único de cada
                               linha do sistema (por sentido de operação)
                [bool]     lc: Indica se uma linha opera no modo circular (sem um terminal secundário)
                [string]   lt: Informa a primeira parte do letreiro numérico da linha
                [int]      tl: Informa a segunda parte do letreiro numérico da linha, que indica se a linha opera nos modos:
                               BASE (10), ATENDIMENTO (21, 23, 32, 41)
                [int]      sl: Informa o sentido ao qual a linha atende, onde 1 significa Terminal Principal para 
                               Terminal Secundário e 2 para Terminal Secundário para Terminal Principal
                [string]   tp: Informa o letreiro descritivo da linha no sentido Terminal Principal para Terminal Secundário
                [string]   ts: Informa o letreiro descritivo da linha no sentido Terminal Secundário para Terminal Principal
        """
        return self.get(f'/Linha/BuscarLinhaSentido?termosBusca={codigoLinha}&sentido={sentido}')

    def buscar_paradas(self, termosBusca):
        """
        Realiza uma busca fonética das paradas de ônibus do sistema com base no parâmetro informado.
        A consulta é realizada no nome da parada e também no seu endereço de localização.
        
        Args:
            termosBusca (str): Aceita nome da parada ou endereço de localização (total ou parcial).
                               Exemplo: Afonso, ou Balthazar da Veiga
        Returns:
            dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
                [int] cp: Código identificador da parada
                [string] np: Nome da parada
                [string] ed: Endereço de localização da parada
                [double] py: Latitude da parada
                [double] px: Longitude da parada
        """
        return self.get(f'/Parada/Buscar?termosBusca={termosBusca}')

    def buscar_paradas_por_linha(self, codigoLinha):
        """
        Realiza uma busca por todos os pontos de parada atendidos por uma determinada linha.

        Args:
            codigoLinha (int): Código identificador da linha. Este é um código identificador único de
                               cada linha do sistema (por sentido) e pode ser obtido através
                               do método buscar_linha da categoria Linhas

        Returns:
            dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
                [int]      cp: Código identificador da parada
                [string]   np: Nome da parada
                [string]   ed: Endereço de localização da parada
                [double]   py: Latitude da parada
                [double]   px: Longitude da parada
        """
        return self.get(f'/Parada/BuscarParadasPorLinha?codigoLinha={codigoLinha}')
   
    def buscar_corredores(self):
        """
        Retorna uma lista com todos os corredores inteligentes.

        Returns:
            dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
                [int]       cc: Código identificador da corredor. Este é um código identificador único de cada corredor inteligente do sistema
                [string]    nc: Nome do corredor
        """
        return self.get('/Corredor')

    def buscar_paradas_por_corredor(self, codigoCorredor):
        """
        Retorna a lista detalhada de todas as paradas que compõem um determinado corredor.

        Args:
            codigoCorredor (str): Código identificador do corredor. Este é um código identificador único
                                  de cada corredor do sistema e pode ser obtido através do método buscar_corredores
        Returns:
            dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
                [int]       cp Código identificador da Parada.
                [string]    np: Nome da parada
                [string]    ed: Endereço de localização da parada
                [double]    py: Latitude da parada
                [double]    px: Longitude da parada
        """
        return self.get(f'/Parada/BuscarParadasPorCorredor?codigoCorredor={codigoCorredor}')

    def buscar_empresas(self):
        """
        Retorna uma lista com todas as empresas operadoras de transporte.

        Returns:
            dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
                [string]    hr: Horário de referência da geração das informações
                [{}]        e: Relação de empresas por área de operação
                    [int]   a: Código da área de operação
                    [{}]    e: Relação de empresa
                        [int]   a: Código da área de operação
                        [int]   c: Código de referência da empresa
                        [string] n: Nome da empresa
        """
        return self.get('/Empresa')
    
    def posicao_veiculos(self):
        """
        Retorna uma lista completa com a última localização de todos os veículos mapeados com suas devidas posições lat / long

        Returns:
            dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
                hr (string): Horário de referência da geração das informações
                ([])        l: Relação de linhas localizadas onde:
                    [string]    c: Letreiro completo
                    [int]       cl: Código identificador da linha
                    [int]       sl: Sentido de operação onde 1 significa de Terminal Principal para Terminal Alternativo e
                                    2 significa de Terminal Alternativo para Terminal Principal
                    [string]    lt0: Letreiro de destino da linha
                    [string]    lt1: Letreiro de origem da linha
                    [int]       qv: Quantidade de veículos localizados
                    [{}]        vs: Relação de veículos localizados, onde:
                            [int]   p: Prefixo do veículo
                            [bool]  a: Indica se o veículo é (true) ou não (false) acessível para pessoas com deficiência
                            [string] ta: Indica o horário universal (UTC) em que a localização foi capturada.
                                         Essa informação está no padrão ISO 8601
                            [double] py: Informação de latitude da localização do veículo
                            [double] px: Informação de longitude da localização do veículo
        """
        return self.get('/Posicao')

    def posicao_linha(self, codigoLinha):
        """
        Retorna uma lista com todos os veículos de uma determinada linha com suas devidas posições lat / long

        Args:
            codigoLinha (int): Código identificador da linha. Este é um código identificador único de cada linha do sistema
                               (por sentido de operação) e pode ser obtido através do método buscar_linha.
        Returns:
            dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
                [string]    hr: Horário de referência da geração das informações
                [{}]        vs: Relação de veículos localizados, onde:
                    [int]   p: Prefixo do veículo
                    [bool]  a: Relação de empresa
                        [int]    a:  Indica se o veículo é (true) ou não (false) acessível para pessoas com deficiência
                        [int]    c:  Código de referência da empresa
                        [string] ta: Indica o horário universal (UTC) em que a localização foi capturada.
                                     Essa informação está no padrão ISO 8601
                        [double] py: Informação de latitude da localização do veículo
                        [double] px: Informação de longitude da localização do veículo
        """
        return self.get(f'/Posicao/Linha?codigoLinha={codigoLinha}')
    
    def posicao_garagem(self, codigoEmpresa, codigoLinha=None):
        """
        Retorna uma lista com todos os veículos de uma determinada empresa em suas respectivas garagens

        Args:
            codigoEmpresa (int): Código identificador da empresa. Este é um código identificador único que
                                 pode ser obtido através do método buscar_empresas.
            codigoLinha (int, opcional): Código identificador da linha. Este é um código identificador único
                                         de cada linha do sistema (por sentido de operação) e pode ser obtido
                                         através do método buscar_linha. Se não for informado, a API retornará
                                         todos os veículos da empresa.
        Returns:
            dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
                [string]    hr: Horário de referência da geração das informações
                [{}]        l: Relação de linhas localizadas onde:
                    [string] c:   Letreiro completo
                    [int]    cl:  Código identificador da linha
                    [int]    sl:  Sentido de operação onde 1 significa de Terminal Principal para
                                  Terminal Secundário e 2 de Terminal Secundário para Terminal Principal
                    [string] lt0: Letreiro de destino da linha
                    [string] lt1: Letreiro de origem da linha
                    [int]    qv:  Quantidade de veículos localizados
                    [{}]     vs: Relação de veículos localizados, onde:
                        [int]    p:  Prefixo do veículo
                        [bool]   a:  Indica se o veículo é (true) ou não (false) acessível para pessoas com deficiência
                        [string] ta: Indica o horário universal (UTC) em que a localização foi capturada.
                                     Essa informação está no padrão ISO 8601
                        [double] py: Informação de latitude da localização do veículo
                        [double] px: Informação de longitude da localização do veículo
        """
        if codigoLinha:
            return self.get(f'/Posicao/Garagem?{codigoEmpresa}=0&{codigoLinha}=0')
        else:
            return self.get(f'/Posicao/Garagem?{codigoEmpresa}=0')
    
    def previsao_chegada(self, codigoParada, codigoLinha):
        """ 
        Retorna uma lista com a previsão de chegada dos veículos da linha informada que atende ao
        ponto de parada informado.

        Args:
            codigoParada (int): Código identificador da parada. Este é um código identificador único de cada
                                ponto de parada do sistema (por sentido) e pode ser obtido através do
                                método buscar_paradas
            codigoLinha (int): Código identificador da linha. Este é um código identificador único de cada
                               linha do sistema (por sentido) e pode ser obtido através do método buscar_linha
        Returns:
           dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
                [string]    hr: Horário de referência da geração das informações
                {}          p:  Representa um ponto de parada onde:
                    [int]    cp:  Código identificador da parada
                    [string] np:  Nome da parada
                    [double] py: Informação de latitude da localização do veículo
                    [double] px: Informação de longitude da localização do veículo
                    [{}]     vs: Relação de veículos localizados, onde:
                        [int]    p:  Prefixo do veículo
                        [string] t:  Horário previsto para chegada do veículo no ponto de parada relacionado
                        [bool]   a:  Indica se o veículo é (true) ou não (false) acessível para pessoas com deficiência
                        [string] ta: Indica o horário universal (UTC) em que a localização foi capturada.
                                     Essa informação está no padrão ISO 8601
                        [double] py: Informação de latitude da localização do veículo
                        [double] px: Informação de longitude da localização do veículo
        """
        return self.get(f'/Previsao?codigoParada={codigoParada}&codigoLinha={codigoLinha}')
    
    def previsao_chegada_linha(self, codigoLinha):
        """
        Retorna uma lista com a previsão de chegada de cada um dos veículos da linha informada em todos
        os pontos de parada aos quais que ela atende.

        Args:
            codigoLinha (int): Código identificador da linha. Este é um código identificador único de cada
                               linha do sistema (por sentido) e pode ser obtido através do método buscar_linha
        
        Returns:
            dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
                [string]    hr: Horário de referência da geração das informações
                [{}]        ps: Representa uma relação de pontos de parada onde:
                    [int]    cp: Código identificador da parada
                    [string] np: Nome da parada
                    [double] py: Informação de latitude da localização do veículo
                    [double] px: Informação de longitude da localização do veículo
                    [{}]     vs: Relação de veículos localizados, onde:
                        [int]    p:  Prefixo do veículo
                        [string] t:  Horário previsto para chegada do veículo no ponto de parada relacionado
                        [bool]   a:  Indica se o veículo é (true) ou não (false) acessível para pessoas com deficiência
                        [string] ta: Indica o horário universal (UTC) em que a localização foi capturada.
                                     Essa informação está no padrão ISO 8601
                        [double] py: Informação de latitude da localização do veículo
                        [double] px: Informação de longitude da localização do veículo
        """
        return self.get(f'/Previsao/Linha?codigoLinha={codigoLinha}')
    
    def previsao_paradas(self, codigoParada):
        """
        Retorna uma lista com a previsão de chegada dos veículos de cada uma das linhas que atendem ao ponto de parada informado.

        Args:
            codigoParada (int): Código identificador da parada. Este é um código identificador único de cada
                                ponto de parada do sistema (por sentido) e pode ser obtido através do
                                método buscar_paradas
        
        Returns:
            dict: A resposta da API convertida em um dicionário Python, ou None se a requisição falhar.
                [string]    hr: Horário de referência da geração das informações
                [{}]        p: Representa um ponto de parada onde:
                    [int]    cp: Código identificador da parada
                    [string] np: Nome da parada
                    [double] py: Informação de latitude da localização do veículo
                    [double] px: Informação de longitude da localização do veículo
                    [{}]     l: Relação de linhas localizadas onde:
                        [string] c:  Letreiro completo
                        [int]    cl:  Código identificador da linha
                        [int]    sl:  Sentido de operação onde 1 significa de Terminal Principal para
                                      Terminal Secundário e 2 de Terminal Secundário para Terminal Principal
                        [string] lt0: Letreiro de destino da linha
                        [string] lt1: Letreiro de origem da linha
                        [int]    qv:  Quantidade de veículos localizados
                        [{}]     vs: Relação de veículos localizados, onde:
                            [int]    p:  Prefixo do veículo
                            [string] t:  Horário previsto para chegada do veículo no ponto de parada relacionado
                            [bool]   a:  Indica se o veículo é (true) ou não (false) acessível para pessoas com deficiência
                            [string] ta: Indica o horário universal (UTC) em que a localização foi capturada.
                                        Essa informação está no padrão ISO 8601
                            [double] py: Informação de latitude da localização do veículo
                            [double] px: Informação de longitude da localização do veículo
        """
        return self.get(f'/Previsao/Parada?codigoParada={codigoParada}')
    
    def get_kmz(self, endpoint):
        """
        Busca um arquivo KMZ a partir de um endpoint específico.

        Args:
            endpoint (str): O endpoint da API para o qual a requisição GET deve ser feita.

        Returns:
            str: O caminho para o arquivo KMZ baixado, ou None se a requisição falhar.
        """
        response = requests.get(f'{self.base_url}/{endpoint}', headers=self.headers)
        if response.status_code == 200:
            filename = endpoint.split('/')[-1] + '.kmz'
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
        else:
            print(f'Falha na requisição GET para {endpoint}.')
            return None

    def velocidade_media_cidade(self, sentido=None):
        """
        Retorna o mapa completo da cidade contendo um mapa de fluidez da cidade com a velocidade média
        e tempo de percurso de cada trecho envolvido.

        Args:
            sentido (string): Se desejar a informação separada de um único sentido será preciso indicar aqui.
                              Os valores possíveis são:
                               BC - veículos saindo do bairro em direção ao centro
                               CB - veículos saindo do centro em direção ao bairro

        Return:
            str: O caminho para o arquivo KMZ baixado, ou None se a requisição falhar.
        """
        if sentido:
            return self.get_kmz(f'/KMZ/{sentido}')
        else:
            return self.get_kmz('/KMZ')
    
    def velocidade_media_corredor(self, sentido=None):
        """
        Retorna o mapa completo de todos os corredores da cidade contendo um mapa de fluidez da cidade
        com a velocidade média e tempo de percurso de cada trecho envolvido.

        Args:
            sentido (string): Se desejar a informação separada de um único sentido será preciso indicar aqui.
                              Os valores possíveis são:
                               BC - veículos saindo do bairro em direção ao centro
                               CB - veículos saindo do centro em direção ao bairro

        Return:
            str: O caminho para o arquivo KMZ baixado, ou None se a requisição falhar.
        """
        if sentido:
            return self.get_kmz(f'/KMZ/Corredor/{sentido}')
        else:
            return self.get_kmz('/KMZ/Corredor')
    
    def velocidade_media_outras_vias(self, sentido=None):
        """
        Retorna o mapa completo com as vias importantes da cidade (exceto corredores) da cidade contendo
        um mapa de fluidez da cidade com a velocidade média e tempo de percurso de cada trecho envolvido.

        Args:
            sentido (string): Se desejar a informação separada de um único sentido será preciso indicar aqui.
                              Os valores possíveis são:
                               BC - veículos saindo do bairro em direção ao centro
                               CB - veículos saindo do centro em direção ao bairro

        Return:
            str: O caminho para o arquivo KMZ baixado, ou None se a requisição falhar.
        """
        if sentido:
            return self.get_kmz(f'/KMZ/OutrasVias/{sentido}')
        else:
            return self.get_kmz('/KMZ/OutrasVias')
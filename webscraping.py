from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

class WebScraping():

    def __init__(self, url, arquivo):
        # Alocando argumentos
        self.url = url
        self.nome_arquivo = arquivo

        # Inicializando objetos
        self.site = None
        self.navegador = None
        self.monitores = None
        self.dados_monitores = []

        # Expecifica configurações de inicialização do navegador -- Selenium
        self.options = Options()
        self.options.add_argument('window-size=maximized')  # Dimensões da janela aberta
        self.options.add_experimental_option("detach", True) # Manter o Chrome aberto
        ## self.options.add_argument('--headless')  # Realiza a rotina sem abrir o navegador

        print('Web Scraping inicializado!')

    def get_url(self):
        # Indicando a automação do Chrome 
        self.navegador = webdriver.Chrome(options=self.options)
        self.navegador.get(self.url)

        sleep(3)

    def navegacao(self):
        botao_exibir = self.navegador.find_element(By.XPATH, "//*[@id='Filter']/label/select")
        sleep(1)
        botao_exibir.click()
        sleep(1)
        botao_100 = self.navegador.find_element(By.XPATH, "//*[@id='Filter']/label/select/option[5]")
        sleep(1)
        botao_100.click()
        sleep(4)

    def integracao_bs(self):
        # Início da integração do BeautifulSoup
        self.site = BeautifulSoup(self.navegador.page_source, 'html.parser')

    def identifica_box(self):
        # Identificação do atributo raiz do anúncio
        self.monitores = self.site.findAll('div', class_='sc-ff8a9791-7 dZlrn productCard')

    def raspagem_dados(self):     
        # Automação da busca dos monitores 
        for monitor in self.monitores:
            monitor_modelo = monitor.find('span', class_='sc-d99ca57-0 iRparH sc-ff8a9791-16 kRYNji nameCard').get_text()
            monitor_preco_aparente = True
            if monitor_preco_aparente:
                try:
                    monitor_preco = monitor.find('span', class_='sc-3b515ca1-2 jTvomc priceCard').get_text()[3:]
                except Exception as e:
                    print(e)
                    pass
                    
            monitor_url = monitor.find('a', href=True)
            monitor_url = f"www.kabum.com.br{monitor_url['href']}"
            
            print('Modelo:', monitor_modelo)
            print('Preço:', monitor_preco)
            print('URL:', monitor_url)

            # Utilizado para quebra de linhas
            print()

            # Criação do DataFrame 
            self.dados_monitores.append([monitor_modelo,
                                        monitor_preco,
                                        monitor_url])

    def prox_pag(self):
        try:
            next_button = self.navegador.find_element(By.XPATH, "//*[@id='listingPagination']/ul/li[7]/a")
            botao_vazio = next_button.get_property('disabled')
            if botao_vazio:
                print('Raspagem encerrada com sucesso!')
                return False
            sleep(2)
            next_button.click()
            print('Seguindo para a próxima página:')
            return True
        except Exception as e:
            print(e)

    def criar_tabela(self):
        dados = pd.DataFrame(self.dados_monitores, columns = ['Marca / Modelo',
                                                            'Preço',
                                                            'URL'])
        dados.to_excel(self.nome_arquivo, index = False)
        
if __name__=='__main__':
    kabum = WebScraping(url='https://www.kabum.com.br/computadores/monitores/monitor-gamer', 
                            arquivo='monitor_gamer_11.11.22.xlsx')
    # Execução sequencial de todas as fases do Web Scraping:
    #   1. Pesquisar pelo URL do site kabum/monitores
    kabum.get_url()
    print('get_url executado com sucesso:')
    kabum.navegacao()
    print('navegação executada com sucesso:')

    ## Laço de Paginação
    botao_prox_pag = True
    while botao_prox_pag:
        #   2. Interpretar o HTML da página
        kabum.integracao_bs()
        print('integracao_bs executado com sucesso:')
        #   3. Indentica a raiz do anúncio
        kabum.identifica_box() 
        print('identifica_box executado com sucesso:')
        #  4. Listar anúncios da página atual
        kabum.raspagem_dados()
        print('raspagem de dados executada com sucesso:')
        sleep(2)
        #  5. Seguir para a próxima página
        botao_prox_pag = kabum.prox_pag()
        sleep(3)

    #   6. Criar tabela com dataframe
    kabum.criar_tabela()
    print('criar tabela executado com sucesso:')
    print('Web Scraping concluído!')


   
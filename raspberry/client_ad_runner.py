import paho.mqtt.client as mqtt
from threading import Thread
from ast import literal_eval
import ADS1256
import config
from queue import Queue
from extract_data import run



class My_client_ad(Thread):
    
    '''
    Classe usada para representar um cliente ativo
    
    Atributo-
    --------
    
    broker : ...
    port : ...
    topic : ...
    client : ...
    userdata : ...
    msg : ...
    
    Metodos-
    -------
    
    on_connect : manter a conexão e a inscrição do cliente ao tópico
    on_message : responsavel pelo envio e requisição da menssagem
    run : iniciar o cliente
    
    '''

    def __init__(self, broker, port, topic):
        
        '''
        -Construtor da classe para definir parametro inicias no momento da instancia-
        Parametros:
        
         broker : endereço do servidor broker.
         port : porta para comunicação do broker.
         topic : tópico para inscrição e publicação da menssagem.
         
        '''
        Thread.__init__(self)
        self.broker = broker
        self.port = port
        self.topic = topic
        self.q = Queue() # recursos de criação da fila para requisitar os dados na memoria 
        self.t1 = Thread(target=run, args=(self.q,))
        
        

    def on_connect(self, client, userdata, flags, rc):
        
        '''
        -Determina o metodo de conexão do cliente, passando o tópico a ser inscrito-
        Parametros:
         
         client : objeto cliente
         userdata : parametro de callbacks para atualização 
         flags : sinalizador do broker
         rc : resultado da conexão
        '''
        client.subscribe(self.topic) # assinatura do tópico 

    def on_message(self, client, userdata, msg):
        print("[MSG RECEBIDA] Topico: "+msg.topic+" / Mensagem: "+str(msg.payload.decode('utf-8')))
        
        
        if msg.payload.decode('utf-8') == "on": # Verifica se a menssagem recebida para o inicio da leitura
            self.t1.start() # inicia a leitura do dispositivo
            print("leitura iniciada")

        if msg.payload.decode("utf-8") == "off": # Verifica se a menssagem recebida para o inicio da leitura
            
            self.t1.do_run=False #término da leitura do dispositivo
            self.t1.join()
            data = self.q.get()# armazena os dados na variavel data
            self.t1 = Thread(target=run, args=(self.q,))
            client.publish('request', str(data))# publica os dados ao tópico request
            print('finalizado')
            
            
    def run(self):
        print("[STATUS] Inicializando MQTT...")

        client = mqtt.Client('113')
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.broker, self.port)
        client.loop_forever()

if __name__ == "__main__":
    my = My_client_ad('broker.emqx.io', 1883, 'ad')
    my.start()

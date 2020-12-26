import paho.mqtt.client as mqtt
from PyQt5.QtCore import QThread, pyqtSignal
from ast import literal_eval


class Receive_from_ad(QThread):
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

    data_signal = pyqtSignal(dict) #envio de dados entre memorias

    #Classe necessária para manter o ativo.
    
    def __init__(self, broker, port, topic, parent=None):
        '''
        -Construtor da classe para definir parametro inicias no momento da instancia-
        Parametros:
        
         broker : endereço do servidor broker.
         port : porta para comunicação do broker.
         topic : tópico para inscrição e publicação da menssagem.
         
        '''
        super(Receive_from_ad, self).__init__(parent)
        self.broker = broker
        self.port = port
        self.topic = topic
        print("[STATUS] Inicializando MQTT...")
        #inicializa MQTT:
        self.client = mqtt.Client('100101')
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port)


    def on_connect(self, client, userdata, flags, rc):
        '''
        -Determina o metodo de conexão do cliente, passando o tópico a ser inscrito-
        Parametros:
         
         client : objeto cliente
         userdata : parametro de callbacks para atualização 
         flags : sinalizador do broker
         rc : resultado da conexão
        '''
        client.subscribe(self.topic)
 
    
    def on_message(self, client, userdata, msg):
        '''
        -Determina o metodo de menssagem, onde sera recebida e enviada-
        Parametros:
         
         client : objeto cliente
         userdata : parametro de callbacks para atualização 
         msg : menssagem recebida em formato byte string
        '''
        self.data_signal.emit(literal_eval(msg.payload.decode('utf-8')))
        
        
        
        
    def run(self):
        #inicializa o cliente no momento que o objeto utiliza o metodo "start()"
        self.client.loop_forever()
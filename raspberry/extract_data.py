import ADS1256
import RPi.GPIO as GPIO
import threading
import time
import numpy as np



def run(instance):
    """
    Função de inicialização d eleitura
    
    data : armazena os dados recebidos do medidor
    timer : armazena o tempo entre as amostras
    """
    data = []
    timer = []
    
    th1 = threading.currentThread()
    ADC = ADS1256.ADS1256() #instancia do A/D
    ADC.ADS1256_init() #inicialização do A/D
    start_timer = time.time() #inicio do temporizador
    
    while getattr(th1, "do_run", True):
        data.append(round(ADC.ADS1256_GetSingleChannel(0)*5.0/0x7fffff,2))
    end_timer = time.time() #término do temporizador
    final = end_timer-start_timer #delta do tempo inicial-final
    
    instance.put({'data':data,'time':list(np.linspace(0,final,len(data)))}) #envio de dados através de fila de memorias
    print("""             |================TEST====================|
             |numero de amostras: {}                |
             |tempo de leitura: {}s                 |
             |spi_clock: 2,2Mhz                       |
             |canais liberados: 1                     |
             |sincronismo_mux: desabilitado           |
             |========================================|""".format(len(data), round(final,2)))

    GPIO.cleanup()

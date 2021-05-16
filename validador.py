import math
import numpy as np

from config import LIMIAR_ACEITACAO_GABRIEL

from config import LIMIAR_DUVIDA_GABRIEL

from config import N_CLUSTERS

from utils import carrega_json_auxiliar
from utils import carrega_cluster_centers

################# Arquivo responsavel por validar audio de entrada #################

def calcula_soma_rmse(locutor):
    
    #Recupera os mfccs salvos extraidos do audio a ser testado
    mfccs = carrega_json_auxiliar()

    mfcss_teste = np.array(mfccs["mfcc"])
    print('Shape mfccs 2D ', mfcss_teste.shape)

    # Carrega os cluster_centers do locutor
    cluster_centers = carrega_cluster_centers(locutor)

    soma_total_rmse = 0
    # for para cada array de mfccs
    for i in range(len(mfcss_teste)):
        soma_rmse_vetor = 0
        vetor_mfcc = mfcss_teste[i]

        # Calculo a soma de rmse's de cada cluster center em relação ao vetor mfcc da vez
        for key in cluster_centers:
            cc = cluster_centers[key]

            # Calcula a raiz do erro médio quadrático do vetor ao center cluster
            soma_rmse_vetor += rmse(vetor_mfcc, cc)

        print('Raiz do erro quadrático médio - RMSE: ', soma_rmse_vetor)

        # Divido a soma dos mse's pela quantidade de clusters
        media_rmse_vetor = soma_rmse_vetor / N_CLUSTERS   

        #  
        soma_total_rmse += media_rmse_vetor

    # Média total é a soma total dividido pelo total de vetores MFCCs
    media_total_rmse = soma_total_rmse / len(mfcss_teste)

    return media_total_rmse


def rmse(v1, v2):
    dim, soma = len(v1), 0
    for i in range(dim):
        ao_quadrado = math.pow(v1[i] - v2[i], 2)
        soma += ao_quadrado

    dist = math.sqrt(soma / dim) #dividir por numero de clusters
    print('RMSE: ', dist)
    return dist

def valida_voz(locutor, retorna_soma=False):
    soma_rmse = calcula_soma_rmse(locutor)
    print('Raiz da soma dos erros quadráticos médios ', soma_rmse)
    result = testa_limiar(soma_rmse, locutor)
    
    if retorna_soma:
        return result, soma_rmse
    else:
        return result


# retorna 1 se valida o locutor
# retorna 2 se indeterminação
# retorna 3 se não valida locutor
def testa_limiar(soma_rmse, locutor):
  limiar_aceitacao = get_limiar_aceitacao(locutor)
  limiar_duvida = get_limiar_duvida(locutor)

  if soma_rmse <= limiar_aceitacao:
    return 1
  elif (soma_rmse > limiar_aceitacao and soma_rmse <= limiar_duvida):
    return 2
  else:
    return 3

def get_limiar_aceitacao(locutor):
    if locutor == 'Gabriel':
        return LIMIAR_ACEITACAO_GABRIEL

def get_limiar_duvida(locutor):
    if locutor == 'Gabriel':
        return LIMIAR_DUVIDA_GABRIEL
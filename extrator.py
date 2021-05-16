import os
import json
import librosa
import python_speech_features
from scipy.signal.windows import hamming

from sklearn.cluster import KMeans

from utils import format_json_path_file

from config import NUM_FFT
from config import NUM_MFCC
from config import N_CLUSTERS
from config import HOP_LENGTH
from config import SAMPLE_RATE

from config import F_MIN
from config import F_MAX
from config import N_MELS
from config import PREEMPH
from config import CEPLIFTER 

from config import ARRAY_LOCUTORES

from config import DATASET_PATH
from config import JSON_MFCC_PATH_BASE
from config import CLUSTER_CENTERS_PATH

################# Arquivo responsável por extrair os mfccs de cada locutor existente na base #################
# Metodo para extrair e armazenar os mfccs
def save_mfcc():

    data = {
        "mapping": '',
        "mfcc": []
    }

    locutores = ARRAY_LOCUTORES

    for (dirpath, dirnames, filenames) in os.walk(DATASET_PATH):
        
        pasta = dirpath.split("/")[-1]
        locutor = dirpath.split("/")[-2]

        if(pasta == 'treino' and locutor in locutores):

            print("\nDirpath ", dirpath)
            print("Locutor ", locutor)

            # salva o nome do locutor 
            data["mapping"] = locutor
            
            print("\nProcessando: {}".format(locutor))

            # processa todos os arquivos de áudio do locutor da pasta de treino
            for f in filenames:

                # carrega o áudio
                file_path = os.path.join(dirpath, f)
                signal, sample_rate = librosa.load(file_path, sr=SAMPLE_RATE)

                duracao = librosa.get_duration(y=signal, sr=sample_rate) # em segundos
                print("Duração do áudio: {}".format(duracao))

                print("Tamanho do sinal: {} frames".format(len(signal)))

                print("Iniciando processamento do arquivo: {}".format(file_path))
                
                mfcc = python_speech_features.mfcc(signal=signal, samplerate=SAMPLE_RATE, winlen=NUM_FFT / SAMPLE_RATE, winstep=HOP_LENGTH / SAMPLE_RATE,
                                          numcep=NUM_MFCC, nfilt=N_MELS, nfft=NUM_FFT, lowfreq=F_MIN, highfreq=F_MAX,
                                          preemph=PREEMPH, ceplifter=CEPLIFTER, appendEnergy=True, winfunc=hamming)

                
                print("Shape MFCC ", mfcc.shape)

                data["mfcc"].append(mfcc.tolist())
                print("{} PROCESSADO!".format(file_path))

            # salva MFCCs em um arquivo json
            with open(format_json_path_file(JSON_MFCC_PATH_BASE, locutor), "w") as fp:
                json.dump(data, fp, indent=4)
            
            print("MFCCs do locutor {} salvos!".format(locutor))

            save_cluster_centers_locutor(locutor, mfcc)


# Metodo para treinar o kmeans e achar os representantes de cada cluster
# Extrai e salva um vetor de tamanho N_CLUSTERS com os representantes de cada cluster para o locutor
def save_cluster_centers_locutor(locutor, mfcc):

    print("\nIniciando geração dos cluster_centers para o locutor {}".format(locutor))
    print("MFCC de shape ", mfcc.shape) 

    # Cria instancia KMeans
    kmeans = KMeans(n_clusters = N_CLUSTERS, init = 'k-means++', random_state = 42)
        
    # Passa os dados de treino para o KMeans treinar
    kmeans.fit(mfcc)

    # Recupera os cluster_centers gerados
    cluster_centers = kmeans.cluster_centers_.tolist()

    # Cria o dicionario que armazena os representantes
    dicionario = {}
    for i in range (len(cluster_centers)):
        dicionario[str(i)] = cluster_centers[i]
        
    #salva o dicionario
    path = CLUSTER_CENTERS_PATH + '/' + locutor + '.json'
    with open(path, "w") as fp:
        json.dump(dicionario, fp, indent=4)
        print("Cluster Centers do locutor {} salvos com sucesso!".format(locutor))
        print("--------------------------------------------------------")
#Áudio precisa está em formato wav
#sinal vai ser um numpy array de uma dimensão composto por valores do sr * duração do som. São as amplitudes.

if __name__ == '__main__':
   
  #Extraindo as características MFCCs para cada janela, usando superposição
  save_mfcc()
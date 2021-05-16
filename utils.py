import json
import librosa
import python_speech_features

from scipy.signal.windows import hamming

from config import NUM_FFT
from config import NUM_MFCC
from config import HOP_LENGTH
from config import SAMPLE_RATE

from config import F_MIN
from config import F_MAX
from config import N_MELS
from config import PREEMPH
from config import CEPLIFTER 

from config import JSON_MFCC_PATH_BASE
from config import CLUSTER_CENTERS_PATH
from config import PATH_FILE_MFCC_AUXILIAR
from config import PATH_FILE_AUDIO_AUXILIAR


def formata_nome(nome):
  nome = nome.lower()
  inicial = nome[0].upper()
  return inicial + nome[1:]


# Metodo para extrair e armazenar os mfccs do audio falado pelo usuário ou audio de teste
def save_mfcc_auxiliar(locutor, path=None):

    data = {
        "mapping": '',
        "mfcc": []
    }

    # Salva o nome do locutor
    data["mapping"] = locutor + '-auxiliar'
            
    print("\nProcessando: {}".format(locutor))

    if path == None:
        path = PATH_FILE_AUDIO_AUXILIAR

    signal, sample_rate = librosa.load(path, sr=SAMPLE_RATE)

    duracao = librosa.get_duration(y=signal, sr=sample_rate) # em segundos

    print("Duração do áudio: {}".format(duracao))

    print("Tamanho do sinal: {} frames".format(len(signal)))

    print("Iniciando processamento do arquivo: {}".format(path))

    mfcc = python_speech_features.mfcc(signal=signal, samplerate=SAMPLE_RATE, winlen=NUM_FFT / SAMPLE_RATE, winstep=HOP_LENGTH / SAMPLE_RATE,
                                          numcep=NUM_MFCC, nfilt=N_MELS, nfft=NUM_FFT, lowfreq=F_MIN, highfreq=F_MAX,
                                          preemph=PREEMPH, ceplifter=CEPLIFTER, appendEnergy=True, winfunc=hamming)

    print("MFCCs ", mfcc)                    
    print()
    print("Shape MFCC ", mfcc.shape)

    data["mfcc"] = mfcc.tolist()
    print("{} PROCESSADO!".format(PATH_FILE_AUDIO_AUXILIAR))

    # Salva MFCCs em um arquivo json
    with open(PATH_FILE_MFCC_AUXILIAR, "w") as fp:
        json.dump(data, fp, indent=4)


# Metodo para criar o path do json file que guarda os mfcss
def format_json_path_file(pathBase, name):
    return "{}/{}.json".format(pathBase, name)

def carrega_json_locutor(locutor):
    path_completo = JSON_MFCC_PATH_BASE + '/' + locutor + '.json'
    print("Carregando dados do path: ", path_completo)

    with open(path_completo, "r") as fp:
        data = json.load(fp)

    print("JSON de MFCCS de {} Carregado!".format(locutor))

    return data

def carrega_json_auxiliar():
    with open(PATH_FILE_MFCC_AUXILIAR, "r") as fp:
        data = json.load(fp)

    print("JSON Auxiliar Carregado!")

    return data

def carrega_cluster_centers(locutor):
    path = CLUSTER_CENTERS_PATH + '/' + locutor + '.json'
    with open(path, "r") as fp:
        data = json.load(fp)

    print("Cluster Centers de {} Carregados!".format(locutor))

    return data
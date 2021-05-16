from scipy import signal as sig

###### Arquivo de Configuração - Defina suas variáveis ######

DATASET_PATH = "../Verificador-de-Locutor/Base_de_Dados"
JSON_MFCC_PATH_BASE = "../Verificador-de-Locutor/data_mfccs"
ANALISE_PATH = "../Verificador-de-Locutor/data_analises"
CLUSTER_CENTERS_PATH = "../Verificador-de-Locutor/data_cluster_centers"
PATH_FILE_AUDIO_AUXILIAR  = "../Verificador-de-Locutor/auxiliar/auxiliar.wav"
ANALISE_IMPOSTORES_PATH = "../Verificador-de-Locutor/data_analises/impostores"
PATH_FILE_MFCC_AUXILIAR = "../Verificador-de-Locutor/auxiliar/mfccs_auxiliar.json"

NUM_MFCC = 13
N_CLUSTERS = 64
SAMPLE_RATE = 44100

PERCENT_DUVIDA = 1.05

### Segmentacao e janelamento de 20ms
# 1seg = 44100 samples
# 0,02 seg = 44100 x 0,02 = 882
n_samples_na_janela = int(0.02 * SAMPLE_RATE)

# n_fft = Quantidade de samples da janela aplicada no FFT usado para extrair os MFCCs
NUM_FFT = n_samples_na_janela

# Superposicao de 50% = 20ms / 2 = 10ms
n_samples_na_superposicao = int(n_samples_na_janela / 2)

HOP_LENGTH = n_samples_na_superposicao

F_MIN = 0
F_MAX = None
N_MELS = 40
PREEMPH = 0.97
CEPLIFTER = 0

ARRAY_LOCUTORES = ['Gabriel']

### Limiares de Aceitação e Dúvida ###
LIMIAR_ACEITACAO_GABRIEL = round(4.303673096793665 , 3)
LIMIAR_DUVIDA_GABRIEL = round(LIMIAR_ACEITACAO_GABRIEL * PERCENT_DUVIDA, 3)
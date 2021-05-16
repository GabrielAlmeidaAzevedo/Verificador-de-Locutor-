import os
import json

from numpy.core.numeric import Infinity

from utils import save_mfcc_auxiliar

from validador import valida_voz

from config import ANALISE_PATH
from config import DATASET_PATH
from config import ARRAY_LOCUTORES
from config import ANALISE_IMPOSTORES_PATH

################# Arquivo responsavel por gerar métricas do verificador #################

def formata_resposta(filename, resp):
  if resp == 1:
    return "{};  Validado;".format(filename)
  if resp == 2:
    return "{}; Dúvida;".format(filename)
  if resp == 3:
    return "{}; Invalidado;".format(filename)


# Metodo que gera as metricas com os arquivos de teste
def calcula_para_arquivos_teste(locutor):
  path_teste = DATASET_PATH + '/' + locutor + '/teste'

  print("path teste ", path_teste)

  metricas = {
    'locutor': locutor,
    'valido' : 0,
    'invalido': 0,
    'duvida': 0,
    'media_rmse': 0 ,

    'met_audios' : []
  }

  soma_geral = 0
  for (dirpath, dirnames, filenames) in os.walk(path_teste):
    locutor = dirpath.split("/")[-2]

    for f in filenames:
      print('Gerando métricas para o arquivo ', f)
      save_mfcc_auxiliar(locutor, path_teste + '/' + f)
      resp_validador, soma_rmse = valida_voz(locutor, retorna_soma=True)
      soma_geral += soma_rmse

      if resp_validador == 1:
        metricas['valido'] += 1
      if resp_validador == 0:
        metricas['duvida'] += 1
      if resp_validador == -1:
        metricas['invalido'] += 1

      analise = formata_resposta(f, resp_validador)

      metrica = {
        'analise' : analise,
        'soma_rmse' : soma_rmse
      }

      metricas['met_audios'].append(metrica)

    metricas['media_rmse'] = soma_geral / len(metricas['met_audios'])

    with open(ANALISE_PATH + '/' + locutor + '.json', "w") as js:
      json.dump(metricas, js, indent=4)

  return metricas

# Metodo que calcula as metricas com arquivos dos impostores
def calcula_para_arquivos_impostores(locutor):
  path_impostor = DATASET_PATH + '/' + locutor + '/impostores'

  print("path impostor ", path_impostor)

  metricas = {
    'locutor': locutor,
    'valido' : 0,
    'invalido': 0,
    'duvida': 0,
    'media_rmse': 0 ,
    'met_audios' : []
  }

  for (dirpath, dirnames, filenames) in os.walk(path_impostor):
    locutor = dirpath.split("/")[-2]

    for f in filenames:
      print('Gerando métricas para o arquivo ', f)
      save_mfcc_auxiliar(locutor, path_impostor + '/' + f)
      resp_validador, rmse = valida_voz(locutor, retorna_soma=True)

      if resp_validador == 1:
        metricas['valido'] += 1
      if resp_validador == 0:
        metricas['duvida'] += 1
      if resp_validador == -1:
        metricas['invalido'] += 1

      analise = formata_resposta(f, resp_validador)

      metrica = {
        'analise' : analise,
        'rmse' : rmse
      }

      metricas['met_audios'].append(metrica)

    with open(ANALISE_IMPOSTORES_PATH + '/' + locutor + '_impostores.json', "w") as js:
      json.dump(metricas, js, indent=4)

  return metricas


def gera_metricas_locutor(locutor):
  print("Gerando métricas para {}".format(locutor))

  metricas = calcula_para_arquivos_teste(locutor)

  print("\nMétricas geradas!\n")

  print("Montado relatório ...\n\n")

  print("===================================== Report ========================================")
  printa_report_locutor(metricas)

  print("======================================================================================")

# Metodo que gera as metricas usando impostores para o locutor
def gera_metricas_locutor_impostores(locutor):
  print("Gerando métricas para os impostores de {}".format(locutor))

  metricas = calcula_para_arquivos_impostores(locutor)

  print("\nMétricas dos impostores geradas!\n")

  print("Montado relatório ...\n\n")

  print("================================= Report Impostores ==================================")
  printa_report_locutor_impostores(metricas)

  print("======================================================================================")

def printa_report_locutor_impostores(metricas, listar_audios=True):
  print("**************************************************************************************")
  print("Arquivos de Impostores;")
  print("Locutor; {};".format(metricas['locutor']))
  print("Validados; {};".format(metricas['valido']))
  print("Invalidados; {};".format(metricas['invalido']))
  print("Dúvida; {};".format(metricas['duvida']))
  print(";;")
  print("Arquivo; Status; Distorção(soma RMSE);")

  if listar_audios:
    for met_audio in metricas['met_audios']:
      print(met_audio['analise'] + " {};".format(met_audio['rmse']))

  print()

def calcula_mediana(arr = []):
  arr.sort()
  tam = len(arr)
  mediana = Infinity
  if ((tam % 2) > 0):
    mediana = arr[tam // 2]
  else:
    meio = tam // 2
    mediana = (arr[meio - 1] + arr[meio]) / 2

  return mediana

def printa_report_locutor(metricas):
  print("**************************************************************************************")
  print("Arquivos de Teste;")
  print("Loctor; {};".format(metricas['locutor']))
  print("Validados; {};".format(metricas['valido']))
  print("Invalidados (falso negativo); {};".format(metricas['invalido']))
  print("Dúvida; {};".format(metricas['duvida']))
  print(";;")
  print("Arquivo; Status; Distorção (RMSE);")

  arr = []
  for met_audio in metricas['met_audios']:
    arr.append(met_audio['soma_rmse'])
    print(met_audio['analise'] + " {};".format(met_audio['soma_rmse']))

  mediana = calcula_mediana(arr)
  print(";;")
  print("RMSE médio; ", metricas['media_rmse'], ";")
  print("Mediana; ", mediana, ";")
  print()

def printa_report_locutor_planilha(metricas):
  print("**************************************************************************************")
  print("Locutor; {};".format(metricas['locutor']))
  print("Validados; {};".format(metricas['valido']))
  print("Invalidados (falso Negativo); {};".format(metricas['invalido']))
  print("Dúvida; {};".format(metricas['duvida']))
  print()
  print("Arquivo; Distorção(RMSE); Status;")

  arr = []
  for met_audio in metricas['met_audios']:
    arr.append(met_audio['soma_rmse'])
    print(met_audio['analise'] + "; {}; {};".format(met_audio['soma_rmse'], ))

  arr.sort()
  mediana = (arr[4] + arr[5]) / 2

  print("RMSE médio: ", metricas['media_rmse'])
  print("Mediana: ", mediana)
  print()

# Metodo para montar um report dos audios dos impostores
def get_report_impostores(listar_audios=True):
  print("================================= Report Impostores ==================================")
  for (dirpath, dirnames, filenames) in os.walk(ANALISE_IMPOSTORES_PATH):
    
    for file in filenames:
      with open(ANALISE_IMPOSTORES_PATH + '/' + file, "r") as fp:
        metricas = json.load(fp)
        printa_report_locutor_impostores(metricas, listar_audios)

  print("======================================================================================")


def get_report_geral():
  
  report_geral = {
    'valido' : 0,
    'invalido': 0,
    'duvida': 0,
    'total_audios': 0,
    'report_locutor': []
  }
  
  for (dirpath, dirnames, filenames) in os.walk(ANALISE_PATH):
    
    for file in filenames:

      if 'impostores' not in file:
        report_locutor = {}
        with open(ANALISE_PATH + '/' + file, "r") as fp:
          data = json.load(fp)
          report_geral['valido'] += data['valido']
          report_geral['invalido'] += data['invalido']
          report_geral['duvida'] += data['duvida']

          report_geral['report_locutor'].append(data)

  report_geral['total_audios'] = report_geral['valido'] + report_geral['invalido'] + report_geral['duvida']
  print("Montando relatório ...\n\n")

  print("===================================== Report ========================================")
  print()
  print("Resumo Geral")
  print("Total de áudios: {}".format(report_geral['total_audios']))
  print("Áudios validados: {}".format(report_geral['valido']))
  print("Falso Negativo: {}".format(report_geral['invalido']))
  print("Limiar de dúvida: {}".format(report_geral['duvida']))
  print()

  for rp in report_geral['report_locutor']:
    printa_report_locutor(rp)

  print("======================================================================================")

if __name__ == '__main__':
  print("Vamos analisar o desempenho do classificador para os dados de teste...")
  print("O que deseja fazer?")
  print("Opção 1 - Ver report do teste")
  print("Opção 2 - Ver report usando impostores")
  print("Opção 3 - Ver report usando impostores sem listar audios")
  print("Opção 4 - Gerar métricas do teste e ver report")
  print("Opção 5 - Gerar métricas usando impostores e ver report")
  print("Opção 6 - Sair")
  opcao = input("Escolha uma opção \n")

  while(opcao != '1' and opcao != '2' and opcao != '3' and opcao != '4' and opcao != '5' and opcao != '6'):
    print("Opção inválida.")
    opcao = input("Escolha uma opção \n")

  if opcao == '1':
    get_report_geral()
  elif opcao == '2':
    get_report_impostores()
  elif opcao == '3':
    get_report_impostores(False)
  elif opcao == '4':  
    for locutor in ARRAY_LOCUTORES:
      gera_metricas_locutor(locutor)
    get_report_geral()
  elif opcao == '5':
    for locutor in ARRAY_LOCUTORES:
      gera_metricas_locutor_impostores(locutor)
    get_report_impostores()
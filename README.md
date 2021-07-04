<a href="">
<img src="https://user-images.githubusercontent.com/29777680/118411176-a28e7b00-b669-11eb-9bce-ee8abab52ec4.jpg" align="right" height="200" width="200" ></a>

# Verificador de Locutor    

Verificador de Locutor utilizando Coeficientes MFCC e Classificador K-Means    
-------------

Desenvolvido para compor Trabalho de Conclusão de Curso disponível em: [Verificador de Locutor utilizando Coeficientes MFCC e Classificador K-Means](http://dspace.sti.ufcg.edu.br:8080/jspui/bitstream/riufcg/19780/1/GABRIEL%20ALMEIDA%20AZEVEDO%20-%20%20-%20TCC%20CI%c3%8aNCIA%20DA%20COMPUTA%c3%87%c3%83O%202021.pdf)

---

## Instruções

### Rodando o Verificador
1. Clone o repositório
2. Entre na pasta
3. Rode o comando `pip3 install -r requirements.txt`
4. Fase de Treinamento: Para extrair as características dos locutores rode: `python3 extrator.py`
5. Fase de Teste: Para gerar as métricas de teste rode `python3 analisador.py` escolhendo uma das opções do MENU. 
6. O arquivo `config.py` contém as configurações de valores usados para extração dos MFCC, Cluster Centers, nomes dos locutores e limiares.

### Base de Dados
A base de dados utilizada no TCC não foi disponibilizada para preservar os locutores, entretanto adicionei meus dados como exemplo.

Para montar sua base de dados defina frases diferentes para cada um dos locutores. Idealmente usa-se [frases foneticamente balanceadas](https://jcis.sbrt.org.br/jcis/article/view/166/80).  
Note que os áudios de impostores são áudios em que outras pessoas falam a frase do locutor original.  
- Após montar sua base e realizar as etapas de pré-processamento de dados (remoção de silêncio, tratamento de ruídos, etc), organize seus áudios.   
- Dentro do verificador existe uma pasta chamada Base_de_Dados. Para cada locutor crie uma pasta com o nome dele. Ex: Gabriel.   
- Dentro dessa pasta crie mais 3 pastas (treino, teste, impostores). Separado os áudios de treino, una-os montando um único arquivo wav.   
- No arquivo `config.py`, defina: o array de locutores, os limiares de aceitação e dúvida para eles e os valores que deseja utilizar para extração dos MFCC (dependem da sua base - Sample Rate, Hop Length, FFT, etc) e para o processo de clusterização.  
- No arquivo do `validador.py`, nos métodos `get_limiar_aceitacao` e `get_limiar_duvida` adicione a lógica para os limiares dos seus locutores.
 



### Requirements
<a href="">
 <img src="https://user-images.githubusercontent.com/29777680/118411562-8c81ba00-b66b-11eb-95b3-60eb07f9824e.jpg" align="right" height="150" width="200" >
</a>

- Python3 versão 3.6.9
- scipy
- numpy
- pydub
- librosa
- python_speech_features
- scikit-learn

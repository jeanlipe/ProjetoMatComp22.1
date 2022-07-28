#Python para finanças - CAPM (Capital Asset Pricing Model)
#Importando as bibliotecas.
from linear_regression import simple_linear_regression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data
import pandas_datareader as pdr

#Buscando dados e armazenando.
acoes = ['BOVA11.SA', 'MGLU3.SA']
acoes_df = pd.DataFrame()

for acao in acoes:
  acoes_df[acao] = data.DataReader(acao, data_source='yahoo', start='2018-01-01')['Close'] 

acoes_df.to_csv('acoes.csv')
dataset = pd.read_csv('acoes.csv')

#Normalizando os dados.
def normalizando(dataset):
  dataset = dataset.copy()
  #Apagando coluna que não será usada.
  dataset.drop(labels = ['Date'], axis = 1, inplace = True)
  #Normalizando
  dataset_normalizado = dataset
  for i in dataset.columns:
    dataset_normalizado[i] = dataset[i] / dataset[i][0]
  return dataset_normalizado

#Taxa de Retorno Esperada diária e anual.
def taxa_diaria_anual(dataset):
  dataset_normalizado = normalizando(dataset)
  #Taxa de Retorno diária
  retorno_diario = (dataset_normalizado / dataset_normalizado.shift(1)) - 1
  #Preenchendo as células Na com 0.
  retorno_diario.fillna(0, inplace=True)
  #Taxa de Retorno Anual.
  retorno_anual = retorno_diario.mean() * 252
  return retorno_diario, retorno_anual

retorno_diario, retorno_anual = taxa_diaria_anual(dataset)

#Analise exploratória dos Dados - Diagrama de Dipersão
#plt.scatter(x = retorno_diario['BOVA11.SA'], y = retorno_diario[acoes[0]], color = 'red')

#Encontrando o Coeficiente Beta.
Beta, Alpha = np.polyfit(x = retorno_diario['BOVA11.SA'], y = retorno_diario[acoes[1]], deg = 1)
print('Beta:', Beta,';', 'Alpha:', Alpha)

#Visualização da Função Retorno do Ativo em relação ao Retorno da Carteira de Mercado.
plt.scatter(x = retorno_diario['BOVA11.SA'], y = retorno_diario[acoes[1]], color = 'red')
x = retorno_diario['BOVA11.SA']

y1 = Beta * retorno_diario['BOVA11.SA'] + Alpha

y2 = simple_linear_regression(retorno_diario)

plt.plot(x, y1, label = 'Reta de Regressão Linear - CAPM')
plt.title('Regressão Linear Simples - Modelo CAPM')
plt.xlabel('BOVA11.SA')
plt.ylabel(acoes[1])
plt.legend()

plt.figure()
plt.scatter(x = retorno_diario['BOVA11.SA'], y = retorno_diario[acoes[1]], color = 'blue')
plt.plot(x, y2, label = 'Reta de Regressão Linear - CAPM', color='green')
plt.title('Regressão Linear Simples - Modelo CAPM')
plt.xlabel('BOVA11.SA')
plt.ylabel(acoes[1])
plt.legend()


plt.show()

#print(Beta)
#Retorno da Carteira de Mercado
Rm = retorno_diario['BOVA11.SA'].mean() * 252
#print(Rm)

#Taxa Selic Média
Taxa_selic_historico = np.array([2.75,2.74,5.95,6.50])
Rf = Taxa_selic_historico.mean() / 100
#print(Rf)

#Modelo CAPM para MGLU
CAPM_MGLU = Rf + (Beta * (Rm - Rf))
#print(CAPM_MGLU)

print(f'Retorno diario é igual a {retorno_diario}\n\n\n\n\n\n')

print(f'Y1 é igual a {y1} \n\n\n\n\n\n\n')

print(f'Y2 é igual a {y2}\n\n\n\n\n\n\n')




from math import pow

def get_headers(dataframe):
    """
    Pega o nome dos headers do dataframe
    :param dataframe:
    :return:
    """
    return dataframe.columns.values


def cal_mean(readings):
    """
    Função que calcula o valor médio das leituras de entrada
    :param readings:
    :return:
    """
    readings_total = sum(readings)
    number_of_readings = len(readings)
    mean = readings_total / float(number_of_readings)
    return mean


def cal_variance(readings):
    """
    Calcula a variança das leituras
    :param readings:
    :return:
    """

    # Para calcular a variança é necessário o valor da média
    readings_mean = cal_mean(readings)
    mean_difference_squared_readings = [pow((reading - readings_mean), 2) for reading in readings]
    variance = sum(mean_difference_squared_readings)
    return variance / float(len(readings) - 1)


def cal_covariance(readings_1, readings_2):
    """
    Calcula a covariança entre duas listas diferentes de leituras
    :param readings_1:
    :param readings_2:
    :return:
    """
    readings_1_mean = cal_mean(readings_1)
    readings_2_mean = cal_mean(readings_2)
    readings_size = len(readings_1)
    covariance = 0.0
    for i in range(0, readings_size):
        covariance += (readings_1[i] - readings_1_mean) * (readings_2[i] - readings_2_mean)
    return covariance / float(readings_size - 1)


def simple_linear_regression(dataset):
    """
    Implementando regressão linear simples
    :param dataset:
    :return:
    """
    
    dataset_headers = get_headers(dataset)
    
    x_mean = cal_mean(dataset[dataset_headers[0]])
    y_mean = cal_mean(dataset[dataset_headers[1]])

    x_variance = cal_variance(dataset[dataset_headers[0]])
    
    # Calculando a regressão
    covariance_of_x_and_y = dataset.cov()[dataset_headers[0]][dataset_headers[1]]
    coef_a = covariance_of_x_and_y / float(x_variance)

    coef_b = y_mean - (coef_a * x_mean)

    y = coef_a * dataset[dataset_headers[0]] + coef_b
    
    return [y, coef_a, coef_b]
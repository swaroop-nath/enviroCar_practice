import math
import numpy as np
import datetime as dt

def inverse_distance(i_latlng, j_latlng):
    den = math.sqrt((j_latlng[0]-i_latlng[0])**2 + (j_latlng[1] - i_latlng[1])**2)
    return 1/den
    
def inverse_distance_squared(i_latlng, j_latlng):
    den = (j_latlng[0]-i_latlng[0])**2 + (j_latlng[1] - i_latlng[1])**2
    return 1/den

def calculate_weight_matrix(concerned_bins, method = 'inverse_distance_squared'):
    weight_matrix = np.zeros(shape = (len(concerned_bins), len(concerned_bins)))
    for row in range(0, len(concerned_bins)):
        for column in range(0, len(concerned_bins)):
            if row != column:
                if method == 'inverse_distance_squared':
                    weight_matrix[row][column] = inverse_distance_squared(concerned_bins[row].latlng, concerned_bins[column].latlng)
                elif method == 'inverse_distance':
                    weight_matrix[row][column] = inverse_distance(concerned_bins[row].latlng, concerned_bins[column].latlng)
    return weight_matrix

def calculate_general_g_statistic(concerned_bins, weight_matrix, date):
    sum_num = 0
    sum_den = 0
    for i in range(0, len(concerned_bins)):
        for j in range(0, len(concerned_bins)):
            sum_num = sum_num + weight_matrix[i][j]*concerned_bins[i].get_feature(date)*concerned_bins[j].get_feature(date)
            sum_den = sum_den + concerned_bins[i].get_feature(date)*concerned_bins[j].get_feature(date)
    general_g = sum_num/sum_den
    return general_g

def calculate_expected_g(weight_matrix):
    sum_num = 0
    den = len(weight_matrix) * (len(weight_matrix) - 1)
    for i in range(0, len(weight_matrix)):
        for j in range(0, len(weight_matrix[i])):
            sum_num = sum_num + weight_matrix[i][j]
    expected_g = sum_num/den
    return expected_g

def calculate_z_score(expected_g, expected_g_square, weight_matrix):
    W = 0
    S_1 = 0
    S_2 = 0
    for i in range(0, len(weight_matrix)):
        temp = 0
        for j in range(0, len(weight_matrix)):
            W = W + weight_matrix[i][j]
            S_1 = 0.5 * ((weight_matrix[i][j] + weight_matrix[j][i])**2)
            temp = temp + 2 * weight_matrix[i][j]
        S_2 = S_2 +(temp**2)

    D_4 = S_1 - S_2 + W**2
    D_3 = 4*(n-1)*S_1 - 2*(n+1)*S_2 + 8*(W**2)
    D_2 = - (2*n*S_1 - (n+3)*S_2 + 6*(W**2))
    D_1 = -((n**2 - n)*S_1 - 2*n*S_2 + 6*(W**2))
    D_0 = (n**2 - 3*n + 3)*S_1 - n*S_2 + 3*(W**2)

            
def find_clusters_global(date, bins):
    bins_concerned = []
    for row in range(0, len(bins)):
        for column in range(0, len(bins[row])):
            if bins[row][column].get_feature(date) != None:
                bins_concerned.append(bins[row][column])
    weight_matrix = calculate_weight_matrix(bins_concerned)
    general_g = calculate_general_g_statistic(bins_concerned, weight_matrix, date)
    expected_g = calculate_expected_g(weight_matrix)
    return [general_g, expected_g, z_score, p_value]

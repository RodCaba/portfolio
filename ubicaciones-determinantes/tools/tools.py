def sep_str(dframe, vector, str_sep, n_sep):
    """
    Function to separate an address vector from a DataFrame to Latitude and Longitude separate Vectors

    Keyword arguments:
    :param dframe: Pandas DataFrame to apply on
    :param vector: Vector as string to apply separate
    :param str_sep: string separator
    :param n_sep: number of separations (int)
    """
    temp = dframe[vector].str.split(str_sep, expand = True, n = n_sep)
    dframe['Latitud'] = temp[0]
    dframe['Longitud'] = temp[1]
    return dframe

def join_str(dframe, new_name, left_vector, right_vector):
    """
    Function to join 2 vectors of strings into a new one, separated by space

    Keyword arguments:
    :param dframe: Pandas DataFrame to apply on
    :param new_name: String value for the name of the new vector created
    :param left_vector: String value of the vector on the left
    :param right_vector: String value of the vector on the right
    """
    dframe[new_name] = dframe[left_vector] + ' ' + dframe[right_vector]
    return dframe
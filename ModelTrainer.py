import pandas as pd
import numpy as np
#from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor

def trainStart(data, target, cols, modelLoading, haveModel, models):

    #cols should be a list of columns
    #target should be a String

    modelLoading[0] = True
    data = pd.read_csv(data, sep="|")

    # Create dummies for all columns of type 'object'
    g = data.columns.to_series().groupby(data.dtypes).groups
    datatypes = {k.name: v for k, v in g.items()}
    objecttypes = list(datatypes['object'])

    for item in objecttypes:
        if item in cols:
            for elem in data[item].unique():
                data[str(elem)] = data[item] == elem
                #locations.append(str(elem))
            data = data.drop([item], axis=1)

    # Good to go!
    data_X = data.drop([target], axis=1)[cols]
    data_y = np.array(data[target])

    # TODO Should make it possible to select a model type #
    mod = MLPRegressor(hidden_layer_sizes=(100, 100), max_iter=1000000)
    mod.fit(data_X, data_y)

    models[0] == mod
    haveModel[0] = True

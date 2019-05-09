import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

dict = {
    "login": ['1', '2', '3', '4', '5'],
    "first_genre": [2,3,4,5,6],
    "second_genre": [6,5,4,3,2],
    "third_genre": [4,4,7,4,1],
    "age": [20,47,12,66,40],
    "sex": ['male', 'female', 'female', 'male', 'male'],
    "language": ['EN','RU','UKR','RU','EN'],
    "religion":['2','1','1','2','6']
}

logs = [{'UserID': '1234567890', 'DataLogs': {'0': 1, '1': 3, '2': 1}, 'Sex': 'male', 'Age': 1},
{'UserID': '123456', 'DataLogs': {'3': 1}, 'Sex': 'male', 'Age': 12},
{'UserID': '123', 'DataLogs': {'2': 1, '3': 1}, 'Sex': 'female', 'Age': 23}]

def convert_data(logs):
    genres = []
    for user in logs:
        for genre in user["DataLogs"].keys():
            if genre not in genres:
                genres.append(genre)
    print(genres)
    dict = {}
    for user in logs:
        for key in user.keys():
            if key != "DataLogs":
                if key not in dict:
                    dict[key] = []
                dict[key].append(user[key])
                continue
            for genre in genres:
                if genre not in dict:
                    dict[genre] = []
                dict[genre].append(user[key].get(genre, 0))

    return dict


def get_clusters(logs):
    data = convert_data(logs)
    dataframe = pd.DataFrame(data)
    print(dataframe)
    labelEncoder = LabelEncoder()
    dataframe["Sex"] = labelEncoder.fit_transform(dataframe["Sex"])
    print(dataframe)
    x = np.array(dataframe.drop(['UserID'], 1).astype(float))
    print(x)
    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)
    print(x)
    kmeans = KMeans(n_clusters = 2)
    kmeans.fit(x)
    clusters = {}
    for i in range(len(x)):
        pred = np.array(x[i].astype(float))
        pred = pred.reshape(-1, len(pred))
        cluster_id = str(kmeans.predict(pred))
        print(cluster_id)
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(dataframe["UserID"][i])
    return(clusters)


def main():
    '''dataframe = pd.DataFrame(dict)
    print(dataframe)

    labelEncoder = LabelEncoder()
    dataframe["sex"] = labelEncoder.fit_transform(dataframe["sex"])
    dataframe["language"] = labelEncoder.fit_transform(dataframe["language"])
    dataframe["religion"] = labelEncoder.fit_transform(dataframe["religion"])
    print(dataframe)

    x = np.array(dataframe.drop(['login'], 1).astype(float))

    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)

    kmeans = KMeans(n_clusters = 3)
    kmeans.fit(x)
    for i in range(len(x)):
        pred = np.array(x[i].astype(float))
        pred = pred.reshape(-1, len(pred))
        print(kmeans.predict(pred))'''

    get_clusters(logs)


if __name__ == "__main__":
    main()

import math
import pandas
import sys
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

"""
Class to generate the cluster prototype. cluster_points saves the indices of the points.
"""


class Cluster:
    def __init__(self):
        self.center = None
        self.cluster_points = []


"""
Class Kmeans to cluster apply the algorithm
"""


class KMeans:
    def __init__(self, points_data):
        """
        Initialize the class with data frame read from csv file
        """
        self.points_data = points_data

    def calculate_new_center(self, data, indices_of_points):
        """
        :param data: get the data points
        :param indices_of_points are indices in the cluster prototype
        :return: the mediod point.
        """
        sum_all = []
        dimensions = len(data[0])
        for i in range(dimensions):
            sum_all.append(0)

        for index in indices_of_points:
            for i in range(dimensions):
                sum_all[i] += data[index][i]
        """
        get the point which has the minimum distance from the centroid.
        """
        centroid = [g / len(data) for g in sum_all]
        mediod = []
        min_d = sys.maxsize
        for point in data:
            d = math.sqrt(sum([(x1 - x2) * (x1 - x2) for x1, x2 in zip(point, centroid)]))
            if d < min_d:
                mediod = point
                min_d = d
        return mediod

    def cluster(self, k):
        """
        :param k: number of clusters to prototype
        :return: the clusters dictionary containing the cluster number as key and Cluster prototype in form of
        dictionary
        Initialize the random clusters. then repeatedly Update the centers and assign points to the closest prototype.
        """
        clusters = {}
        random_k_centroids = random.sample(range(0, len(self.points_data.index)), k)
        data_points = self.points_data.values.tolist()

        for i in range(k):
            clusters[i] = Cluster()
            clusters[i].center = data_points[random_k_centroids[i]]

        current_iteration = 0
        done = False

        while (not done) & (current_iteration < 20):

            for key in clusters.keys():
                clusters[key].cluster_points = []
            """
            assign the points to nearest prorotype.
            """
            for i in range(len(self.points_data.index.tolist())):
                current_point = data_points[i]
                min_distance = sys.maxsize
                min_cluster = None
                for cluster_number, cluster in clusters.items():
                    distance = math.sqrt(sum([(x1 - x2) * (x1 - x2) for x1, x2 in zip(current_point, cluster.center)]))
                    if distance < min_distance:
                        min_cluster = cluster_number
                        min_distance = distance
                clusters[min_cluster].cluster_points.append(i)

            """
            update the prototype center with mediod.
            """
            for cluster_number, cluster in clusters.items():
                if cluster.cluster_points:
                    new_center = self.calculate_new_center(data_points, cluster.cluster_points)
                    change_distance = math.sqrt(
                        sum([(x1 - x2) * (x1 - x2) for x1, x2 in zip(new_center, cluster.center)]))
                    if change_distance < 0.1:
                        done = True
            current_iteration += 1
        return clusters

    def find_sse(self, prototype):
        """
        :param prototype: This is a dictionary with cluster number and Cluster class with center and cluster_points
        :return: float value of sum of squared distances.
        """
        sum_of_squared_errors = 0
        data_points = self.points_data.values.tolist()
        for cluster_number, cluster in prototype.items():
            for point_index in cluster.cluster_points:
                squared_distance = sum([(x1 - x2) ** 2 for x1, x2 in zip(data_points[point_index], cluster.center)])
                sum_of_squared_errors += squared_distance

        return sum_of_squared_errors


def main():
    """
    Read the data into df, calculate sse for 12 iterations for given K and append it to 'min_sses' list
    and list of 'cluster_prototypes'
    """
    df = pandas.read_csv("HW08_KMEANS_DATA_v300.csv", header=0)
    clustering = KMeans(df)
    cluster_prototype = []
    min_sses = []
    z = 0
    while z < 12:
        e = []
        s = []
        q = -1
        min_sse = sys.maxsize
        for i in range(10):
            c = clustering.cluster(z + 1)
            e.append(c)
            sse = clustering.find_sse(c)
            s.append(sse)
            if sse < min_sse:
                min_sse = sse
                q = i
        cluster_prototype.append(e[q])
        min_sses.append(s[q])
        z += 1

    plt.scatter( [ i+1 for i in range(len(min_sses))], min_sses)
    plt.plot( [ i+1 for i in range(len(min_sses))], min_sses)
    plt.ylabel("Min SSE in "+str(z)+" iterations")

    plt.xlabel("Value of K")
    plt.show()

    for i, c in enumerate(cluster_prototype):
        print("K = ", i + 1, "SSE = ", min_sses[i])
        for k, v in c.items():
            print(k, " : ", "len: ", len(v.cluster_points), "\n")

    # since we selected K = 5
    """
    Get all the points and assign the color based on K
    """
    K = 5
    x = []
    y = []
    z = []
    clr = ['red', 'yellow', 'magenta', 'green','black', 'orange', 'cyan', 'gray', 'pink', 'brown']
    fig = plt.figure(2)
    ax = fig.add_subplot(111, projection='3d')
    cm = plt.get_cmap("RdYlGn")

    points_data = df.values.tolist()
    for k, v in cluster_prototype[K - 1].items():
        for p in v.cluster_points:
            x.append((points_data[p])[0])
            y.append((points_data[p])[1])
            z.append((points_data[p])[2])
            clr.append(k)
            color = k
            if k >len(clr):
                color = k%len(clr)

            ax.scatter((points_data[p])[0], (points_data[p])[1], (points_data[p])[2], c=clr[color], zdir='z',
                       depthshade=True)

    # print(x, "\n", "\n", y, "\n", z)
    ax.set_xlabel('Attr1')
    ax.set_ylabel('Attr2')
    ax.set_zlabel('Attr3')

    plt.show()


if __name__ == '__main__':
    main()

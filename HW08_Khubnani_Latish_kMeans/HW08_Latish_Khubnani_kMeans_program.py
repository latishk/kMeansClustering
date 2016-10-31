import math
import pandas as pd
import sys
import random
import matplotlib.pyplot as plt


class Cluster:
    def __init__(self):
        self.center = None
        self.c_points = []


def find_new_center(indices_of_points, points):
    sum_distance = []
    dimensions = len(points[0])
    # print("dimensions",dimensions)
    for i in range(dimensions):
        sum_distance.append(0)

    for index in indices_of_points:
        for i in range(dimensions):
            sum_distance[i] += points[index][i]

    center = [g / len(points) for g in sum_distance]

    md = sys.maxsize
    mediod = []
    for e, point in enumerate(points):
        d = sum([math.pow((x - y), 2) for x, y in zip(point, center)])
        if d < md:
            md = d
            mediod = point
            # print(e)
    return mediod


def sse(clstrs, points):
    s_sse = 0
    for cl_n, clstr in clstrs.items():
        for p in clstr.c_points:
            s_sse += sum([(x1 - x2) ** 2 for x1, x2 in zip(points[p], clstr.center)])

    return s_sse


def cluster(points, k):
    clusters = {}
    random_k_centroids = random.sample(range(0, len(points)), k)
    for i in range(k):
        clusters[i + 1] = Cluster()
        clusters[i + 1].center = points[random_k_centroids[i]]

    for i, p in enumerate(points):
        md = sys.maxsize
        cls_n = None
        for k_n, cls in clusters.items():
            d = math.sqrt(sum([(x1-x2)**2 for x1,x2 in zip(cls.center, p)]))
            if d < md:
                md = d
                cls_n = k_n

        clusters[cls_n].c_points.append(i)


    changed = True
    iter = 0

    while changed and iter < 20:

        for cluster_number, clstr in clusters.items():
            new_center = find_new_center(clstr.c_points, points)
            if new_center is not clstr.center:
                clstr.center = new_center
            else:
                changed = False

        for key, value in clusters.items():
            value.c_points = []

        for idx, pnt in enumerate(points):

            dis = sys.maxsize
            cls_n = None

            for k_n, clstr in clusters.items():
                d = math.sqrt(sum([(x2-x1)**2 for x1, x2 in zip(pnt, clstr.center)]))
                if d < dis:
                    dis = d
                    cls_n = k_n

            clusters[cls_n].c_points.append(idx)


        iter += 1
    return clusters




    #     center_moving = True
    #     # while(delta_cahnge > 0.05):
    #     current_iteration = 0
    #     terminate = "No"
    #     while center_moving:
    #         for key, value in clusters.items():
    #             value.c_points = []
    #
    #         for index, point in enumerate(points):
    #             min_distance = sys.maxsize
    #             cluster_number = None
    #             for k_value, c_point in clusters.items():
    #                 distance_from_center = sum([(x1 - x2) ** 2 for x1, x2 in zip(c_point.center, point)])
    #                 if min_distance >= distance_from_center:
    #                     min_distance = distance_from_center
    #                     cluster_number = k_value
    #             clusters[cluster_number].c_points.append(index)
    #
    #         for cluster_number, clstr in clusters.items():
    #             new_center = find_new_center(clstr.c_points, points)
    #             # delta = math.sqrt(sum([(x1 - x2) ** 2 for x1, x2 in zip(new_center, clstr.center)]))
    #             # if delta > 0.05:
    #             if new_center == clstr.center:
    #                 center_moving = False
    #                 terminate = "Yes"
    #             else:
    #                 clstr.center = new_center
    #
    #         current_iteration = current_iteration + 1
    # return clusters


def main():
    df = pd.read_csv("HW08_KMEANS_DATA_v300.csv", header=0)
    points_data = df.values.tolist()
    c = cluster(points_data, 5)
    # #
    for key, value in c.items():
        print(key, ": ",value.center,"\n", value.c_points)
    # # print(sse(c, points_data))


    # all_clusters = []
    # sses = []
    # for i in range(1, 13):
    #     all_clusters.append(cluster(points_data, i))
    #     sses.append(sse(all_clusters[i - 1], points_data))
    #
    # m = sses[0]
    # k = -1
    # for i, minsse in enumerate(sses):
    #     if minsse < m:
    #         m = minsse
    #         k = i + 1
    # print(k)
    # for key, value in all_clusters[k - 1].items():
    #     print(key, ": ", value.center, "\n", value.c_points)
    #
    # plt.plot([x + 1 for x in range(len(sses))], sses)
    # plt.show()


if __name__ == '__main__':
    main()





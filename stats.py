import collections
from scipy.spatial import distance
from operator import add

#Function to calculate the individual within-cluster scatter.
def calc_ind_within_cluster_scatter(data, centers, count, k):
    data_length = len(data)
    within_cluster_scatter = []
    total = 0
    for i in xrange(0, k):
        for j in xrange(0, data_length):
            if(data[j][5] == i):
                total += distance.euclidean(data[j][0:4:1], centers[i])
        within_cluster_scatter.append((float(1) / count[i]) * total)
    return within_cluster_scatter

#Function to calculate the overall within-cluster scatter.
def calc_ov_within_cluster_scatter(data, centers, k):
    data_length = len(data)
    wcs = 0
    for i in xrange(0, k):
        temp_tot = 0
        for j in xrange(0, data_length):
            if(data[j][5] == i):
                temp_tot += ((distance.euclidean(data[j][0:4:1], centers[i])) ** float(2))
    wcs += temp_tot
    return wcs

#Function to calculate the overall between-cluster variance
def calc_between_cluster_variance(data, centers, count, k):    
    data_length = len(data)
    bcv = 0
    mean = [0.0, 0.0, 0.0, 0.0]
    for i in xrange(0, data_length):
        mean = map(add, data[i][0:4:1], mean)
    for i in xrange(0, 4):
        mean[i] /= data_length
    for i in xrange(0, k):
        bcv += (count[i] * ((distance.euclidean(centers[i], mean)) ** float(2)))
    return bcv

#Function to calculate the between-cluster spread.
def calc_between_cluster_spread(center1, center2):
    return distance.euclidean(center1, center2)
    
#Function to calculate the measure of cluster 'goodness'
def calc_cluster_measure(scatter1, scatter2, spread):
    return ((scatter1 + scatter2) / spread)

#Function to caclulate the Davies-Bouldin Index.
def calc_dbi(k, d):
    return (float(1) / float(k)) * (float(3) * float(d))

#Function to calculate the Calinski-Harabasz Index.
def calc_chi(N, k, ssb, ssw):
    return ((ssb / ssw) * ((N - k) / (k - 1)))

#Function to evaluate the clusters using simple metrics.
def evaluate_clusters_simple(data, count, k):
    data_length = len(data)
    evaluation = []
    for i in xrange(0, k):
        counter = collections.Counter()
        for j in xrange(0, data_length):
            if(data[j][5] == i):
                counter[data[j][4]] += 1
        evaluation.append(counter)
    print "\nCluster 1: ", dict(evaluation[0])
    print "Cluster 2: ", dict(evaluation[1])
    print "Cluster 3: ", dict(evaluation[2]), "\n"
    for i in xrange(0, k):
        dominant_label = max(evaluation[i], key=evaluation[i].get)
        print "Dominant label for cluster", i + 1, "is '", dominant_label, "' with", evaluation[i][dominant_label], "out of", int(count[i]), "data points. (", round(float((float(evaluation[i][dominant_label]) / count[i]) * float(100))), "% )"


#Function to perform DBI evaluation on a set of clusters.
def evaluate_clusters_complex(data, centers, count, k):
    within_cluster_scatter = calc_ind_within_cluster_scatter(data, centers, count, k)
    sep1_2 = calc_between_cluster_spread(centers[0], centers[1])
    sep1_3 = calc_between_cluster_spread(centers[0], centers[2])
    sep2_3 = calc_between_cluster_spread(centers[1], centers[2])
    cm1_2 = calc_cluster_measure(within_cluster_scatter[0], within_cluster_scatter[1], sep1_2)
    cm1_3 = calc_cluster_measure(within_cluster_scatter[0], within_cluster_scatter[2], sep1_3)
    cm2_3 = calc_cluster_measure(within_cluster_scatter[1], within_cluster_scatter[2], sep2_3)
    dbi = calc_dbi(k, max(cm1_2, cm1_3, cm2_3))
    print "Davies-Bouldin Index for cluster set (lower is better):", round(dbi, 4)
    ssw = calc_ov_within_cluster_scatter(data, centers, k)
    ssb = calc_between_cluster_variance(data, centers, count, k)
    chi = calc_chi(len(data), k, ssb, ssw)
    print "Calinski-Harabasz Index for cluster set (higher is better):", round(chi, 4)
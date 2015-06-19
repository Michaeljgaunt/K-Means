import random
import numpy
import collections
from scipy.spatial import distance
from operator import add

#Function to generate vectors from the data.
def get_feat_vects(fname, D):
    feat_vects = []
    #Opening the training data file
    with open(fname) as feat_file:
        for line in feat_file:
            x = []
            count = 1
            #Splitting feature by comma and line.
            for w in line.strip().split(','):
                if(count < 5):
                    #Converting string representations into floats
                    x.append(float(w))
                else:
                    #Appending the string label.
                    x.append(w)
                count += 1
            feat_vects.append(x)
    return feat_vects

#Function to cluster the data using Euclidean distance from the cluster centers.
def cluster_data(centers, data, c):
    data_length = len(data)
    centers_length = len(centers)
    #Iterating over each feature vector
    for i in xrange(0, data_length):
        #Iterating over each cluster center
        for j in xrange(0, centers_length):
            #Calculating euclidean distance of the vector from the cluster center.
            if(centers_length == 5):
                curr_dist = distance.euclidean(data[i][0:4:1], centers[j][0:4:1])
            else:
                curr_dist = distance.euclidean(data[i][0:4:1], centers[j][0:4:1])
            if(j == 0):
                dist = curr_dist
                cluster = 0
            if(curr_dist < dist):
                dist = curr_dist
                cluster = j
        #Appending the cluster index to the feature vector if its the first occurence of this method call.
        if(c):
            data[i].append(cluster)
        #Replacing the old cluster index with the new one if it is not the first occurence of this method call.
        else:
            data[i][-1] = cluster
    return data

#Function to caluclate the centers of the clusters.
def calculate_centers(data, k):
    data_length = len(data)
    new_centers = []
    #Iterating over the clusters.
    for i in xrange(0, k):
        count = 0
        total = [0.0, 0.0, 0.0, 0.0]
        for j in xrange(0, data_length):
            #If the data point has the same cluster number as the currently iterating one, add it to the total.
            if(data[j][5] == i):
                count += 1
                total = map(add, data[j][0:4:1], total)
        #Calculating the mean center.
        for l in xrange(0, 4):
            total[l] /= count   
        new_centers.append(total)
    return new_centers

#Function to count the number of items in a cluster.
def count_cluster_items(data, k):
    count = numpy.zeros(k)
    data_length = len(data)
    for i in xrange(0, k):
        for j in xrange(0, data_length):
            if(data[j][5] == i):
                count[i] += 1
    return count

#Function to compare two lists.
def compare_counts(old_count, new_count, k):
    for i in xrange(0, k):
        if(old_count[i] != new_count[i]):
            return False
        else:
            continue
    return True

#Function to evaluate the clusters using simple methods.
def simple_evaluate_clusters(data, count, k):
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

#Function to evaluate clusters using the more complex Davies-Bouldin index.
def DBI_evaluate_clusters(data, centers, count, k):
    data_length = len(data)
    within_cluster_scatter = []
    total = 0
    for i in xrange(0, k):
        for j in xrange(0, data_length):
            if(data[j][5] == i):
                total += distance.euclidean(data[j][0:4:1], centers[i][0:4:1])
        within_cluster_scatter.append((float(1) / count[i]) * total)
    print within_cluster_scatter
if __name__ == "__main__":
    #Setting K value.
    k = 3
    #Generating vectors from the data file.
    feat_vects = get_feat_vects("iris.data.txt", 5)
    #Picking K random vectors to serve as initial cluster centres.
    print "\nInitialising cluster centers..."
    centers = random.sample(feat_vects, k)
    #Performing initial clustering.
    print "Clustering data..."
    clustered_data = cluster_data(centers, feat_vects, True)
    #Counting members in each cluster.
    print "Counting cluster members..."
    new_count = count_cluster_items(clustered_data, k)
    print new_count
    #Setting the flag and counter for the while loop.
    converge_flag = False
    counter = 1


    #This block executes while the clusters have not converged
    while not bool(converge_flag):
        print "\nIteration ", counter
        old_count = new_count
        print "Calculating new cluster centers..."
        centers = calculate_centers(clustered_data, k)
        print "Clustering data..."
        clustered_data = cluster_data(centers, feat_vects, False)
        print "Counting cluster members..."
        new_count = count_cluster_items(clustered_data, k)
        print new_count
        #Comparing the counts to check for convergence.
        converge_flag = compare_counts(old_count, new_count, k)
        counter += 1

    print "\nCount has remained unchanged, clusters have converged to an optima."
    print  "Evaluating clusters..."
    #Evaluating clusters
    evaluation = simple_evaluate_clusters(clustered_data, new_count, k)
    DBI_evaluate_clusters(clustered_data, centers, new_count, k)















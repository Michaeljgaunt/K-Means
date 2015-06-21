import numpy
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

#Function to caluclate the mean centers of the clusters.
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

#Function to calculate the nearest data point to the mean cluster center (medoid)
def calculate_medoids(data, centers, k):
    medoids = []
    data_length = len(data)
    for i in xrange(0, k):
        closest = 0
        firstFlag = True
        for j in xrange(0, data_length):
            if(firstFlag):
                closest = j
                curr_dist = distance.euclidean(data[j][0:4:1], centers[i][0:4:1])
                firstFlag = False
            else:
                if(distance.euclidean(data[j][0:4:1], centers[i][0:4:1]) < curr_dist):
                    closest = j
                    curr_dist = distance.euclidean(data[j][0:4:1], centers[i][0:4:1])
        medoids.append(data[closest][0:4:1])
    return medoids                    

#Function to count the number of items in a cluster.
def count_cluster_items(data, k):
    count = numpy.zeros(k)
    data_length = len(data)
    for i in xrange(0, k):
        for j in xrange(0, data_length):
            if(data[j][5] == i):
                count[i] += 1
    return count

#Function to check if the clusters are all non-zero.
def check_count(count, k):
    for i in xrange(0, k):
        if (count[i] == 0):
            return False
    return True
    
#Function to compare two lists.
def compare_counts(old_count, new_count, k):
    for i in xrange(0, k):
        if(old_count[i] != new_count[i]):
            return False
        else:
            continue
    return True
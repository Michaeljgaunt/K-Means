import k_means
import random
import argparse

if __name__ == "__main__":
    
    #Adding an argparse to parse command line commands.
    parser = argparse.ArgumentParser(description="K-Means clustering algorithm for Fisher's Iris Dataset.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #Adding commands.
    centmod = parser.add_mutually_exclusive_group(required=True)
    centmod.add_argument("-c", "--centroids", help="Use Mean centroids as cluster centers", action='store_true')
    centmod.add_argument("-m", "--medoids",help="Use Mean medoids as cluster centers", action='store_true')
    
    #Parsing the command line arguments.
    args = parser.parse_args()

    #Setting K value.
    k = 3
    #Setting acceptable initialisation flag.
    init_flag = False
    while not (init_flag):
        #Generating vectors from the data file.
        print "\nLoading dataset..."
        feat_vects = k_means.get_feat_vects("iris.data.txt", 5)
        print "Initialising cluster centers..."
        if(args.centroids):
            #Picking K random vectors to serve as initial cluster centres.
            centers = random.sample(feat_vects, k)
        if(args.medoids):
            centers = random.sample(feat_vects, k)
            #Assigning datapoints nearest to randomly generated points as the centers.
            centers = k_means.calculate_medoids(feat_vects, centers, k) 
        #Performing initial clustering.
        print "Clustering data..."
        clustered_data = k_means.cluster_data(centers, feat_vects, True)
        #Counting members in each cluster.
        print "Counting cluster members..."
        new_count = k_means.count_cluster_items(clustered_data, k)
        print new_count
        print "Checking clusters are acceptable..."
        init_flag = k_means.check_count(new_count, k)
        if not (init_flag):
            print "Non-zero cluster detected, re-initialising algorithm."
        else: 
            print "Clusters are acceptable, proceeding with iterations."
        #Setting the flag and counter for the while loop.
        converge_flag = False
        counter = 1


    #This block executes while the clusters have not converged
    while not bool(converge_flag):
        print "\nIteration", counter
        old_count = new_count
        if(args.centroids):
            print "Calculating new cluster centers (mean centroids)..."
            centers = k_means.calculate_centers(clustered_data, k)
        elif(args.medoids):
            print "Calculating new cluster centers (medoids)..."
            centers = k_means.calculate_centers(clustered_data, k)
            centers = k_means.calculate_medoids(clustered_data, centers, k)
        print "Clustering data..."
        clustered_data = k_means.cluster_data(centers, feat_vects, False)
        print "Counting cluster members..."
        new_count = k_means.count_cluster_items(clustered_data, k)
        print new_count
        #Comparing the counts to check for convergence.
        converge_flag = k_means.compare_counts(old_count, new_count, k)
        counter += 1

    print "\nCount has remained unchanged, clusters have converged to an optima."
    print  "Evaluating clusters..."
    #Evaluate clusters using simple metrics and also DBI.
    k_means.evaluate_clusters_simple(clustered_data, new_count, k)
    k_means.evaluate_clusters_complex(clustered_data, centers, new_count, k)

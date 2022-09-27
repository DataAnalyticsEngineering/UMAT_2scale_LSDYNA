#%%
db = DBSCAN(eps=1.3, min_samples=50).fit(X) #metric='correlation'
labels = db.labels_
l, count = np.unique(labels,return_counts=True)
count[l==-1] = 0
nnz = np.nonzero(count / count.max() > 0.8)[0]
n_clusters = l[nnz].size
centers_mean=np.empty((n_clusters,3))
centers_median=np.empty((n_clusters,3))
for i in range(n_clusters):
    centers_mean[i] = np.mean(X[labels==i],axis=0)
    centers_median[i] = np.median(X[labels==i],axis=0)
plt.subplot(1, 3, 2)
plt.imshow(centers_mean.reshape(-1,1,3).astype(np.int))
plt.title('DBSCAN')
plt.subplot(1, 3, 3)
plt.imshow(centers_median.reshape(-1,1,3).astype(np.int))
plt.title('DBSCAN')
plt.show()

#%%
clust = OPTICS(min_samples=50)
clust.fit(X)
# xi = .05, min_cluster_size = .05
labels = cluster_optics_dbscan(reachability=clust.reachability_,
                                   core_distances=clust.core_distances_,
                                   ordering=clust.ordering_, eps=0.5)
l, count = np.unique(labels,return_counts=True)
count[l==-1] = 0
nnz = np.nonzero(count / count.max() > 0.8)[0]
n_clusters = l[nnz].size
centers_mean=np.empty((n_clusters,3))
centers_median=np.empty((n_clusters,3))
for i in range(n_clusters):
    centers_mean[i] = np.mean(X[labels==i],axis=0)
    centers_median[i] = np.median(X[labels==i],axis=0)
plt.subplot(1, 3, 2)
plt.imshow(centers_mean.reshape(-1,1,3).astype(np.int))
plt.title('OPTICS')
plt.subplot(1, 3, 3)
plt.imshow(centers_median.reshape(-1,1,3).astype(np.int))
plt.title('OPTICS')
plt.show()

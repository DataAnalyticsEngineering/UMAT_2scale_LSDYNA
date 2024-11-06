# TODO: look at cv.THRESH_BINARY

image_eroded = cv.morphologyEx(binary_image, cv.MORPH_GRADIENT, kernel, iterations=itr)


#%% can we extract/isolate the cracks?

plt.figure(figsize=[16,8])
image_cracks = np.asarray(grayscale_sample_image * digital_image)

rng = image_cracks<=0.71
image_cracks[rng]=0
image_cracks[~rng]=1
# image_cracks[image_cracks>=0.78]=0

# image_cracks = cv.morphologyEx(image_cracks, cv.MORPH_OPEN, kernel, iterations=3)
# image_cracks = cv.morphologyEx(image_cracks, cv.MORPH_ERODE, kernel, iterations=2)


thresh = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,3,3)
# ret2,thresh = cv.threshold(gray,0,255,cv.THRESH_OTSU)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    area = cv.contourArea(cnt)
    hull = cv.convexHull(cnt)
    # if 5 < area < 100:
    cv.drawContours(image_cracks, [hull], -1, (255, 255, 255), 2)

plt.imshow(image_cracks)

#%%
# draw circle around points of the contour
# if you intersect with any black lines then ignore the contour (we're on the edge & not inside the partickle)
rr, cc = circle(np.squeeze(cnt[i])[1],np.squeeze(cnt[i])[0],3)
if np.any(digital_image[rr,cc]) == 0:




laplacian = cv.Laplacian(image_cracks, cv.CV_64F)
sobelx = cv.Sobel(image_cracks, cv.CV_64F, 1, 0, ksize=5)
sobely = cv.Sobel(image_cracks, cv.CV_64F, 0, 1, ksize=5)
plt.imshow(sobely, cmap='gray')


shrink circles a bit to find cracks inside the particles and not on the boundary


#%% density & ...

fig = plt.figure(figsize=[16,4])
xr = X[idx==0]
xg = X[idx==1]
xb = X[idx==2]

fig.add_subplot(1,3,1)
plt.scatter(xr[:,0], xr[:,1],color='red')
plt.scatter(xg[:,0], xg[:,1],color='green')

fig.add_subplot(1,3,2)
plt.scatter(xr[:,0], xr[:,2],color='red')
plt.scatter(xb[:,0], xb[:,2],color='blue')

fig.add_subplot(1,3,3)
plt.scatter(xg[:,1], xg[:,2],color='green')
plt.scatter(xb[:,1], xb[:,2],color='blue')




# fig = plt.figure(figsize=[16,4])
#
# # Z = np.exp(1/((xr[:,0])+xr[:,2]))
#
# # Plot the density map using nearest-neighbor interpolation
# # plt.hist2d(xr[:,0],xr[:,1])
#
# x = X[:,0]
# y = X[:,1]
#
# rng = x>200
# x=x[rng]
# y=y[rng]
# # plt.hist2d(,xg[:,1])
# # plt.show()
#
# from scipy.stats import gaussian_kde
#
# # Calculate the point density
# xy = np.vstack([x,y])
# z = gaussian_kde(xy)(xy)
#
# idx = z.argsort()
# x, y, z = x[idx], y[idx], z[idx]
#
# plt.scatter(x, y,c=z,s=30)


#% detect circles
#% equivalent artificial structure/image

# np.save("digital_image",digital_image)
# np.save("particles",np.array(particles))

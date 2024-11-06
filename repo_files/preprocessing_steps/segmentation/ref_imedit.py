import numpy as np
import cv2

if __name__ == '__main__':

    image = cv2.imread('image.png',cv2.IMREAD_UNCHANGED)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret,binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)

    binary = cv2.bitwise_not(binary)

    H = cv2.Sobel(binary, cv2.CV_8U, 0, 2)
    V = cv2.Sobel(binary, cv2.CV_8U, 2, 0)

    rows,cols = image.shape[:2]

    contours, hierarchy = cv2.findContours(V, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt)
        # rows/3 is the threshold for length of line
        if h > rows/3:
            cv2.drawContours(V, [cnt], -1, 255, -1)
            cv2.drawContours(binary, [cnt], -1, 255, -1)
        else:
            cv2.drawContours(V, [cnt], -1, 0, -1)

    contours, hierarchy = cv2.findContours(H, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt)
        # cols/3 is the threshold for length of line
        if w > cols/3:
            cv2.drawContours(H, [cnt], -1, 255, -1)
            cv2.drawContours(binary, [cnt], -1, 255, -1)
        else:
            cv2.drawContours(H, [cnt], -1, 0, -1)

    kernel = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(3,3))
    H = cv2.morphologyEx(H, cv2.MORPH_DILATE, kernel,iterations = 3)
    V = cv2.morphologyEx(V, cv2.MORPH_DILATE, kernel, iterations = 3)

    cross = cv2.bitwise_and(H, V)

    contours, hierarchy = cv2.findContours(cross,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    centroids = []
    for cnt in contours:
        mom = cv2.moments(cnt)
        (x,y) = mom['m10']/mom['m00'], mom['m01']/mom['m00']
        cv2.circle(image,(int(x),int(y)),4,(0,255,0),-1)
        centroids.append((x,y))

    centroids.sort(key = lambda x: x[0], reverse = False)
    centroids.sort(key = lambda x: x[1], reverse = False)

    dx = int(centroids[1][0] - centroids[0][0])
    centroids = np.array(centroids, dtype = np.float32)
    (x,y,w,h) = cv2.boundingRect(centroids)

    if x-dx > -5: x = max(x-dx,0)
    if h+dx <= rows+5: h = min(h+dx,rows)
    if w+dx <= cols+5: w = min(w+dx,cols)
    cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0))

    roi = binary[y:y+h,x:x+w]

    roi = cv2.morphologyEx(roi, cv2.MORPH_OPEN, kernel,iterations = 1)

    cv2.imshow('image', image)
    cv2.imshow('roi', roi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

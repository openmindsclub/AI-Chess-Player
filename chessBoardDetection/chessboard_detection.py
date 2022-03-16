import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.cluster import AgglomerativeClustering

def image_preprocessing(image):
    #Gaussian Blur parameters
    ksize = (5,5)

    #Adaptative Threshold parameters
    blocksize = 29  
    C = 20 

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image,ksize,cv2.BORDER_DEFAULT)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, blocksize, C)
    return image


def hough_transform(image):
    '''
    Detect lines in an image
    returns an array of (rho, theta) values.
    '''
    return cv2.HoughLines(image,1,np.pi/180,200)


def segment_by_angle(lines, k=2, **kwargs):
    #Groups lines based on angle using k-means.

    # Define criteria = (type, max_iter, epsilon)
    stop_criteria = cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER
    criteria = kwargs.get('criteria', (stop_criteria, 10, 1.0))
    flags = kwargs.get('flags', cv2.KMEANS_RANDOM_CENTERS)
    attempts = kwargs.get('attempts', 10)

    # returns angles in [0, pi] in radians then multiply the angles by two and find coordinates of that angle
    angles = np.array([line[0][1] for line in lines])
    pts = np.array([[np.cos(2*angle), np.sin(2*angle)] for angle in angles], dtype=np.float32)

    #use kmeans on the coordinates to cluster the lines
    labels, centers = cv2.kmeans(pts, k, None, criteria, attempts, flags)[1:]
    labels = labels.reshape(-1)

    # segment lines based on their kmeans label
    segmented = defaultdict(list)
    for i, line in enumerate(lines):
        segmented[labels[i]].append(line)
    segmented = list(segmented.values())
    return segmented


def intersection(line1, line2):
    #Finds the intersection of two lines.

    rho1, theta1 = line1[0]
    rho2, theta2 = line2[0]
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    b = np.array([[rho1], [rho2]])
    x0, y0 = np.linalg.solve(A, b)
    x0, y0 = int(np.round(x0)), int(np.round(y0))
    return [[x0, y0]]


def segmented_intersections(lines):
    #Finds the intersections between each vertical line with each horizontal line.

    intersections = []
    for i, group in enumerate(lines[:-1]):
        for next_group in lines[i+1:]:
            for line1 in group:
                for line2 in next_group:
                    intersections.append(intersection(line1, line2)) 

    return intersections

def final_coordinates(intersections):
    final_coordinates = []
    n_clusters = 112

    points = np.array(intersections)
    points = points.reshape(points.shape[0], 2)
    
    #Agglomerative hierarchical to cluster intersection points
    n_clusters = 112
    clustering = AgglomerativeClustering(n_clusters = n_clusters, affinity='euclidean', linkage='ward')
    clustering.fit_predict(points)

    clusters = {}
    for i in range (n_clusters):
        clusters[i] = []
    labels = list(clustering.labels_)
    for i in range(clustering.labels_.shape[0]):
        clusters[int(labels[i])].append(intersections[i])

    for i in clusters:
        cluster = np.array(clusters[i])
        cluster = cluster.reshape([cluster.shape[0], 2]) 
        final_coordinates.append((int(np.mean(cluster[:, 0])),int(np.mean(cluster[:, 1]))))

    return np.array(final_coordinates)


if __name__ == "__main__":

    path = 'chessboard_img.jpg'
    img = cv2.imread(path)
    image = image_preprocessing(img)
    lines = hough_transform(image)
    segmented = segment_by_angle(lines)
    intersections = segmented_intersections(segmented)
    coordinates = final_coordinates(intersections)

    #Display the image with the final coordinates
    img_ = img.copy()
    for point in coordinates:
        pt = (point[0], point[1])
        cv2.circle(img_,pt,3,(0,0,255),-5)
        
    cv2.imshow("Final Coordinates", img_)
    cv2.waitKey()
    cv2.destroyAllWindows()



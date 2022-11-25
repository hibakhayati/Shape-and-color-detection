
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import time


def empty(img) : #on definit une fonction pour les trackbars
    pass



cv2.namedWindow("TrackBar") #Création d'une fenetre intitulé Trackbar
cv2.resizeWindow("TrackBar", 640, 80) #Définir la taille de la fenetre que nous avons créée
cv2.createTrackbar("Threshold1", "TrackBar", 150, 255, empty) #La fenetre TrackBar contient deux paramètres à modifier qui sont
cv2.createTrackbar("Threshold2", "TrackBar", 255, 255, empty) #Threshold1 et Threshold2

video = cv2.VideoCapture(0) #le programme lit a partir de la webcam

# used to record the time when we processed last frame
prev_frame_time = 0
  
# used to record the time at which we processed current frame
new_frame_time = 0


# Définir les intervalles des couleurs rouge,bleu et vert en HSV
red_min1 = np.array([0, 90, 70])
red_max1 = np.array([11, 255, 255])
red_min2 = np.array([161, 50, 70])
red_max2 = np.array([179, 255, 255])
blue_min = np.array([85, 50, 70])
blue_max= np.array([130, 255, 255])
green_min = np.array([36, 25, 25])
green_max = np.array([70, 255, 255])


previousFrame = 0

while True: # Création d'une boucle infinie
    ret, img = video.read(0) # Lecture de la video à travers la webcam
    img = cv2.GaussianBlur(img, (7, 7), 1) # Un petit filtrage appliqué au video
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # Définir imghsv qui est la projection de l'image en couleur RGB en couleur HSV 
    
    new_frame_time = time.time()
    
    # Calculating the fps
  
    # fps will be number of frame processed in given time frame
    # since their will be most of time error of 0.001 second
    # we will be subtracting it to get more accurate result
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
  
    # converting the fps into integer
    fps = int(fps)
  
    # converting the fps to string so that we can display it on frame
    # by using putText function
    fps = str(fps)
    

    Threshold1 = cv2.getTrackbarPos("Threshold1", "TrackBar")  # parametre d affichage de contours
    Threshold2 = cv2.getTrackbarPos("Threshold2", "TrackBar")  # parametre d affichage de contours


    red_mask1 = cv2.inRange(imgHsv, red_min1, red_max1) #créer un premier masque du rouge de la carte des couleurs HSV
    red_mask2 = cv2.inRange(imgHsv, red_min2, red_max2) #créer un deuxième masque du rouge de la carte des couleurs HSV
    red_mask = red_mask1 + red_mask2 # création du masque rouge
    blue_mask = cv2.inRange(imgHsv, blue_min, blue_max) #création du mask du bleu de la carte des couleurs HSV
    green_mask = cv2.inRange(imgHsv, green_min, green_max)
    

    contours_rouge, hierarchy = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #trouver les contours

    shape_detection = imgHsv.copy()

    rectangle_rouge = 0
    cercle_rouge = 0
    triangle_rouge = 0

    for contour in contours_rouge:
        area = cv2.contourArea(contour)

        if area > 1000:
            cv2.drawContours(shape_detection, contour, -1, (0, 255, 0), 5)
            perim = cv2.arcLength(contour, True)
            approximation = cv2.approxPolyDP(contour, 0.02 * perim, True)
            shape_points = len(approximation)
            
            if shape_points == 3:
                triangle_rouge = triangle_rouge + 1
            elif shape_points == 4:
                rectangle_rouge = rectangle_rouge + 1
           
            elif shape_points >= 8:
                cercle_rouge = cercle_rouge + 1  # The cicles have only 8 corners after approxPolyDP


    contours_bleu, hierarchy = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


    rectangle_bleu = 0
    cercle_bleu = 0
    triangle_bleu= 0
    for contour in contours_bleu:
        area = cv2.contourArea(contour)

        if area > 1000:
            cv2.drawContours(shape_detection, contour, -1, (0, 255, 0), 5)
            perimeter = cv2.arcLength(contour, True)
            approximation = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            shape_points = len(approximation)
            
            if  shape_points == 3:
                triangle_bleu = triangle_bleu + 1
            elif shape_points == 4:
                rectangle_bleu = rectangle_bleu + 1
            elif shape_points >= 8:
                cercle_bleu = cercle_bleu + 1  # The cicles have only 8 corners after approxPolyDP
    
    
    contours_vert, hierarchy = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


    rectangle_vert = 0
    cercle_vert = 0
    triangle_vert= 0
    for contour in contours_vert:
        area = cv2.contourArea(contour)

        if area > 1000:
            cv2.drawContours(shape_detection, contour, -1, (0, 255, 0), 5)
            perimeter = cv2.arcLength(contour, True)
            approximation = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            shape_points = len(approximation)
            
            if  shape_points == 3:
                triangle_vert = triangle_vert + 1
            elif shape_points == 4:
                rectangle_vert = rectangle_vert + 1
            elif shape_points >= 8:
                cercle_vert = cercle_vert + 1  # The cicles have only 8 corners after approxPolyDP



    shape_detection = cv2.cvtColor(shape_detection, cv2.COLOR_HSV2BGR)
    
    
    # puting the FPS count on the frame
    cv2.putText(img, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

    # personnalisation du texte du nombre de contours a afficher sur l ecran
    cv2.putText(shape_detection, "Rectangle(s) rouge(s) :" + str(rectangle_rouge), (4, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 255),1)
    cv2.putText(shape_detection, "Cercle(s) rouge(s) :" + str(cercle_rouge), (4, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.putText(shape_detection, "Triangle(s) rouge(s) :" + str(triangle_rouge), (4, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 255) , 1)
    cv2.putText(shape_detection, "Rectangle(s) bleu(s) :" + str(rectangle_bleu), (4, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 0, 0) , 1)
    cv2.putText(shape_detection, "Cercle(s) bleu(s) :" + str(cercle_bleu), (4, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    cv2.putText(shape_detection, "Triangle(s) bleu(s) :" + str(triangle_bleu), (4, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),1)
    cv2.putText(shape_detection, "Rectangle(s) vert(s) :" + str(rectangle_vert), (4, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 255, 0) , 1)
    cv2.putText(shape_detection, "Cercle(s) vert(s) :" + str(cercle_vert), (4, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(shape_detection, "Triangle(s) vert(s) :" + str(triangle_vert), (4, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),1)


    # affichage
    cv2.imshow('Real Time video', img)

    # Show result for testing
    cv2.imshow("Shape_Color_Detection", shape_detection)

    if cv2.waitKey(1) == ord('q'): #l appui sur le bouton 'q' du clavier ferme toutes les fenetres
        break

video.release()
cv2.destroyAllWindows()


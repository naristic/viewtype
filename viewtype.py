import cv2

#video captura ff
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)


#bucle infinito

while True:
    #realizamos lectura de la captura
    ret, frame=cap.read()
    
    if ret == False:
        break

    
    #extrayendo alto y ancho de los fotogramas
    al, an, c=frame.shape

    #tomar centro de la imagen
    #en X
    x1=int(an/3) #
    x2=int(x1*2) #

    #en Y

    y1=int(al/3)
    y2=int(y1*2)

    #texto del recuadro
    cv2.putText(frame,'ubique el ojo en el recuadro',(x1-50,y1-50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    #colocando el recuadro en la zona de analisis
    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0),2)

    #se realiza recorte a la zona de interes
    recorte = frame[y1:y2,x1:x2]

    #pasamos el recorte a escala de girses
    
    gris = cv2.cvtColor(recorte,cv2.COLOR_BGR2GRAY)

    #aplicamos un filtro gaussiano para eliminar pestañas
    gris = cv2.GaussianBlur(gris, (3,3),0)

    #aplicamos un umbral para detectar la pupila por el color
    _, umbral=cv2.threshold(gris, 7,255, cv2.THRESH_BINARY_INV)


    #extraemos los contornos de la zona seleccionada
    contornos, _ = cv2.findContours(umbral, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    #extender area de los contornos 
    #se ordena del mas grande al mas pequeño
    contornos = sorted(contornos, key=lambda x: cv2.contourArea(x), reverse=True)


    for contorno in contornos:

        #dibujamos rectangolo a partir de contorno 
        #sacamos las cordenadas 
        (x, y, ancho, alto )= cv2.boundingRect(contorno)
        
        #dibijamos

        cv2.rectangle(frame, (x+x1, y+y1), (x+ancho+x1, y+alto+y1), (0,255,0),1)
        break

    cv2.imshow("ojos",frame)
   # cv2.imshow("recorte",recorte)
    #cv2.imshow("umbral",umbral)
    t= cv2.waitKey(1)

    if t==27:
        break
cap.release()

import cv2
import numpy as np
from collections import deque

# Configuración de video
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if not ret:
    print("No se pudo acceder a la cámara")
    exit()

# Sustractor de fondo MOG2
fondo = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=40, detectShadows=True)

# Línea vertical para cruce
linea_x = 300
tolerancia = 10  # margen para el cruce

# Estado
historial = deque(maxlen=10)  # guardamos últimos 10 centros detectados
entradas = 0
salidas = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocesamiento con MOG2
    fg = fondo.apply(frame)

    # Limpiar la máscara
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, kernel, iterations=2)
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, kernel, iterations=2)
    fg = cv2.dilate(fg, None, iterations=2)

    # Buscar contornos
    contornos, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contornos:
        contorno_mayor = max(contornos, key=cv2.contourArea)
        if cv2.contourArea(contorno_mayor) > 2000:  # área mínima para evitar ruido
            x, y, w, h = cv2.boundingRect(contorno_mayor)
            centro = (x + w // 2, y + h // 2)
            historial.append(centro)

            # Dibujar rectángulo y centro
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.circle(frame, centro, 5, (0, 0, 255), -1)

            # Verificar cruce de línea con historial
            if len(historial) >= 2:
                x_prev = historial[0][0]
                x_act = historial[-1][0]

                if x_prev < linea_x - tolerancia and x_act > linea_x + tolerancia:
                    entradas += 1
                    historial.clear()  # evitar contar dos veces
                elif x_prev > linea_x + tolerancia and x_act < linea_x - tolerancia:
                    salidas += 1
                    historial.clear()

    # Dibujar línea y contadores
    cv2.line(frame, (linea_x, 0), (linea_x, frame.shape[0]), (0, 255, 255), 2)
    cv2.putText(frame, f"Entradas: {entradas}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, f"Salidas: {salidas}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Mostrar
    cv2.imshow("Detector Entrada/Salida", frame)
    cv2.imshow("Mascara", fg)

    key = cv2.waitKey(30) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("r"):  # resetear el modelo de fondo
        fondo = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=40, detectShadows=True)
        print("Fondo reiniciado")

cap.release()
cv2.destroyAllWindows()
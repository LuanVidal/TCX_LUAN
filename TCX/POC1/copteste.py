import cv2 as cv
import numpy as np

def detectar_alto_falantes(imagem):
    # Carregar a imagem
    img = cv.imread(imagem)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Aplicar um filtro de desfoque para reduzir ruídos
    img_blur = cv.GaussianBlur(img_gray, (5, 5), 0)

    # Detecção de bordas utilizando o algoritmo de Canny
    bordas = cv.Canny(img_blur, 50, 150)

    # Encontrar contornos na imagem
    contornos, _ = cv.findContours(bordas, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Contagem de alto-falantes detectados
    contador = 0

    # Iterar sobre os contornos encontrados
    for contorno in contornos:
        # Calcular a área do contorno
        area = cv.contourArea(contorno)

        # Realizar filtragem com base na área e circularidade
        if area > 1000:
            perimetro = cv.arcLength(contorno, True)
            forma_aproximada = cv.approxPolyDP(contorno, 0.03 * perimetro, True)
            circularidade = 4 * np.pi * (area / (perimetro * perimetro))

            if len(forma_aproximada) > 6 and circularidade > 0.6:
                # Desenhar um círculo em volta do alto-falante
                (x, y), raio = cv.minEnclosingCircle(contorno)
                centro = (int(x), int(y))
                raio = int(raio)
                cv.circle(img, centro, raio, (0, 255, 0), 2)

                # Incrementar o contador de alto-falantes detectados
                contador += 1

    # Exibir a quantidade de alto-falantes encontrados
    cv.putText(img, "Alto-falantes: {}".format(contador), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Exibir a imagem com os alto-falantes detectados
    cv.imshow("Detecção de Alto-falantes", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

# Exemplo de uso
detectar_alto_falantes('POC1/img/image1.jpeg')
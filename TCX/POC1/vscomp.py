import cv2 as cv
import numpy as np

def cont_img(image_packge):

    img = cv.imread(image_packge)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    focus = cv.GaussianBlur(gray, (5, 5), 2)
    detcBoard = cv.Canny(focus, 0, 0)

    contours, _ = cv.findContours(detcBoard, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    count = 0

    for contour in contours:

        area = cv.contourArea(contour)

        if area > 1000:

            (x, y), radius = cv.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)

            circularity = area / (np.pi * radius ** 2)
            if 0.1 <= circularity <= 1.5:

                cv.circle(img, center, radius, (0, 255, 0), 2)
                count += 1

    cv.putText(img, "Alto-falante: {}".format(count), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv.imshow("Image", img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    cv.drawContours(img, contours, -1, (0, 255, 0), 2)
    cv.imshow("Imagem", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

cont_img('POC1/img/image3.jpeg')
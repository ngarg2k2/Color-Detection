import pandas as pd
import cv2

index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
data = pd.read_csv('./colors.csv', names=index, header = None)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

_, frame = cap.read()

clicked = False
r = g = b = xPos = yPos = 0

def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(data)):
        d = abs(R - int(data.loc[i, "R"])) + abs(G - int(data.loc[i, "G"])) + abs(B - int(data.loc[i, "B"]))

        if d <= minimum:
            minimum = d
            colorName = data.loc[i, "color_name"]
    return colorName

def operation(event, x, y, flag, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xPos, yPos, clicked
        clicked = True
        xPos = x
        yPos = y
        b, g, r = frame[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('Frame')   
cv2.setMouseCallback('Frame', operation)
flag = False

while True:
    if clicked:
        flag = True
        color = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

    if flag:
        cv2.putText(frame, color, (10, 70), 2, 0.9, (b, g, r), 2)

    clicked = False
    cv2.imshow("Frame", frame)
    _, frame = cap.read()

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

    
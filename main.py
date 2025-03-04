import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8, maxHands=2)  # Updated initialization
keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                   [ 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
                    ['Z', 'X', 'C', 'V', 'B', 'N','M',',','.','/']]
finalText = ""
def drawAll(img, buttonList):

    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img
class Button():
    def __init__(self, pos, text, size=[85,85]):
        self.pos = pos
        self.size = size
        self.text = text

    #def draw(self, img):

        #return img

buttonList = []
for i in range(len(keys)):
    for x, key in enumerate(keys[i]):
        buttonList.append(Button([100 * x + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, flipType=False)  # With draw
    img = drawAll(img, buttonList)

    # Get the value of the 'lmList' key from the dictionary



    if hands:
        lmList = hands[0]["lmList"]
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if  x < lmList[8][0]<x+w and y < lmList[8][1] < y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                l, k1, k2 = detector.findDistance(lmList[8][0:2],lmList[12][0:2],
                                                  img)
                print(l)
                if l < 30:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    finalText+= button.text
                    sleep(0.5)
    cv2.rectangle(img, (50,350), (700,450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)




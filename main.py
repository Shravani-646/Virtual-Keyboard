import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Key, Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1200)
cap.set(4, 750)
detector = HandDetector(detectionCon=0.8)
BUTTON_HOVER_EFFECT = 5
finalText = ""
keyboard = Controller()
Quit = False

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (128, 0, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    return img


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size


keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "<"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "_"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/","x"]]
buttonList = []

for row in range(len(keys)):
    for button_x_distance, text in enumerate(keys[row]):
        buttonList.append(Button((100 * button_x_distance + 50, 100 * row + 50), text))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)
    if lmList:
        for button in buttonList:
            x, y = button.pos
            h, w = button.size
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:

                cv2.rectangle(img, (x - BUTTON_HOVER_EFFECT, y - BUTTON_HOVER_EFFECT),
                              (x + w + BUTTON_HOVER_EFFECT, y + h + BUTTON_HOVER_EFFECT), (141, 44, 61), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                len, _, _ = detector.findDistance(8, 12, img, draw=False)
                # print(len)
                if len < 30:
                    if button.text == "x":
                        Quit = True
                        break
                    if button.text == "<":
                        keyboard.press(Key.backspace)
                    elif button.text == "_":
                        keyboard.press(Key.space)
                    else:
                        keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (180, 229, 255), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    if button.text == "<":
                        if finalText.__len__() > 0:
                            finalText = finalText.replace(finalText[-1], "")
                    elif button.text == "_":
                        finalText += " "
                    else:
                        finalText += button.text
                    sleep(0.4)
    cv2.rectangle(img, (50, 450), (700, 550), (128, 0, 0), cv2.FILLED)
    cv2.putText(img, finalText, (60, 530), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    cv2.imshow("Image", img)
    if Quit:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

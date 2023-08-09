import cv2
from servo import doorAutomate
from time import sleep

camera = cv2.VideoCapture(0)
classificador = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

reconhecedor = cv2.face.LBPHFaceRecognizer_create()
reconhecedor.read("classificadorLBPH.yml")

def capturar():
    print('Reconhecendo Rosto')
    idSeq = []
    i = 0
    num = 0
    while i < 200:
        success, img = camera.read()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(imgGray)
        faces = classificador.detectMultiScale(imgGray, scaleFactor=1.5, minSize=(50, 50))

        for (x, y, l, a) in faces:
            imgFace = cv2.resize(imgGray[y:y + a, x:x + l], (220, 220))
            cv2.rectangle(img, (x, y), (x + l, y + a), (1, 237, 0), 2)
            id, confianca = reconhecedor.predict(imgFace)
            idSeq.append(id)

            if confianca <= 50:
                num = id

            if num == 1:
                cv2.putText(img, "Acesso liberado", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow('Cam', img)
        k = cv2.waitKey(1)
        i = i + 1
    cv2.destroyAllWindows()

    if idSeq:
        return max(set(idSeq), key=idSeq.count)
    else:
        return -1

def monitor():
    while True:
        success, img = camera.read()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = classificador.detectMultiScale(imgGray, scaleFactor=1.5, minSize=(100, 100))

        if len(faces) > 0:
            print('Face encontrada!')
            return True
        else:
            return False

def main():
    while True:
        print('Monitorando ...')
        num = 0
        comando = monitor()
        if comando:
            num = capturar()
            if num == 0:
                pass
            elif num == -1:
                print('Pessoa desconhecida!')
                sleep(3)
            else:
                print(f'Pessoa reconhecida com nível de confiança: {num}')
                doorAutomate(1)
                sleep(10)
                doorAutomate(0)

if __name__ == "__main__":

    main()
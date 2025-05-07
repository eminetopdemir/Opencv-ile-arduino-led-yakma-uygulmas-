import cv2
import serial
import time

# Arduino seri bağlantısını başlat
arduino = serial.Serial('COM4', 9600)  # Arduino bağlantı portu, değiştirmen gerekebilir
time.sleep(2)  # Bağlantının oturması için bekle

# Yüz tespiti için Haar Cascade sınıflandırıcısını yükle
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Kamerayı başlat
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera görüntüsü alınamadı.")
        break

    # Görüntüyü gri tonlamaya çevir
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yüzleri tespit et
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Algılanan yüz sayısı
    person_count = len(faces)

    # Arduino'ya komut gönder
    if person_count == 0:
        print("Yüz Tespit Edilemedi - LEDLER SÖNÜK")
        arduino.write(b'0')  # Hiç yüz algılanmadı, LED'ler kapalı
    elif person_count == 1:
        print("1 Yüz Tespit Edildi - LED1 YANIK")
        arduino.write(b'1')  # 1 kişi algılandı, sadece LED1 yanar
    elif person_count == 2:
        print("2 Yüz Tespit Edildi - LED2 YANIK")
        arduino.write(b'2')  # 2 kişi algılandı, sadece LED2 yanar
    else:
        print(f"{person_count} Yüz Tespit Edildi - İKİ LED YANIYOR")
        arduino.write(b'3')  # 2'den fazla kişi algılandı, her iki LED de yanar

    # Görüntüyü işaretle ve algılanan yüzleri çerçeve içine al
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Görüntüyü göster
    cv2.putText(frame, f"Yuz Sayisi: {person_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Frame", frame)

    # Çıkış için 'q' tuşuna basın
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
arduino.close()

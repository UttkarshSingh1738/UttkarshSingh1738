from gtts import gTTS
from playsound import playsound
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'D:/Tesseract-OCR/tesseract.exe'
image = cv2.imread('D:\AI-ML\Tesseract OCR 1.png')
text = pytesseract.image_to_string(image)
print(text)
voice_text = ""
for i in text.split():
    voice_text += i + ' '
voice_text = voice_text[:-1]
voice_text
tts = gTTS(voice_text)
tts.save("test.mp3")
playsound("test.mp3")
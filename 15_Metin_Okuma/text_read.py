from PIL import Image
import pytesseract #Metrin okumak için kullanılır
# Resimdeki metni okuma

img = Image.open("opencv\\15_Metin_Okuma\\media\\text2.png")
text = pytesseract.image_to_string(img,lang="eng")
print(text)
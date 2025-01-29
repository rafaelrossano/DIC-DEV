from PIL import ImageGrab

def screnshot():
    try:
        img = ImageGrab.grab()
        img.save(r'base\img\screenshot.jpg')
    except Exception as e:
        print("Erro ao tirar o print.")

import glob
import os
import shutil
from turtle import position
from PIL import Image,ImageOps,ImageEnhance,ImageDraw,ImageFont

print(Image)

class Digitizer:
    def __init__(self,filepath):
        self.filepath = filepath
        self.img = Image.open(filepath).convert("RGBA")
    
    def convert_ascii(self):
        font_size = 10
        letters = [" ", ".","!","-","m","n","f","H","A"]
        (w,h) = self.img.size
        new_width = int(w / font_size)
        new_height = int(h / font_size)
        sample_size = (new_width,new_height)
        final_size = (new_width * font_size , new_height * font_size)

        #make grayscale
        self.make_grayscale()
        self.make_contrast(4.0)
        #resizing the image 10x smaller
        self.img = self.img.resize(sample_size)
        #create a brand new image
        ascii_img = Image.new("RGBA",size=final_size,color="#000000")

        font = ImageFont.truetype("ibm-plex-mono.ttf",10)
        drawer = ImageDraw.Draw(ascii_img)

        for x in range(new_width):
            for y in range(new_height):
                (r,g,b,a) = self.img.getpixel((x,y))

                brightness = r / 256
                letter = letters[int(len(letters) * brightness)]
                position = (x * font_size, y * font_size)
                drawer.text(position,letter,font=font,fill=(255,255,255,255))

        self.img = ascii_img


    def make_upside_down(self,value=180):
        self.img = self.img.rotate(value)
        print('Made upside down')
    
    def make_thumbnail_size(self,size=(128,128)):
        self.img.thumbnail(size)

    def make_grayscale(self):
        self.img = ImageOps.grayscale(self.img)
        self.img = self.img.convert("RGBA")

    def make_square(self,size=200):
        (w,h) = self.img.size

        if w > h:
            print('Landscape')
            x = (w - h) * 0.5
            y = 0
            box = (0,0,h + x ,h + y)
        else:
            print('Portrait')
            x = 0
            y = (h - w) * 0.5
            box = (0,0,x + w,y + w)

        self.img = self.img.resize((size,size),box=box)

    def add_watermark(self):
        font = ImageFont.truetype('ibm-plex-mono.ttf',30)
        drawer = ImageDraw.Draw(self.img)
        drawer.text((20,20),"Danny",font=font)

    def make_contrast(self,amount=1.5):
        enhancer = ImageEnhance.Contrast(self.img)
        self.img = enhancer.enhance(amount)
        
    def save(self,output_filepath):
        if self.filepath.endswith('.jpg'):
            self.img = self.img.convert("RGB")
        self.img.save(output_filepath)
        print('Saved a File!')

if __name__ == "__main__":
    inputs = glob.glob('inputs/*.jpg')
    #create an output folder
    os.makedirs('outputs',exist_ok=True)

    for filename in inputs:
        # #replace the filename input with outputs
        outpath = filename.replace('inputs','outputs')

        image = Digitizer(filename)
        image.convert_ascii()
        image.save(outpath)
from PIL import Image

# Convert webp to jpg
img = Image.open('/home/jeffry/Downloads/celebrities/Elon_Musk_-_54820081119_(cropped).jpg.webp')
rgb_img = img.convert('RGB')
rgb_img.save('frontend/images/elon_musk.jpg', 'JPEG')
print("Converted elon_musk.jpg successfully")

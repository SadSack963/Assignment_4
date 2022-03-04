# https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html#specifying-an-anchor

from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("Tests/fonts/NotoSans-Regular.ttf", 72)
# im = Image.new("RGB", (200, 200), "white")
im = Image.open("images/test_image_1.jpg")
d = ImageDraw.Draw(im)
d.line(((0, 100), (200, 100)), "gray")
d.line(((100, 0), (100, 200)), "gray")
d.text((100, 100), "Quick", fill="white", anchor="ms", font=font)
im.show()

# img = Image.open("images/test_image_1.jpg")
# print(img.format, img.size, img.mode)
# img.show()

"""

I chose to use tkinterDnD rather than tkinterDnD2 because it is so straightforward to install using pip.
There is a bit of faffing around when installing tkinterDnD2, particularly with tkdndn2.8.
See https://pythonguides.com/python-tkinter-drag-and-drop/
Also https://github.com/Eliav2/tkinterdnd2

"""


import tkinter as tk
import tkinterDnD  # pip install python-tkdnd
from PIL import Image, ImageDraw, ImageFont, ImageTk
from time import sleep


def drop(event):
    """
    This function is called when a file is dropped onto the canvas widget.

    :param event: The path to the file is in the data parameter
    :type event: DnDEvent
    """
    label_string.set(event.data)
    display_image(event.data)


def display_image(path):
    """
    Open an image file and display on the canvas.

    :param path: Path to image file
    :type path: string
    """
    global image, base_img, x, y
    # Add an Alpha channel
    base_img = Image.open(path).convert(mode='RGBA')
    # Get coordinates for placing the image
    w, h = base_img.size
    x = w/2
    y = h/2
    # Set the canvas size to fit the image
    my_canvas.config(width=w, height=h)
    # Convert to a tkinter image and place on the canvas
    image = ImageTk.PhotoImage(base_img)
    my_image = my_canvas.create_image(x, y, image=image)


def update_watermark(event):
    global image, base_img
    mouse_x = event.x
    mouse_y = event.y
    img = base_img.copy()
    d = ImageDraw.Draw(img)
    d.text((mouse_x, mouse_y), "\u00A9 John", fill=(255, 255, 255, 127), anchor="mm", font=watermark_font)
    # Convert to a tkinter image and place on the canvas
    image = ImageTk.PhotoImage(img)
    my_image = my_canvas.create_image(x, y, image=image)


# Use the tkinterDnD.Tk object for easy initialization, and use the main window as a dnd widget
root = tkinterDnD.Tk()
root.title("Image Watermark using tkinterDnD")

# A global tag is required by tkinter otherwise the function will not display the updated canvas image.
# (Even weirder, you don't actually need to create this tag - just tell the function that it is global!!)
image = Image.new(mode='RGBA', size=(300, 300), color=(127, 127, 127, 0))
base_img = image.copy()
x = y = 0
watermark_font = ImageFont.truetype("fonts/lcallig.ttf", 72)
label_font = ("fonts/arial.ttf", 16)

# Text to display in the label
label_string = tk.StringVar()
label_string.set('Drop an image file onto the canvas!')

# The label displays the current image file path
label = tk.Label(root, textvariable=label_string, relief="flat", font=label_font)
label.pack(expand=True, padx=10, pady=10)

# Create a canvas to hold the image. Bind to the drop function.
# register_drop_target and similar functions are in dnd.py DnDWrapper class.
# Constants are in constants.py
my_canvas = tk.Canvas(root)
my_canvas.pack(padx=10, pady=10)
my_canvas.register_drop_target(tkinterDnD.FILE)  # only allow dropping of files
# See class DnDWrapper, dnd_bind method for event sequences
my_canvas.bind("<<Drop:File>>", drop)
my_canvas.bind("<B1-Motion>", update_watermark)


# Start the GUI
root.mainloop()

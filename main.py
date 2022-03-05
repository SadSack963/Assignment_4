
import tkinter as tk
import tkinterDnD  # pip install python-tkdnd
from PIL import Image, ImageDraw, ImageFont, ImageTk


def drop(event):
    # This function is called, when stuff is dropped into a widget
    stringvar.set(event.data)
    display_image(event.data)


def display_image(path):
    global image
    im = Image.open(path).convert(mode='RGBA')
    # Get coordinates for placing the image
    w, h = im.size
    x = w/2
    y = h/2
    # Set the canvas size to fit the image
    my_canvas.config(width=w, height=h)
    # Convert to a tkinter image and place on the canvas
    image = ImageTk.PhotoImage(im)
    my_image = my_canvas.create_image(x, y, image=image)


# You have to use the tkinterDnD.Tk object for super easy initialization,
# and to be able to use the main window as a dnd widget
root = tkinterDnD.Tk()
root.title("Image Watermark using tkinterDnD")

# A global tag is required by tkinter otherwise the function will not update the canvas
image = ""
font = ImageFont.truetype("fonts/lcallig.ttf", 72)

# Text to display in the label
stringvar = tk.StringVar()
stringvar.set('Drop an image file on the canvas!')

# The label displays the current image file path
label = tk.Label(root, textvariable=stringvar, relief="flat", font=("fonts/arial.ttf", 16))
label.pack(expand=True, padx=10, pady=10)

# Create a canvas to hold the image. Bind to the drop function.
my_canvas = tk.Canvas(root)
my_canvas.pack(padx=10, pady=10)
my_canvas.register_drop_target(tkinterDnD.FILE)
my_canvas.bind("<<Drop>>", drop)

# Start the GUI
root.mainloop()

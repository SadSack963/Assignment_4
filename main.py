"""

I chose to use tkinterDnD rather than tkinterDnD2 because it is so straightforward to install using pip.
There is a bit of faffing around when installing tkinterDnD2, particularly with tkdndn2.8.
See https://pythonguides.com/python-tkinter-drag-and-drop/
Also https://github.com/Eliav2/tkinterdnd2

"""


import tkinter as tk
import tkinterDnD  # pip install python-tkdnd
from PIL import Image, ImageDraw, ImageFont, ImageTk, UnidentifiedImageError
from time import sleep


def drop(event):
    """
    This function is called when a file is dropped onto the canvas widget.
    Update the label text to show the filepath.
    Call function to display the image on the canvas.

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
    global base_img, text_image, x, y
    try:
        # Load the image from file and add an Alpha channel
        base_img = Image.open(path).convert(mode='RGBA')
        # Make a transparent image the same size to draw text upon
        text_image = Image.new(mode="RGBA", size=base_img.size, color=(255, 255, 255, 0))
    except UnidentifiedImageError:
        print(f"{path} is not recognized as an image file")
        return
    # Get coordinates for placing the image
    w, h = base_img.size
    x = w/2
    y = h/2
    # Set the canvas size to fit the image
    my_canvas.config(width=w, height=h)
    convert_image(base_img)


def move_watermark(event):
    """
    This function is called when the mouse is moved with the left button clicked.
    Get mouse coordinates and draw the watermark text at that location.

    :param event: Mouse event
    :type event: Event
    """
    global wm_x, wm_y
    wm_x = event.x
    wm_y = event.y
    img = text_image.copy()
    img = draw_watermark(img)
    convert_image(img)


def set_opacity(value):
    """
    Called from the Opacity scale.
    Set the watermark opacity.

    :param value: Passed from the scale widget.
    :type value: Integer, 0 to 255
    """
    global watermark_opacity
    watermark_opacity = int(value)
    img = text_image.copy()
    img = draw_watermark(img)
    convert_image(img)


def draw_watermark(img):
    # global text_image
    d = ImageDraw.Draw(img)
    d.text(
        (wm_x, wm_y),
        "\u00A9 John",
        fill=(255, 255, 255, watermark_opacity),
        anchor="mm",
        font=watermark_font,
    )
    return img


def convert_image(img):
    global image
    out_image = Image.alpha_composite(base_img, img)
    # Convert to a tkinter image and place on the canvas
    image = ImageTk.PhotoImage(out_image)
    my_image = my_canvas.create_image(x, y, image=image)


# Use the tkinterDnD.Tk object for easy initialization, and use the main window as a dnd widget
root = tkinterDnD.Tk()
root.title("Image Watermark using tkinterDnD")

# A global tag is required by tkinter otherwise the function will not display the updated canvas image.
# (Even weirder, you don't actually need to create this tag - just tell the function that it is global!!)
# base_image is the image loaded from disk
# text_image is the image upon which the text is drawn
base_img = Image.new(mode='RGBA', size=(1, 1), color=(255, 255, 255, 0))
text_image = base_img.copy()
x = y = 0  # centre point of image
watermark_font = ImageFont.truetype("fonts/lcallig.ttf", 72)
watermark_opacity = 127
wm_opacity_cv = tk.IntVar()
wm_opacity_cv.set(127)
wm_x = wm_y = 0  # centre point of watermark
label_font = ("fonts/arial.ttf", 16)

# Text to display in the label
label_string = tk.StringVar()
label_string.set('Drop an image file onto the canvas!')

# The label displays the current image file path
label = tk.Label(master=root, textvariable=label_string, relief="flat", font=label_font)
label.pack(expand=True, padx=10, pady=10)

# Create a frame to hold the image and controls
frame_main = tk.Frame(master=root)
frame_main.pack(side=tk.BOTTOM)

# Create a canvas to hold the image. Bind to the drop function.
# register_drop_target and similar functions are in dnd.py DnDWrapper class.
# Constants are in constants.py
my_canvas = tk.Canvas(master=frame_main)
my_canvas.pack(side=tk.RIGHT, padx=10, pady=10)
my_canvas.register_drop_target(tkinterDnD.FILE)  # only allow dropping of files
# See class DnDWrapper, dnd_bind method for event sequences
my_canvas.bind("<<Drop:File>>", drop)
my_canvas.bind("<B1-Motion>", move_watermark)

frame_controls = tk.Frame(master=frame_main)
frame_controls.pack(side=tk.LEFT)

slider_opacity = tk.Scale(
    master=frame_controls,
    label="Opacity",
    from_=255,
    to=0,
    variable=wm_opacity_cv,
    orient=tk.VERTICAL,
    command=set_opacity
)
slider_opacity.pack(side=tk.LEFT)

# Start the GUI
root.mainloop()

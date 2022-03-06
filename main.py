"""
Program to add a custom watermark to an image.
"""


import tkinter as tk
from tkinter import messagebox
import tkinterDnD  # pip install python-tkdnd
from PIL import Image, ImageDraw, ImageFont, ImageTk, UnidentifiedImageError


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

    :param value: Percentage passed from the scale widget.
    :type value: String
    """
    global watermark_opacity
    watermark_opacity = int(wm_opacity_cv.get() * 2.55)
    img = text_image.copy()
    img = draw_watermark(img)
    convert_image(img)


def set_color(value):
    global red, green, blue
    red = slider_red.get()
    green = slider_green.get()
    blue = slider_blue.get()
    img = text_image.copy()
    img = draw_watermark(img)
    convert_image(img)


def set_size(value):
    global size, watermark_font
    size = slider_size.get()
    watermark_font = ImageFont.truetype("fonts/lcallig.ttf", size)
    img = text_image.copy()
    img = draw_watermark(img)
    convert_image(img)


def draw_watermark(img):
    # Get the text and strip the newline character from the end
    text = text_watermark.get(index1=1.0, index2=tk.END).strip()
    d = ImageDraw.Draw(img)
    d.text(
        (wm_x, wm_y),
        text=text,
        fill=(red, green, blue, watermark_opacity),
        anchor="mm",
        font=watermark_font,
    )
    return img


def convert_image(img):
    global image, out_image
    out_image = Image.alpha_composite(base_img, img)
    # Convert to a tkinter image and place on the canvas
    image = ImageTk.PhotoImage(out_image)
    my_image = my_canvas.create_image(x, y, image=image)


def save_image():
    path_original = label_string.get()
    if path_original == label_string_default_text:
        messagebox.showerror(title="Error", message="Nothing to save!")
        return
    try:
        index = path_original.rindex('.')
        path = path_original[:index] + '_watermarked' + path_original[index:]
        print(path)
        file_image = out_image.convert(mode="RGB")
        file_image.save(fp=path)
        messagebox.showinfo(title="Success", message=f"Your image was saved to\n{path}")
    except Exception as e:
        print(e)
        messagebox.showerror(title="Error", message=f"Unknown Error!\n{e}\nUnable to save image.")


# Use the tkinterDnD.Tk object for easy initialization, and use the main window as a dnd widget
root = tkinterDnD.Tk()
root.title("Image Watermark using tkinterDnD")

# A global tag is required by tkinter otherwise the function will not display the updated canvas image.
# (Even weirder, you don't actually need to create this tag - just tell the function that it is global!!)
# base_image is the image loaded from disk
# text_image is the image upon which the text is drawn
base_img = Image.new(mode='RGBA', size=(1, 1), color=(255, 255, 255, 0))
text_image = base_img.copy()
out_image = base_img.copy()  # Output image to save
x = y = 0  # centre point of image
watermark_font = ImageFont.truetype("fonts/lcallig.ttf", 36)
wm_opacity_cv = tk.IntVar(value=100)
watermark_opacity = 255
wm_red_cv = tk.IntVar(value=255)
wm_green_cv = tk.IntVar(value=255)
wm_blue_cv = tk.IntVar(value=255)
red = green = blue = 255
wm_size_cv = tk.IntVar(value=36)
size = 36
wm_x = wm_y = 0  # centre point of watermark
label_font = ("fonts/arial.ttf", 16)

# Text to display in the label
label_string = tk.StringVar()
label_string_default_text = 'Drop an image file onto the canvas!'
label_string.set(label_string_default_text)

# The label displays the current image file path
label = tk.Label(master=root, textvariable=label_string, relief="flat", font=label_font)
label.pack(expand=True, padx=10, pady=10)

save_as = tk.Button(master=root, text=" Save ", font=label_font, command=save_image)
save_as.pack()


# Create a frame to hold the image and controls
frame_main = tk.Frame(master=root)
frame_main.pack(side=tk.BOTTOM)

frame_controls = tk.Frame(master=frame_main)
frame_controls.pack(side=tk.LEFT)

frame_text = tk.Frame(master=frame_controls)
frame_text.pack(side=tk.TOP)

label_text = tk.Label(master=frame_text, text="Type your Watermark text here.")
label_text.pack(side=tk.TOP)

text_watermark = tk.Text(master=frame_text, height=3, width=24, wrap=tk.WORD)
text_watermark.pack()

slider_size = tk.Scale(
    master=frame_text,
    label="Size",
    from_=0,
    to=255,
    variable=wm_size_cv,
    orient=tk.HORIZONTAL,
    length=200,
    command=set_size,
)
slider_size.pack(expand=True, side=tk.BOTTOM)

frame_colors = tk.Frame(master=frame_controls)
frame_colors.pack(side=tk.LEFT)

slider_red = tk.Scale(
    master=frame_colors,
    label="Red",
    from_=0,
    to=255,
    variable=wm_red_cv,
    orient=tk.HORIZONTAL,
    command=set_color,
)
slider_red.pack(side=tk.TOP)

slider_green = tk.Scale(
    master=frame_colors,
    label="Green",
    from_=0,
    to=255,
    variable=wm_green_cv,
    orient=tk.HORIZONTAL,
    command=set_color,
)
slider_green.pack()

slider_blue = tk.Scale(
    master=frame_colors,
    label="Blue",
    from_=0,
    to=255,
    variable=wm_blue_cv,
    orient=tk.HORIZONTAL,
    command=set_color,
)
slider_blue.pack()

label_blank_1 = tk.Label(master=frame_colors, text=" ")
label_blank_1.pack(side=tk.BOTTOM)

label_blank_2 = tk.Label(master=frame_controls, text=" ")
label_blank_2.pack()

slider_opacity = tk.Scale(
    master=frame_controls,
    label="Opacity",
    from_=100,
    to=0,
    variable=wm_opacity_cv,
    orient=tk.VERTICAL,
    length=130,
    command=set_opacity,
)
slider_opacity.pack(side=tk.RIGHT, pady=10)

# Create a canvas to hold the image. Bind to the drop function.
# register_drop_target and similar functions are in dnd.py DnDWrapper class.
# Constants are in constants.py
my_canvas = tk.Canvas(master=frame_main)
my_canvas.pack(side=tk.RIGHT, padx=10, pady=10)
my_canvas.register_drop_target(tkinterDnD.FILE)  # only allow dropping of files
# See class DnDWrapper, dnd_bind method for event sequences
my_canvas.bind("<<Drop:File>>", drop)
my_canvas.bind("<B1-Motion>", move_watermark)


# Start the GUI
root.mainloop()

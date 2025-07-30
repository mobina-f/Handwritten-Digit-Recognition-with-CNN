import tkinter as tk
from PIL import Image, ImageDraw, ImageOps
import numpy as np
from tensorflow.keras.models import load_model

# بارگذاری مدل
model = load_model("my_model.keras")

# تنظیمات بوم نقاشی
width = 200
height = 200
bg_color = "black"
fg_color = "white"
brush_size = 15

# ساخت پنجره
root = tk.Tk()
root.title("Draw a Digit (0-9)")

canvas = tk.Canvas(root, width=width, height=height, bg=bg_color)
canvas.pack()

# تصویر پشت صحنه برای پردازش
image1 = Image.new("L", (width, height), color=0)
draw = ImageDraw.Draw(image1)

# نگه‌داری مکان موس و رسم خط
def paint(event):
    x1, y1 = (event.x - brush_size), (event.y - brush_size)
    x2, y2 = (event.x + brush_size), (event.y + brush_size)
    canvas.create_oval(x1, y1, x2, y2, fill=fg_color, outline=fg_color)
    draw.ellipse([x1, y1, x2, y2], fill=255)

canvas.bind("<B1-Motion>", paint)

# تابع پاک‌کردن بوم
def clear():
    canvas.delete("all")
    draw.rectangle([0, 0, width, height], fill=0)

# تابع پیش‌بینی عدد
def predict():
    img = image1.resize((28, 28))
    img = ImageOps.invert(img)
    img = np.array(img).astype("float32") / 255.0
    img = img.reshape(1, 28, 28, 1)
    pred = model.predict(img)
    digit = np.argmax(pred)
    confidence = np.max(pred)
    result_label.config(text=f"Predicted: {digit} ({confidence:.2%})")

# دکمه‌ها
button_frame = tk.Frame(root)
button_frame.pack()

tk.Button(button_frame, text="Predict", command=predict).pack(side="left")
tk.Button(button_frame, text="Clear", command=clear).pack(side="left")

# برچسب نتیجه
result_label = tk.Label(root, text="Draw a digit and press Predict", font=("Arial", 14))
result_label.pack()

root.mainloop()

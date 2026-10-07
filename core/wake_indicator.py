import tkinter as tk

def show():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.configure(bg="black")
    root.attributes("-transparentcolor", "black")

    size = 110
    x = root.winfo_screenwidth() - size - 35
    y = 35
    root.geometry(f"{size}x{size}+{x}+{y}")

    canvas = tk.Canvas(
        root,
        width=size,
        height=size,
        bg="black",
        highlightthickness=0,
    )
    canvas.pack()

    canvas.create_oval(
        8, 8, size - 8, size - 8,
        outline="lime",
        width=6,
    )

    canvas.create_oval(
        25, 25, size - 25, size - 25,
        outline="white",
        width=2,
    )

    root.after(1800, root.destroy)
    root.mainloop()

if __name__ == "__main__":
    show()

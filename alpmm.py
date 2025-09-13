import tkinter as tk
from tkinter import ttk
import webbrowser
import os

class ALPMMApp:
    def __init__(self, alpmm_code):
        self.root = tk.Tk()
        self.root.title("ALPMM App")
        self.root.geometry("600x400")
        self.widgets = []
        self.js_code = ""
        self.css_code = ""
        self.parse(alpmm_code)

    def parse(self, code):
        lines = code.split("\n")
        current_widget = None

        for line in lines:
            line = line.strip()
            if not line: 
                continue

            # ---------------- APP ----------------
            if line.startswith("app.title"):
                self.root.title(line.split('"')[1])
            elif line.startswith("app.size"):
                self.root.geometry(line.split('"')[1])
            elif line.startswith("app.bgcolor"):
                self.root.configure(bg=line.split('"')[1])

            # ---------------- IMPORT ----------------
            elif line.startswith("import css form"):
                css_path = line.split('"')[1]
                if os.path.exists(css_path):
                    with open(css_path, "r", encoding="utf-8") as f:
                        self.css_code = f.read()
            elif line.startswith("import js form"):
                js_path = line.split('"')[1]
                if os.path.exists(js_path):
                    with open(js_path, "r", encoding="utf-8") as f:
                        self.js_code = f.read()

            # ---------------- TEXT ----------------
            elif line.startswith("text."):
                txt = line.split('"')[1]
                label = tk.Label(self.root, text=txt)
                label.pack(pady=5)
                self.widgets.append(label)
                current_widget = label
            elif line.startswith("text.size"):
                size = int(line.split('"')[1])
                current_widget.config(font=("Arial", size))
            elif line.startswith("text.fgcolor"):
                current_widget.config(fg=line.split('"')[1])
            elif line.startswith("text.bgcolor"):
                current_widget.config(bg=line.split('"')[1])

            # ---------------- BUTTON ----------------
            elif line.startswith("button."):
                txt = line.split('"')[1]
                btn = tk.Button(self.root, text=txt)
                btn.pack(pady=5)
                self.widgets.append(btn)
                current_widget = btn
            elif line.startswith("button.bgcolor"):
                current_widget.config(bg=line.split('"')[1])
            elif line.startswith("button.fgcolor"):
                current_widget.config(fg=line.split('"')[1])
            elif line.startswith("onclick.button;alert["):
                # extract javascript inside java[...] 
                if "javascript(" in line:
                    js_func = line.split("javascript(")[1].split(")")[0].strip()
                    current_widget.config(command=lambda j=js_func: self.run_js(j))

    def run_js(self, js_command):
        # save temp HTML to run js + css
        html_code = f"""
        <html>
        <head>
        <style>{self.css_code}</style>
        <script>{self.js_code}</script>
        </head>
        <body>
        <script>{js_command}</script>
        </body>
        </html>
        """
        path = "alpmm_temp.html"
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_code)
        webbrowser.open("file://" + os.path.abspath(path))

    def run(self):
        self.root.mainloop()


# ----------------------------
# Run ALPMM file
# ----------------------------
def run_alpmm_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    app = ALPMMApp(code)
    app.run()

if __name__ == "__main__":
    run_alpmm_file("main.alpmm")

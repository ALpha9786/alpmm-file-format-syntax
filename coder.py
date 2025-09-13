import tkinter as tk
from tkinter import filedialog, scrolledtext
import re
import os

# ---------------- ALPMM EXAMPLE ----------------
ALPMM_CODE = """
# ALPMM IDE Example
app.title "My ALP.mm App"
app.size "600x400"
app.bgcolor "#000000"

text."Hello ALP.mm IDE!"
text.size "20"
text.fgcolor "#ffffff"
text.bgcolor "#000000"

button."Click Me"
button.bgcolor "#4CAF50"
button.fgcolor "#ffffff"
onclick.button;alert[javascript(alert('Hello from ALP.mm!'))]
"""

# ---------------- ALPMM IDE CLASS ----------------
class ALPMMIDE:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ALPMM IDE")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e1e")  # Dark Theme background

        # Editor
        self.editor = scrolledtext.ScrolledText(
            self.root, font=("Consolas", 12), undo=True,
            bg="#1e1e1e", fg="#ffffff", insertbackground="white"
        )
        self.editor.pack(fill="both", expand=True)
        self.editor.insert(tk.END, ALPMM_CODE)
        self.editor.bind("<KeyRelease>", self.on_key_release)

        # Console
        self.console = scrolledtext.ScrolledText(
            self.root, height=10, bg="black", fg="white"
        )
        self.console.pack(fill="x")

        # Menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Run", command=self.run_code)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Syntax Highlighting tags
        self.editor.tag_config("keyword", foreground="#C586C0")
        self.editor.tag_config("string", foreground="#CE9178")
        self.editor.tag_config("comment", foreground="#6A9955")
        self.editor.tag_config("function", foreground="#DCDCAA")

        self.highlight()

    # ---------------- File Operations ----------------
    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("ALPMM Files", "*.alpmm")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, f.read())
            self.highlight()

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".alpmm", filetypes=[("ALPMM Files", "*.alpmm")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.get("1.0", tk.END))

    # ---------------- Syntax Highlight ----------------
    def highlight(self, event=None):
        content = self.editor.get("1.0", tk.END)
        self.editor.tag_remove("keyword", "1.0", tk.END)
        self.editor.tag_remove("string", "1.0", tk.END)
        self.editor.tag_remove("comment", "1.0", tk.END)
        self.editor.tag_remove("function", "1.0", tk.END)

        # Highlight comments
        for match in re.finditer(r"#.*", content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.editor.tag_add("comment", start, end)

        # Highlight strings
        for match in re.finditer(r'"[^"]*"', content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.editor.tag_add("string", start, end)

        # Highlight keywords
        keywords = ["app.title", "app.size", "app.bgcolor", "text.", "button.", "onclick.button"]
        for kw in keywords:
            for match in re.finditer(re.escape(kw), content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.editor.tag_add("keyword", start, end)

    def on_key_release(self, event=None):
        self.highlight()

    # ---------------- Run ALPMM CODE ----------------
    def run_code(self):
        code = self.editor.get("1.0", tk.END)
        output = self.run_alpmm_code(code)
        self.console.delete("1.0", tk.END)
        self.console.insert(tk.END, output)

    def run_alpmm_code(self, code):
        output = ""
        lines = code.splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # APP settings
            if line.startswith("app.title"):
                output += f"Set app title: {line.split('\"')[1]}\n"
            elif line.startswith("app.size"):
                output += f"Set app size: {line.split('\"')[1]}\n"
            elif line.startswith("app.bgcolor"):
                output += f"Set app bg color: {line.split('\"')[1]}\n"
            # TEXT
            elif line.startswith("text."):
                txt = line.split('"')[1]
                output += f"Text: {txt}\n"
            # BUTTON
            elif line.startswith("button."):
                txt = line.split('"')[1]
                output += f"Button: {txt}\n"
            # BUTTON JS
            elif line.startswith("onclick.button;alert["):
                if "javascript(" in line:
                    js_func = line.split("javascript(")[1].split(")")[0].strip()
                    output += f"Run JS: {js_func}\n"
                    html_code = f"<script>{js_func}</script>"
                    path = "alpmm_temp.html"
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(html_code)
        return output

    # ---------------- Run IDE ----------------
    def run(self):
        self.root.mainloop()


# ---------------- RUN ----------------
if __name__ == "__main__":
    ide = ALPMMIDE()
    ide.run()

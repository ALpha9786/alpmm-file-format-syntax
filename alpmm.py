import sys
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from tkinter import font as tkfont

# ==============================
# Alp-- Engine + CSS-like Styling
# ==============================
class AlpParser:
    def __init__(self, code):
        self.code = code.splitlines()
        self.ast = []

    def parse(self):
        for line in self.code:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            self.ast.append(self._parse_line(line))
        return self.ast

    def _parse_line(self, line):
        if line.startswith("import"):
            return {"type":"import","value":line.replace("import","").strip()}
        if line.startswith("app.title"):
            return {"type":"title","value":line.split("[")[-1].rstrip("]")}
        if line.startswith("app.size"):
            return {"type":"size","value":line.split("[")[-1].rstrip("]")}
        if line.startswith("text."):
            content = line.replace("text.","").strip("[]\"")
            return {"type":"text","value":content}
        if line.startswith("text.style"):
            style = line.replace("text.style","").strip("[]\"")
            return {"type":"text.style","value":style}
        if line.startswith("button.text"):
            content = line.replace("button.text","").strip("[]\"")
            return {"type":"button","value":content}
        if line.startswith("button.style"):
            style = line.replace("button.style","").strip("[]\"")
            return {"type":"button.style","value":style}
        if line.startswith("input."):
            content = line.replace("input.","").strip("[]\"")
            return {"type":"input","value":content}
        if line.startswith("image."):
            return {"type":"image","value":line.replace("image.","").strip("[]\"")}
        if line.startswith("filedialog."):
            return {"type":"filedialog","value":line.replace("filedialog.","").strip("[]\"")}
        if line.startswith("checkbox."):
            return {"type":"checkbox","value":line.replace("checkbox.","").strip("[]\"")}
        if line.startswith("dropdown."):
            options = line.replace("dropdown.","").split(",")
            return {"type":"dropdown","value":[opt.strip() for opt in options]}
        if line.startswith("slider."):
            value = line.replace("slider.","").strip()
            return {"type":"slider","value":value}
        if line.startswith("tabview."):
            tabs = line.replace("tabview.","").split(",")
            return {"type":"tabview","value":[tab.strip() for tab in tabs]}
        if line.startswith("onclick"):
            return {"type":"event","value":line}
        return {"type":"raw","value":line}

def parse_style(style_str):
    styles = {}
    for item in style_str.split(";"):
        if ":" in item:
            k,v = item.split(":")
            styles[k.strip()] = v.strip()
    return styles

def apply_style(widget, styles, widget_type="text"):
    if not styles: return
    if "font-size" in styles or "font-family" in styles:
        size = int(styles.get("font-size","14").replace("px",""))
        family = styles.get("font-family","Arial")
        fnt = tkfont.Font(family=family,size=size)
        widget.config(font=fnt)
    if "color" in styles:
        widget.config(fg=styles["color"])
    if "background" in styles:
        widget.config(bg=styles["background"])

class AlpApp:
    def __init__(self, ast):
        self.ast = ast
        self.root = tk.Tk()
        self._last_button = None
        self._inputs = []
        self._checkboxes = []
        self._dropdowns = []
        self._sliders = []
        self._tabs = None
        self._last_text_widget = None

    def build(self):
        text_styles = {}
        button_styles = {}
        for node in self.ast:
            t = node["type"]
            if t=="title":
                self.root.title(node["value"])
            elif t=="size":
                self.root.geometry(node["value"])
            elif t=="text":
                lbl = tk.Label(self.root,text=node["value"])
                lbl.pack(pady=5)
                self._last_text_widget = lbl
                if text_styles:
                    apply_style(lbl,text_styles)
            elif t=="text.style":
                text_styles = parse_style(node["value"])
                if self._last_text_widget:
                    apply_style(self._last_text_widget,text_styles)
            elif t=="button":
                btn = tk.Button(self.root,text=node["value"])
                btn.pack(pady=5)
                self._last_button = btn
                if button_styles:
                    apply_style(btn,button_styles,"button")
            elif t=="button.style":
                button_styles = parse_style(node["value"])
                if self._last_button:
                    apply_style(self._last_button,button_styles,"button")
            elif t=="input":
                entry = tk.Entry(self.root)
                entry.insert(0,node["value"])
                entry.pack(pady=5)
                self._inputs.append(entry)
            elif t=="checkbox":
                var = tk.BooleanVar()
                chk = tk.Checkbutton(self.root,text=node["value"],variable=var)
                chk.pack()
                self._checkboxes.append(var)
            elif t=="dropdown":
                combo = ttk.Combobox(self.root,values=node["value"])
                combo.current(0)
                combo.pack(pady=5)
                self._dropdowns.append(combo)
            elif t=="slider":
                s = tk.Scale(self.root,from_=0,to=int(node["value"]),orient=tk.HORIZONTAL)
                s.pack(pady=5)
                self._sliders.append(s)
            elif t=="tabview":
                self._tabs = ttk.Notebook(self.root)
                for tab_name in node["value"]:
                    frame = tk.Frame(self._tabs)
                    self._tabs.add(frame,text=tab_name)
                self._tabs.pack(expand=True,fill="both")
            elif t=="event":
                if "onclick" in node["value"] and self._last_button:
                    if "alert" in node["value"]:
                        msg = node["value"].split("alert")[-1].strip("[]\"")
                        self._last_button.config(command=lambda: messagebox.showinfo("Alert",msg))

    def run(self):
        self.root.mainloop()

def run_alpmm_file(filename):
    with open(filename,"r",encoding="utf-8") as f:
        code = f.read()
    parser = AlpParser(code)
    ast = parser.parse()
    app = AlpApp(ast)
    app.build()
    app.run()

if __name__=="__main__":
    run_alpmm_file("main.alpmm") #change main to your file but best performance in vs code

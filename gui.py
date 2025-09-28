\
"""
Tkinter GUI definition.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional

from models import get_available_models, BaseModel
from utils import human_error, AppError, explain_oop_choices
import oop_demo

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HIT137 – Group Assignment 3 (Tkinter + Hugging Face + OOP)")
        self.geometry("1080x720")
        self._models = get_available_models()
        self.configure(bg="#f2f2f2")  # light gray background
        self._current_model: Optional[BaseModel] = None
        self._build_menu()
        self._build_layout()

    # ----- Menus -----
    def _build_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Quit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)

    def _show_about(self):
        messagebox.showinfo(
            "About",
            "HIT137 – Group Assignment 3\nTwo Hugging Face models with OOP concepts in a Tkinter GUI.\n"
            "Made by GAGANDEEP GAGANDEEP\nMAAN MAAN SINGH\nMANISHA MAHARJAN\nNISHCHALA TIWARI"
        )

    # ----- Layout -----
    def _build_layout(self):
        # Top controls
        top = ttk.Frame(self)
        top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Label(top, text="Model:").pack(side=tk.LEFT)
        self.model_var = tk.StringVar(value=list(self._models.keys())[0])
        self.model_combo = ttk.Combobox(top, textvariable=self.model_var, values=list(self._models.keys()), state="readonly", width=40)
        self.model_combo.pack(side=tk.LEFT, padx=8)
        self.model_combo.bind("<<ComboboxSelected>>", lambda e: self._on_model_change())

        ttk.Label(top, text="Input Type:").pack(side=tk.LEFT, padx=(16, 0))
        self.input_type = tk.StringVar(value="Text")
        self.input_combo = ttk.Combobox(top, textvariable=self.input_type, values=["Text", "Image"], state="readonly", width=10)
        self.input_combo.pack(side=tk.LEFT, padx=8)
        self.input_combo.bind("<<ComboboxSelected>>", lambda e: self._refresh_input_panel())

        self.execute_btn = ttk.Button(top, text="Execute", command=self._on_run)
        self.execute_btn.pack(side=tk.LEFT, padx=12)   


        # Paned window: left inputs + right outputs/info
        body = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel (inputs)
        self.left = ttk.Frame(body)
        body.add(self.left, weight=1)

        # Right panel (outputs + info)
        self.right = ttk.Notebook(body)
        body.add(self.right, weight=2)

        # Output tab
        self.output_frame = ttk.Frame(self.right)
        self.right.add(self.output_frame, text="Output")
        self.output_text = tk.Text(self.output_frame, wrap="word", height=18)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        clear_btn = ttk.Button(self.output_frame, text="Clear Output", command=lambda: self.output_text.delete("1.0", tk.END))
        clear_btn.pack(side=tk.BOTTOM, pady=5)

        # Model Info tab
        self.info_frame = ttk.Frame(self.right)
        self.right.add(self.info_frame, text="Model Info")
        self.info_text = tk.Text(self.info_frame, wrap="word", height=12)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # OOP Explanations tab
        self.oop_frame = ttk.Frame(self.right)
        self.right.add(self.oop_frame, text="OOP Explanations")
        self.oop_text = tk.Text(self.oop_frame, wrap="word", height=12)
        self.oop_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Build input panel
        self._text_input = None
        self._image_path_var = tk.StringVar(value="")
        self._build_text_input_panel()
        self._on_model_change()
        self._write_oop_explanations()

    def _write_oop_explanations(self):
        self.oop_text.delete("1.0", tk.END)
        self.oop_text.insert(tk.END, "Project OOP choices:\n")
        self.oop_text.insert(tk.END, explain_oop_choices())
        self.oop_text.insert(tk.END, "\nAdditional demo (not executed):\n")
        self.oop_text.insert(tk.END, oop_demo.short_demo_text())

    def _build_text_input_panel(self):
        # Clear left frame
        for child in self.left.winfo_children():
            child.destroy()
        # Text input widgets
        ttk.Label(self.left, text="Enter text for sentiment analysis:").pack(anchor="w", padx=4, pady=(0,4))
        self._text_input = tk.Text(self.left, height=8)
        self._text_input.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    def _build_image_input_panel(self):
        for child in self.left.winfo_children():
            child.destroy()
        row = ttk.Frame(self.left)
        row.pack(fill=tk.X, padx=4, pady=4)
        ttk.Label(row, text="Choose an image file for classification:").pack(side=tk.LEFT)
        ttk.Button(row, text="Browse...", command=self._pick_image).pack(side=tk.LEFT, padx=6)
        ttk.Entry(self.left, textvariable=self._image_path_var).pack(fill=tk.X, padx=4, pady=4)

    def _pick_image(self):
        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp"), ("All files", "*.*")],
        )
        if path:
            self._image_path_var.set(path)

    def _refresh_input_panel(self):
        kind = self.input_type.get()
        if kind == "Text":
            self._build_text_input_panel()
        else:
            self._build_image_input_panel()

    def _on_model_change(self):
        # Instantiate fresh model
        model_key = self.model_var.get()
        model_cls = self._models.get(model_key)
        if model_cls:
            self._current_model = model_cls()
            self._write_model_info()

    def _write_model_info(self):
        self.info_text.delete("1.0", tk.END)
        if self._current_model:
            self.info_text.insert(tk.END, f"Name: {self._current_model.name}\n")
            self.info_text.insert(tk.END, f"Task: {self._current_model.task}\n\n")
            self.info_text.insert(tk.END, self._current_model.model_info())

    def _on_run(self):
        if not self._current_model:
            messagebox.showwarning("No model", "Please choose a model first.")
            return
        try:
            if self.input_type.get() == "Text":
                txt = (self._text_input.get("1.0", tk.END) or "").strip()
                result = self._current_model.run(txt)  # validate_nonempty decorator applied on text model
            else:
                path = self._image_path_var.get().strip()
                if not path:
                    raise AppError("Please select an image file first.")
                result = self._current_model.run(path)
            # Show output
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Summary: {result.summary}\n\n")
            self.output_text.insert(tk.END, f"Raw: {result.raw}\n")
        except Exception as e:
            messagebox.showerror("Error", human_error(e))

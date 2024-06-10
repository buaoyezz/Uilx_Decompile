import os
import subprocess
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, END, Text
from datetime import datetime
import uncompyle6

class PycDecompilerApp:
    def __init__(self, root):
        self.root = root
        root.iconbitmap('./assets/icon/logo.ico')
        self.root.title("Uilx_Decompile || Ver 1.0.0.0 || 2024.6.10")

        self.engine = ttk.StringVar(value="pycdc")
        self.style = ttk.Style("darkly")
        self.engine_paths = {
            "pycdc": "./assets/kernel/pycdc/pycdc.exe",
            "jd_gui": "./assets/kernel/JD-GUI/jd-gui.exe",
            "PyInstaller_Extractor": "./assets/kernel/pyinstxtractor/pyinstxtractor.py"
        }
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root, bootstyle="darkly")
        self.notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.home_frame = self.create_frame(self.notebook, 'Home')
        self.add_home_content()

        self.manual_frame = self.create_frame(self.notebook, '程序逆向')
        self.create_manual_content()

        self.pyc_frame = self.create_frame(self.notebook, '反编译')
        self.create_pyc_content()

        self.log_frame = self.create_frame(self.notebook, 'Log')
        self.create_log_content()

        self.about_frame = self.create_frame(self.notebook, 'About')
        self.add_about_content()

        ttk.Button(self.root, bootstyle="dark",text="Exit", command=self.root.quit).grid(row=1, column=0, pady=5, padx=5, sticky="e")

    def create_frame(self, parent, text):
        frame = ttk.Frame(parent)
        parent.add(frame, text=text)
        return frame

    def create_manual_content(self):
        ttk.Button(self.manual_frame, bootstyle="dark",text="选择程序", command=self.select_exe_file_manual).grid(row=0, column=0, pady=5, padx=5)
        ttk.Button(self.manual_frame, bootstyle="dark",text="开始Dec", command=self.manual_decompile).grid(row=0, column=1, pady=5, padx=5)
        self.manual_result_text = Text(self.manual_frame, wrap="word", height=15, width=60)
        self.manual_result_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        ttk.Button(self.manual_frame, bootstyle="warning",text="清空结果框", command=lambda: self.clear_text(self.manual_result_text)).grid(row=0, column=2, pady=5, padx=5)

    def create_pyc_content(self):
        ttk.Label(self.pyc_frame, text="选择你要使用的引擎:").grid(row=0, column=0, pady=5, padx=5, sticky=W)
        engines = ["pycdc[推荐]", "uncompyle6", "jd_gui[.java]", "PyInstaller_Extractor"]
        for i, engine in enumerate(engines):
            ttk.Radiobutton(self.pyc_frame, text=engine.capitalize(), variable=self.engine, value=engine).grid(row=0, column=i+1, padx=5, sticky=W)

        ttk.Button(self.pyc_frame, bootstyle="info" , text="选择文件", command=self.select_files).grid(row=1, column=0, pady=5, padx=5)
        ttk.Button(self.pyc_frame, bootstyle="info" , text="开始反编译", command=self.decompile_files).grid(row=1, column=1, pady=5, padx=5)
        ttk.Button(self.pyc_frame, bootstyle="info", text="导出结果框内结果", command=self.export_results).grid(row=1, column=2, pady=5, padx=5)
        self.result_text = Text(self.pyc_frame, wrap="word", height=15, width=60)
        self.result_text.grid(row=2, column=0, columnspan=6, padx=5, pady=5)
        ttk.Button(self.pyc_frame, bootstyle="warning", text="清空结果框", command=lambda: self.clear_text(self.result_text)).grid(row=1, column=3, pady=5, padx=5)

    def create_log_content(self):
        self.log_text = Text(self.log_frame, wrap="word", height=15, width=60)
        self.log_text.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        ttk.Button(self.log_frame, bootstyle="success",text="导出日志", command=self.export_log).grid(row=1, column=0, pady=5, padx=5)
        ttk.Button(self.log_frame, bootstyle="danger", text="清空日志框", command=lambda: self.clear_text(self.log_text)).grid(row=1, column=1, pady=5, padx=5)

    def add_home_content(self):
        ttk.Label(self.home_frame, text=" Uilx Decompile\n================", font=("Helvetica", 48), anchor="center").grid(row=0, column=0, pady=20, padx=10)
        ttk.Label(self.home_frame, text="", wraplength=500, anchor="center").grid(row=1, column=0, pady=20, padx=10)
        ttk.Label(self.home_frame, text="     See the tabbar above for all the features\n                     Welcome Uilx_dec", font=("Helvetica", 16), anchor="center").grid(row=2, column=0, pady=20, padx=10)

    def add_about_content(self):
        ttk.Label(self.about_frame, text="Uilx_Decompile\n================", font=("Helvetica", 48), anchor="center").grid(row=0, column=0, pady=20, padx=10)
        about_text = """
         Uilx Are Tools of Python Programming Language.
         This Tools are Free And Can Help Quick To Decompile PYC Files.
         Powered By ZZBuAoYe in CN 
         Ver-1.0.0.0Beta
         Uilx->>[Pycdc]-[uncompyle6]-[jd-gui]-[PyInstaller_Extractor]
        """
        ttk.Label(self.about_frame, text=about_text, wraplength=500, anchor="s").grid(row=1, column=0, pady=20, padx=10)

    def select_exe_file_manual(self):
        self.exefilepath = filedialog.askopenfilename(filetypes=[("EXE files", "*.exe")])
        if self.exefilepath:
            self.manual_result_text.insert(END, f"Selected file: {self.exefilepath}\n")

    def manual_decompile(self):
        if not hasattr(self, 'exefilepath') or not self.exefilepath:
            messagebox.showwarning("No files selected", "Please select an EXE file to decompile.")
            return
        threading.Thread(target=self.extract_and_decompile, args=(self.exefilepath, self.manual_result_text)).start()

    def extract_and_decompile(self, exefilepath, text_widget):
        try:
            engine_path = self.engine_paths.get(self.engine.get())
            if engine_path is None:
                messagebox.showwarning("Engine not found", "Selected engine path is not defined.")
                return

            if self.engine.get() == "PyInstaller_Extractor":
                pyinstxtractor_cmd = ["python", engine_path, exefilepath]
                result = subprocess.run(pyinstxtractor_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
                text_widget.insert(END, f"Extracting .pyc from {exefilepath}:\n{result.stdout}\n")

                if result.stderr:
                    self.log_error(result.stderr)

                extracted_dir = os.path.dirname(exefilepath)
                pyc_files = [os.path.join(extracted_dir, f) for f in os.listdir(extracted_dir) if f.endswith(".pyc")]

                for pyc_file in pyc_files:
                    if not self.decompile_pyc_with_pyinstxtractor(pyc_file, text_widget):
                        self.decompile_with_engine(engine_path, pyc_file)

            else:
                cmd = [engine_path, exefilepath]
                result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
                text_widget.insert(END, f"Decompiled {exefilepath} with {self.engine.get()}:\n{result.stdout}\n")

                if result.stderr:
                    self.log_error(result.stderr)

        except Exception as e:
            self.log_error(str(e))

    def decompile_pyc_with_pyinstxtractor(self, pyc_file, text_widget):
        try:
            cmd = ["./assets/kernel/pycdc/pycdc.exe", pyc_file]
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            text_widget.insert(END, f"Decompiled {pyc_file} with pycdc:\n{result.stdout}\n")

            if result.stderr:
                self.log_error(result.stderr)
                return False

            self.save_decompiled_result(pyc_file, result.stdout)

            return True
        except Exception as e:
            self.log_error(str(e))
            return False

    def select_files(self):
        self.filepaths = filedialog.askopenfilenames(filetypes=[("PYC files", "*.pyc")])
        if self.filepaths:
            self.result_text.insert(END, f"Selected files: {self.filepaths}\n")

    def decompile_files(self):
        if not hasattr(self, 'filepaths') or not self.filepaths:
            messagebox.showwarning("No files selected", "Please select PYC files to decompile.")
            return

        for filepath in self.filepaths:
            threading.Thread(target=self.decompile_file, args=(filepath,)).start()

    def decompile_file(self, filepath):
        engine_path = self.engine_paths.get(self.engine.get())
        if engine_path is None:
            messagebox.showwarning("Engine not found", "Selected engine path is not defined.")
            return

        threading.Thread(target=self.decompile_with_engine, args=(engine_path, filepath)).start()

    def decompile_with_engine(self, engine_path, filepath):
        try:
            if self.engine.get() == "uncompyle6":
                with open(filepath, "rb") as f_in, open(filepath.replace(".pyc", ".py"), "w") as f_out:
                    uncompyle6.decompile_file(f_in, f_out)
                with open(filepath.replace(".pyc", ".py"), "r") as f_out:
                    self.result_text.insert(END, f"Decompiled {filepath} with uncompyle6:\n{f_out.read()}\n")
            else:
                cmd = [engine_path, filepath]
                result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
                self.result_text.insert(END, f"Decompiled {filepath} with {self.engine.get()}:\n{result.stdout}\n")

                if result.stderr:
                    self.log_error(result.stderr)

        except Exception as e:
            self.log_error(str(e))

    def export_results(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if save_path:
            with open(save_path, "w", encoding='utf-8') as f:
                f.write(self.result_text.get(1.0, END))

    def export_log(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if save_path:
            with open(save_path, "w", encoding='utf-8') as f:
                f.write(self.log_text.get(1.0, END))

    def clear_text(self, text_widget):
        text_widget.delete(1.0, END)

    def log_error(self, error_message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(END, f"{timestamp} - ERROR: {error_message}\n")

    def save_decompiled_result(self, filepath, result):
        result_dir = "./assets/result/"
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        result_path = os.path.join(result_dir, os.path.basename(filepath).replace(".pyc", ".py"))
        with open(result_path, "w", encoding='utf-8') as f:
            f.write(result)


if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = PycDecompilerApp(root)
    root.mainloop()

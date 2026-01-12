import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from core.stego_core import Steganography
from core.metrics import StegoMetrics
import os

class StegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual Steganography Tool")
        self.root.geometry("600x500")
        
        self.stego = Steganography()
        self.metrics = StegoMetrics()
        
        self.selected_file = None
        
        self._init_ui()
        
    def _init_ui(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 1. File Selection
        self.lbl_file = ttk.Label(main_frame, text="No file selected")
        self.lbl_file.pack(pady=5)
        
        btn_browse = ttk.Button(main_frame, text="Select Image", command=self.browse_file)
        btn_browse.pack(pady=5)
        
        # 2. Notebook for Hide / Reveal
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # --- Tab 1: Hide Message ---
        tab_hide = ttk.Frame(notebook)
        notebook.add(tab_hide, text="Hide Message")
        
        ttk.Label(tab_hide, text="Secret Message:").pack(pady=5)
        self.txt_message = tk.Text(tab_hide, height=5)
        self.txt_message.pack(fill=tk.X, padx=5)
        
        btn_hide = ttk.Button(tab_hide, text="Encrypt & Hide", command=self.do_hide)
        btn_hide.pack(pady=10)
        
        # --- Tab 2: Reveal Message ---
        tab_reveal = ttk.Frame(notebook)
        notebook.add(tab_reveal, text="Reveal Message")
        
        btn_reveal = ttk.Button(tab_reveal, text="Decrypt & Reveal", command=self.do_reveal)
        btn_reveal.pack(pady=10)
        
        self.txt_output = tk.Text(tab_reveal, height=10, state='disabled')
        self.txt_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 3. Status Bar
        self.status = tk.StringVar()
        self.status.set("Ready")
        statusbar = ttk.Label(main_frame, textvariable=self.status, relief=tk.SUNKEN, anchor=tk.W)
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")])
        if filename:
            self.selected_file = filename
            self.lbl_file.config(text=os.path.basename(filename))
            self.status.set(f"Selected: {filename}")
            
    def do_hide(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select an image first.")
            return
            
        msg = self.txt_message.get("1.0", tk.END).strip()
        if not msg:
            messagebox.showwarning("Warning", "Please enter a message.")
            return
            
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Images", "*.png")])
        if not output_path:
            return
            
        self.status.set("Encoding...")
        self.root.update()
        
        try:
            self.stego.encode(self.selected_file, msg, output_path)
            
            # Calculate metrics
            mse = self.metrics.calculate_mse(self.selected_file, output_path)
            psnr = self.metrics.calculate_psnr(self.selected_file, output_path)
            
            info = f"Message hidden successfully!\n\nMetrics:\nMSE: {mse:.5f}\nPSNR: {psnr:.2f} dB"
            messagebox.showinfo("Success", info)
            self.status.set("Ready")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Error occurred")

    def do_reveal(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select an image first.")
            return
            
        self.status.set("Decoding...")
        self.root.update()
        
        try:
            msg = self.stego.decode(self.selected_file)
            
            self.txt_output.config(state='normal')
            self.txt_output.delete("1.0", tk.END)
            self.txt_output.insert(tk.END, msg)
            self.txt_output.config(state='disabled')
            
            self.status.set("Ready")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Error occurred")

def main():
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

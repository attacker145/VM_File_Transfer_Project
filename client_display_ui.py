import requests
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys

class FileUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Uploader")
        self.root.geometry("400x200")

        # Server URL input
        tk.Label(root, text="Server URL:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.url_entry = tk.Entry(root, width=40)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        self.url_entry.insert(0, "http://172.20.10.5:8000")

        # File path input
        tk.Label(root, text="File Path:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.path_entry = tk.Entry(root, width=40)
        self.path_entry.grid(row=1, column=1, padx=5, pady=5)

        # Browse button
        tk.Button(root, text="Browse", command=self.browse_file).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Upload button
        tk.Button(root, text="Upload File", command=self.upload_file).grid(row=3, column=0, columnspan=2, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, file_path)

    def upload_file(self):
        file_path = self.path_entry.get()
        server_url = self.url_entry.get()

        if not file_path or not server_url:
            messagebox.showerror("Error", "Please provide both file path and server URL")
            return

        if not os.path.isfile(file_path):
            messagebox.showerror("Error", f"File {file_path} does not exist")
            return

        filename = os.path.basename(file_path)
        try:
            with open(file_path, 'rb') as f:
                headers = {'X-Filename': filename}
                response = requests.post(server_url, headers=headers, data=f)

            if response.status_code == 200:
                messagebox.showinfo("Success", "File uploaded successfully")
            else:
                messagebox.showerror("Error", f"Upload failed: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def check_display_and_run():
    if 'DISPLAY' not in os.environ:
        try:
            # Attempt to start Xvfb if DISPLAY is not set
            xvfb_process = subprocess.Popen(
                ['Xvfb', ':99', '-screen', '0', '1280x1024x24'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            os.environ['DISPLAY'] = ':99'
            print("Started Xvfb on :99")
        except FileNotFoundError:
            print("Error: Xvfb not installed. Please install it using 'sudo apt-get install xvfb' on Debian/Ubuntu.")
            sys.exit(1)
        except Exception as e:
            print(f"Error starting Xvfb: {str(e)}")
            sys.exit(1)
    try:
        root = tk.Tk()
        app = FileUploaderApp(root)
        root.mainloop()
    finally:
        # Clean up Xvfb process if it was started
        if 'xvfb_process' in locals():
            xvfb_process.terminate()


if __name__ == '__main__':
    check_display_and_run()

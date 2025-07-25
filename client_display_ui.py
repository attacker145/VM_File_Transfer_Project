import requests
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys
import time
import traceback
from urllib.parse import urlparse

class FileUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Uploader")
        self.root.geometry("400x200")
        self.root.resizable(False, False)

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
        tk.Button(root, text="Upload File", command=self.upload_file).grid(row=3, column=0, columnspan=2, pady=10, padx=5)

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

        parsed_url = urlparse(server_url)
        if not parsed_url.scheme.startswith("http"):
            messagebox.showerror("Error", "Invalid server URL, please include http:// or https://")
            return

        if not os.path.isfile(file_path):
            messagebox.showerror("Error", f"File {file_path} does not exist")
            return

        filename = os.path.basename(file_path)
        try:
            with open(file_path, 'rb') as f:
                # If your server expects raw data:
                headers = {'X-Filename': filename}
                response = requests.post(server_url, headers=headers, data=f)

                # If your server expects multipart/form-data, use instead:
                # files = {'file': (filename, f)}
                # response = requests.post(server_url, files=files)

            if response.status_code == 200:
                messagebox.showinfo("Success", "File uploaded successfully")
            else:
                messagebox.showerror("Error", f"Upload failed: {response.text}")
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def check_display_and_run():
    xvfb_process = None
    if 'DISPLAY' not in os.environ:
        try:
            xvfb_process = subprocess.Popen(
                ['Xvfb', ':99', '-screen', '0', '1280x1024x24', '-ac'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            time.sleep(1)

            # Check if Xvfb is still running
            if xvfb_process.poll() is not None and xvfb_process.returncode != 0:
                stderr = xvfb_process.stderr.read()
                print(f"Xvfb failed to start: {stderr}")
                sys.exit(1)

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
        root.update()  # Test display connection
        print("Successfully connected to display")
        app = FileUploaderApp(root)
        root.mainloop()
    except tk.TclError as e:
        print(f"Tkinter error: {str(e)}")
        sys.exit(1)
    finally:
        if xvfb_process is not None:
            xvfb_process.terminate()
            xvfb_process.wait()
            print("Terminated Xvfb")


if __name__ == '__main__':
    check_display_and_run()

import requests
import os


def upload_file(file_path, server_url):
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist")
        return

    filename = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        headers = {'X-Filename': filename}
        response = requests.post(server_url, headers=headers, data=f)

    if response.status_code == 200:
        print("File uploaded successfully")
    else:
        print(f"Upload failed: {response.text}")


if __name__ == '__main__':
    # Replace with your VM's IP and port
    server_url = 'http://192.168.1.231:8000'
    file_path = 'C:/Users/Roman.Chak/Documents/Github/py_electrical/py_electrical/HeatSink/all.zip'
    upload_file(file_path, server_url)

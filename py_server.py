import os
import socket
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

UPLOAD_DIR = "/home/roman/Documents/uploads"  # Changed to /tmp for better permissions
HOST_IP = "192.168.252.xx"  # Host PC's IP for restricted firewall rule


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Could not determine IP: {e}"


def kill_process_on_port(port):
    try:
        result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        for line in lines[1:]:
            pid = line.split()[1]
            subprocess.run(['kill', '-9', pid])
            print(f"Killed process {pid} on port {port}")
    except subprocess.CalledProcessError:
        print(f"No process found on port {port}")
    except Exception as e:
        print(f"Error killing process on port {port}: {e}")


def open_port(port, restrict_ip=None):
    try:
        # Check if ufw is installed
        subprocess.run(['which', 'ufw'], check=True, capture_output=True)

        # Check if port is already allowed
        result = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
        if f"{port}" in result.stdout and "ALLOW" in result.stdout:
            print(f"Port {port} is already open")
            return True

        # Construct ufw command
        if restrict_ip:
            ufw_cmd = ['sudo', '-n', 'ufw', 'allow', 'from', restrict_ip, 'to', 'any', 'port', str(port)]
        else:
            ufw_cmd = ['sudo', '-n', 'ufw', 'allow', str(port)]

        # Try to open port
        result = subprocess.run(ufw_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully opened port {port}")
            return True
        else:
            print(f"Failed to open port {port}: {result.stderr}")
            return False
    except subprocess.CalledProcessError:
        print("Error: 'ufw' is not installed or not found. Install with 'sudo apt install ufw'.")
        return False
    except Exception as e:
        print(f"Error opening port {port}: {e}")
        return False


def check_directory_permissions(directory):
    try:
        os.makedirs(directory, exist_ok=True)
        test_file = os.path.join(directory, ".test_write")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        return True
    except PermissionError:
        print(f"Permission denied: Cannot write to {directory}")
        return False
    except Exception as e:
        print(f"Error checking permissions for {directory}: {e}")
        return False


class FileUploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        filename = self.headers.get('X-Filename', 'uploaded_file')
        file_path = os.path.join(UPLOAD_DIR, filename)

        try:
            with open(file_path, 'wb') as f:
                f.write(self.rfile.read(content_length))
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'File uploaded successfully')
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Upload failed: {str(e)}'.encode())


def run(server_class=HTTPServer, handler_class=FileUploadHandler, port=8000):
    # Check directory permissions
    if not check_directory_permissions(UPLOAD_DIR):
        print(f"Cannot proceed: No write permissions for {UPLOAD_DIR}")
        return

    # Open port 8000, restricted to host IP for security
    """if not open_port(port, restrict_ip=HOST_IP):
        print(f"Cannot proceed: Failed to open port {port}")
        return"""

    # Kill any process on port 8000
    kill_process_on_port(port)

    # Get and display IP address
    ip = get_ip_address()
    print(f"Server IP address: {ip}")

    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run()

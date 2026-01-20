import os
import hashlib
import hmac
import socket
import threading
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecureFileTransfer:
    def __init__(self, password):
        self.password = password.encode()
        self.salt = os.urandom(16)
        self.key = self._derive_key()
        self.cipher = Fernet(self.key)
    
    def _derive_key(self):
        # Derive encryption key from password using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = self.salt,
            iterations = 10000
        )
        key = base64.urlsafe_b64decode(kdf.derive(self.password))
        return key
    
    def encrypt_file(self, file_path):
        #Encrypt file contents
        with open(file_path, 'rb') as f:
            data = f.read()
        
        encrypted_data = self.cipher.encrypt(data)

        #Calculate file hash for integrity
        file_hash = hashlib.sha256(data).hexdigest()

        return {
            'encrypted_data': encrypted_data,
            'salt': self.salt,
            'hash': file_hash,
            'filename': os.path.basename(file_path)
        }
    
    def decrypt_file(self, encrypted_package, output_path):
        #Decrypt file and verify integrity

        try:
            #Decrypt data
            decrypted_data = self.cipher.decrypt(encrypted_package['encrypted_data'])

            #Verify integrity
            calculated_hash = hashlib.sha256(decrypted_data).hexdigest()
            if calculated_hash != encrypted_package['hash']:
                raise ValueError("File integrity check failed!")
            
            #Write decrypted file
            with open(output_path, 'wb') as f:
                f.write(decrypted_data)

            return True
        except Exception as e:
            print("Decryption failed: {e}")
            return False

class SecureServer:
    def __init__(self, host='localhost', port=8888, password='default_password'):
        self.host = host
        self.port = port
        self.password = password
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start_server(self):
        #Start secure file transfer
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Secure server listening on {self.host}:{self.port}")

        while True:
            client_socket, address = self.socket.accept()
            print(f"Connection from {address}")
            client_thread = threading.thread(
                target = self.handle_client,
                args = (client_socket)
            )
            client_thread.start()
    
    def handle_client(self, client_socket):
        #Handle client file transfer

        try:
            #Receive encrypted file package

            data = b""
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                data += chunk
            
            #Parse received data
            package = json.loads(data.decode())
            package['encrypted_data'] = base64.b64decode(package['encrypted_data'])
            package['salt'] = base64.b64decode(package['salt'])

            #Initializing decryption with received salt
            transfer = SecureFileTransfer(self.password)
            transfer.salt = package['salt']
            transfer.key = transfer._derive_key()
            transfer.cipher = Fernet(transfer.key)

            #Decrypting and saving the file
            output_path = f"received_{package['filename']}"
            if transfer.decrypt_file(package, output_path):
                response = "File received and decrypted successfully!"
                print(f"Received: {package['filename']}")
            else:
                response = "Failed to decrypt file!"
                print("Decryption failed")

            client_socket.send(response.encode())
        
        except Exception as e:
            print(f"Error handling client: {e}")
            client_socket.send(f"Error: {e}".encode())
        finally:
            client_socket.close()

class SecureClient:
    def __init__(self, server_host = 'localhost', server_port = 8888, password = 'default_password'):
        self.server_host = server_host
        self.server_port = server_port
        self.password = password

    def send_file(self, file_path):
        #Sending encrypted file to server
        try:
            #Encrypt file
            transfer = SecureFileTransfer(self.password)
            encrypted_package = transfer.encrypt_file(file_path)

            #Prepare for transmission
            package = {
                'encrypted_data': base64.b64encode(encrypted_package['encrypted_data']).decode(),
                'salt': base64.b64encode(encrypted_package['salt']).decode(),
                'hash': encrypted_package['hash'],
                'filename': encrypted_package['filename']
            }
            
            # Connect and send
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.server_host, self.server_port))
            
            client_socket.send(json.dumps(package).encode())
            client_socket.shutdown(socket.SHUT_WR)
            
            # Receive response
            response = client_socket.recv(1024).decode()
            print(f"Server response: {response}")
            
            client_socket.close()
            return True
            
        except Exception as e:
            print(f"Failed to send file: {e}")
            return False
import tkinter as tk
from tkinter import filedialog
import socket
import os
import zipfile
import threading

class Server:
    def __init__(self, master):
        self.master = master
        self.master.title("KACKLE File Transfer Server")

        # create an entry to input the IP address
        self.ip_address_entry = tk.Entry(self.master)
        self.ip_address_entry.pack()

        # create an entry to input the port number
        self.port_entry = tk.Entry(self.master)
        self.port_entry.pack()

        # create a button to select a file
        self.select_file_btn = tk.Button(self.master, text="Select File", command=self.select_file)
        self.select_file_btn.pack()

        # create a label to display the selected file
        self.selected_file_label = tk.Label(self.master, text="No file selected")
        self.selected_file_label.pack()

        # create a button to start the server
        self.start_server_btn = tk.Button(self.master, text="Start Listening", command=self.start_server, state='disabled')
        self.start_server_btn.pack()

        # create a button to close the server
        self.close_server_btn = tk.Button(self.master, text="Close Server", command=self.close_server, state='disabled')
        self.close_server_btn.pack()

    def select_file(self):
        # open a file dialog to select a file
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("all files", "*.*"), ("jpeg files", "*.jpg")))
        self.selected_file_label.config(text=self.filename)
        self.start_server_btn.config(state='normal')

    def start_server(self):
        # start the server socket on a separate thread
        t = threading.Thread(target=self.run_server)
        t.start()

    def run_server(self):
        # start the server socket
        self.server_socket = socket.socket()
        ip_address = self.ip_address_entry.get()
        port = int(self.port_entry.get())
        self.server_socket.bind((ip_address, port))
        self.server_socket.listen(1)
        print("Server started, waiting for a connection...")

        # disable select and start buttons and enable close button
        self.select_file_btn.config(state='disabled')
        self.start_server_btn.config(state='disabled')
        self.close_server_btn.config(state='normal')

        # accept a client connection
        self.client_socket, self.client_address = self.server_socket.accept()
        print("Accepted connection from", self.client_address)

        # compress the file
        filename_base = os.path.basename(self.filename)
        filename_zip = os.path.splitext(filename_base)[0] + '.zip'
        with zipfile.ZipFile(filename_zip, 'w', zipfile.ZIP_DEFLATED) as zip:
            zip.write(self.filename, filename_base)
        print("File compressed successfully")

        # send the compressed file to the client
        with open(filename_zip, 'rb') as file:
            data = file.read()
            self.client_socket.sendall(data)
        print("Compressed file sent successfully")

        # close the client socket and server socket
        self.client_socket.close()
        self.server_socket.close()
        print("Server closed")

        # enable select and start buttons and disable close button
        self.select_file_btn.config(state='normal')
        self.start_server_btn.config(state='normal')
        self.close_server_btn.config(state='disabled')

    def close_server(self):
        # close the client socket and server socket
        self.client_socket.close()
        self.server_socket.close()
        print("Server closed")

        # enable select and start buttons and disable close button
        self.select_file_btn.config(state='normal')
        self.start_server_btn.config(state='normal')
        self.close_server_btn.config(state='disabled')

root = tk.Tk()
app = Server(root)
root.mainloop()

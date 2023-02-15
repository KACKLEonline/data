import tkinter as tk
from tkinter import filedialog
import socket
import os
import threading
import zipfile

class Client:
    def __init__(self, master):
        self.master = master
        self.master.title("KACKLE File Transfer Client")

        # create an entry to input the server IP address
        self.server_ip_entry = tk.Entry(self.master)
        self.server_ip_entry.pack()

        # create an entry to input the port number
        self.port_entry = tk.Entry(self.master)
        self.port_entry.pack()

        # create a button to select the folder to save the received file
        self.select_folder_btn = tk.Button(self.master, text="Select Folder", command=self.select_folder)
        self.select_folder_btn.pack()

        # create a label to display the selected folder
        self.selected_folder_label = tk.Label(self.master, text="No folder selected")
        self.selected_folder_label.pack()

        # create a button to connect to the server
        self.connect_btn = tk.Button(self.master, text="Connect to Server", command=self.connect_to_server, state='disabled')
        self.connect_btn.pack()

        # create a button to receive the file
        self.receive_file_btn = tk.Button(self.master, text="Receive File", command=self.receive_file, state='disabled')
        self.receive_file_btn.pack()

        # create a button to close the client
        self.close_client_btn = tk.Button(self.master, text="Close Client", command=self.close_client, state='disabled')
        self.close_client_btn.pack()

    def select_folder(self):
        # open a file dialog to select a folder
        self.folder_path = filedialog.askdirectory(initialdir="/", title="Select folder")
        self.selected_folder_label.config(text=self.folder_path)
        self.connect_btn.config(state='normal')

    def connect_to_server(self):
        # connect to the server
        self.client_socket = socket.socket()
        ip_address = self.server_ip_entry.get()
        port = int(self.port_entry.get())
        self.client_socket.connect((ip_address, port))
        print("Connected to the server")
        self.receive_file_btn.config(state='normal')

    def receive_file(self):
        # create a new thread to receive the file in the background
        t = threading.Thread(target=self.receive_file_thread)
        t.start()

    def receive_file_thread(self):
        # receive the compressed file from the server
        filename_zip = os.path.join(self.folder_path, "received_file.zip")
        with open(filename_zip, 'wb') as file:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print("Compressed file received successfully")

        # extract the file from the zip archive
        with zipfile.ZipFile(filename_zip, 'r') as zip:
            zip.extractall(self.folder_path)
        print("File extracted from zip archive")

        # delete the zip archive
        os.remove(filename_zip)
        print("Zip archive deleted")

        # close the client socket
        self.client_socket.close()

        # update the GUI to reflect that the file has been received
        self.master.after(0, self.receive_file_done)

    def receive_file_done(self):
        # disable connect and receive buttons and enable close button
        self.connect_btn.config(state='disabled')
        self.receive_file_btn.config(state='disabled')
        self.close_client_btn.config(state='normal')

        # print a message to the console to indicate that the client has closed
        print("Client closed")

    def close_client(self):
        # print a message to the console to indicate that the client is closing
        print("Closing client...")

        # close the client socket
        self.client_socket.close()

        # print a message to the console to indicate that the client has closed
        print("Client closed")

root = tk.Tk()
app = Client(root)
root.mainloop()


import tkinter as tk
from tkinter import ttk, messagebox
import serial
import time

USERNAME = "admin"
PASSWORD = "1234"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Maambo Industries - Login")
        self.root.geometry("500x350")
        self.root.configure(bg="#2C3E50")
        self.login_frame = tk.Frame(self.root, bg="#2C3E50")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.login_screen()

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        tk.Label(self.login_frame, text="MAAMBO INDUSTRIES", font=("Arial", 22, "bold"), fg="lightblue", bg="#2C3E50").pack(pady=10)
        tk.Label(self.login_frame, text="Enter your credentials", font=("Arial", 12), fg="white", bg="#2C3E50").pack(pady=5)

        entry_frame = tk.Frame(self.login_frame, bg="#2C3E50")
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Username:", fg="white", bg="#2C3E50", anchor='w', width=12).grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(entry_frame, bg="#34495E", fg="white", insertbackground='white', width=30)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(entry_frame, text="Password:", fg="white", bg="#2C3E50", anchor='w', width=12).grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(entry_frame, show="*", bg="#34495E", fg="white", insertbackground='white', width=30)
        self.password_entry.grid(row=1, column=1, pady=5)

        tk.Button(self.login_frame, text="Login", bg="#2980B9", fg="white", width=25, height=2, command=self.check_login).pack(pady=10)

    def check_login(self):
        if self.username_entry.get() == USERNAME and self.password_entry.get() == PASSWORD:
            self.launch_loading_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def launch_loading_window(self):
        loading_win = tk.Toplevel(self.root)
        loading_win.geometry("400x150")
        loading_win.configure(bg="#2C3E50")
        loading_win.title("Loading...")

        tk.Label(loading_win, text="Loading Systems...", font=("Arial", 14), fg="lightblue", bg="#2C3E50").pack(pady=20)
        progress = ttk.Progressbar(loading_win, orient="horizontal", length=300, mode="determinate")
        progress.pack(pady=10)

        def fill():
            value = progress["value"]
            if value < 100:
                progress["value"] = value + 5
                self.root.after(50, fill)
            else:
                loading_win.destroy()
                self.blank_screen()
        fill()

    def blank_screen(self):
        self.clear_root()
        self.root.geometry("1000x700")
        self.root.configure(bg="#2C3E50")
        RelayControlApp(self.root)

class RelayControlApp:
    def __init__(self, root):
        self.root = root

        self.status_var = tk.StringVar()
        self.status_var.set("Connecting...")

        self.init_serial_ports()
        self.create_widgets()

    def init_serial_ports(self):
        try:
            self.ser_generator = serial.Serial('COM6', 9600, timeout=2, write_timeout=2)
            self.ser_output = serial.Serial('COM8', 9600, timeout=2, write_timeout=2)
            time.sleep(2)
            self.status_var.set("Connected to both Arduino boards.")
        except Exception as e:
            self.status_var.set("Connection error.")
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")

    def create_widgets(self):
        section_font = ("Arial", 14, "bold")
        label_font = ("Arial", 10)

        # Generator Control Section
        gen_frame = tk.LabelFrame(self.root, text="Generator Control", fg="lightblue", bg="#2C3E50", font=section_font)
        gen_frame.pack(padx=20, pady=15, fill="x")

        tk.Button(gen_frame, text="Turn ON Battery 1", command=lambda: self.send_command(self.ser_generator, "4_LOW"), width=25, bg="#34495E", fg="white").pack(pady=5)
        tk.Button(gen_frame, text="Turn OFF Battery 1", command=lambda: self.send_command(self.ser_generator, "4_HIGH"), width=25, bg="#34495E", fg="white").pack(pady=5)
        tk.Button(gen_frame, text="Turn ON Battery 2", command=lambda: self.send_command(self.ser_generator, "5_LOW"), width=25, bg="#34495E", fg="white").pack(pady=5)
        tk.Button(gen_frame, text="Turn OFF Battery 2", command=lambda: self.send_command(self.ser_generator, "5_HIGH"), width=25, bg="#34495E", fg="white").pack(pady=5)
        tk.Button(gen_frame, text="Emergency OFF (Generator)", command=lambda: self.emergency_off(self.ser_generator), bg="red", fg="white", width=30).pack(pady=10)

        # Output Control Section
        out_frame = tk.LabelFrame(self.root, text="Output Control", fg="lightblue", bg="#2C3E50", font=section_font)
        out_frame.pack(padx=20, pady=15, fill="x")

        for i in range(1, 5):
            tk.Button(out_frame, text=f"Turn ON Section {i}", command=lambda i=i: self.send_command(self.ser_output, f"{i+1}_LOW"), width=25, bg="#34495E", fg="white").pack(pady=5)
            tk.Button(out_frame, text=f"Turn OFF Section {i}", command=lambda i=i: self.send_command(self.ser_output, f"{i+1}_HIGH"), width=25, bg="#34495E", fg="white").pack(pady=5)

        tk.Button(out_frame, text="Emergency OFF (Output)", command=lambda: self.emergency_off(self.ser_output), bg="red", fg="white", width=30).pack(pady=10)
        tk.Button(out_frame, text="Power ALL Sections", command=self.power_all_sections, bg="#2980B9", fg="white", width=30).pack(pady=10)

        # Status Bar
        tk.Label(self.root, textvariable=self.status_var, bg="#2C3E50", fg="white", font=label_font).pack(pady=10)

    def send_command(self, serial_port, command):
        try:
            serial_port.write(f"{command}\n".encode())
            serial_port.flush()
            time.sleep(0.1)
        except Exception as e:
            messagebox.showerror("Communication Error", f"Failed to send command: {e}")

    def emergency_off(self, serial_port):
        for pin in range(2, 13):
            self.send_command(serial_port, f"{pin}_HIGH")
        self.status_var.set("All relays OFF (Emergency)")

    def power_all_sections(self):
        for pin in range(2, 9):
            self.send_command(self.ser_output, f"{pin}_LOW")
        self.status_var.set("All output sections ON")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
 

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.colorchooser import askcolor
import json
import os
from datetime import datetime
from DEVICE import Device
from LIGHT import Light
from THERMOSTAT import Thermostat
from CAMERA import SecurityCamera
from FAN import Fan

class DeviceManager:
    def __init__(self):
        self.devices = {
            'lights': {},
            'thermostat': {},
            'security_camera': {},
            'fan': {}
        }
        self.device_classes = {
            'lights': Light,
            'thermostat': Thermostat,
            'security_camera': SecurityCamera,
            'fan': Fan,
        }
        self.initialize_storage()
        self.load_devices()

    def initialize_storage(self):
        os.makedirs('data', exist_ok=True)
        for device_type in self.devices.keys():
            filepath = os.path.join('data', f'{device_type}.json')
            if not os.path.exists(filepath):
                self.save_devices(device_type)

    def remove_device(self, device_type, name):
        if name in self.devices[device_type]:
            del self.devices[device_type][name]
            self.save_devices(device_type)
            return True
        return False

    def get_device(self, device_type, name, username):
        device = self.devices[device_type].get(name)
        if device and device.owner == username:
            return device
        return None

    def add_device(self, device_type, name, location, owner):
        device_class = self.device_classes[device_type]
        self.devices[device_type][name] = device_class(name, location, owner)
        self.save_devices(device_type)

    def get_user_devices(self, device_type, username):
        return {name: device for name, device in self.devices[device_type].items() 
            if device.owner == username}

    def save_devices(self, device_type):
        filepath = os.path.join('data', f'{device_type}.json')
        try:
            data = {name: device.to_dict() for name, device in self.devices[device_type].items()}
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save {device_type}: {str(e)}")

    def load_devices(self):
        for device_type, device_class in self.device_classes.items  ():
            filepath = os.path.join('data', f'{device_type}.json')
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    self.devices[device_type] = {
                    name: device_class.from_dict({**device_data, 'name': name})
                    for name, device_data in data.items()
                    }
            except FileNotFoundError:
                self.devices[device_type] = {}
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load {device_type}: {str(e)}")

class UI:
    def __init__(self, root, device_manager):
        self.root = root
        self.device_manager = device_manager
        self.current_user = None
        self.frames = {}
        # Updated color scheme to match second file
        self.colors = {
            'primary': "#464F5D",      # Slate Blue-Gray for buttons
            'success': "#464F5D",      # Same color for consistency
            'warning': "#464F5D",      # Same color for consistency
            'error': "#464F5D",        # Same color for consistency
            'background': "#374151",   # Background color
            'surface': "#1F2937",      # Surface color
            'text': "#FFFFFF",         # White text
            'button_text': "#FFFFFF"   # White button text
        }
        self.setup_ui()
        self.users = self.load_users()

    def setup_ui(self):
        self.root.title("Smart Home Automation")
        self.root.geometry("800x600")
        self.root.configure(bg=self.colors['background'])

    def load_users(self):
        try:
            with open('data/users.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open('data/users.json', 'w') as f:
            json.dump(self.users, f, indent=4)

    def create_styled_button(self, parent, text, command, style='primary'):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.colors[style],        # Use color from the style
            fg='#000000',  # Use defined text color
            relief='raised',
            padx=15,
            pady=8,
            borderwidth=2,
            font=('Helvetica', 10, 'bold'),
            activebackground=self.colors[style],  # Match active background to style
            activeforeground=self.colors['button_text']  # Match active text color
        )

    def clear_frame(self):
        for frame in self.frames.values():
            frame.destroy()
        self.frames.clear()

    def create_frame(self, frame_name):
        self.clear_frame()
        frame = tk.Frame(self.root, bg=self.colors['background'])
        self.frames[frame_name] = frame
        return frame

    def show_auth_screen(self):
        frame = self.create_frame('auth')
        frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(
            frame,
            text="Smart Home Authentication",
            font=('Helvetica', 24, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(pady=20)

        self.create_styled_button(frame, "Login", self.show_login_screen).pack(pady=10)
        self.create_styled_button(frame, "Register", self.show_register_screen).pack(pady=10)

    def show_register_screen(self):
        frame = self.create_frame('register')
        frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(frame, text="Register New User", font=('Helvetica', 24, 'bold'),
                bg=self.colors['background'], fg=self.colors['text']).pack(pady=20)

        username_var = tk.StringVar()
        password_var = tk.StringVar()

        tk.Label(frame, text="Username:", bg=self.colors['background'], fg=self.colors['text']).pack()
        ttk.Entry(frame, textvariable=username_var).pack(pady=5)

        tk.Label(frame, text="Password:", bg=self.colors['background'], fg=self.colors['text']).pack()
        ttk.Entry(frame, textvariable=password_var, show="*").pack(pady=5)

        def register():
            username = username_var.get().strip()
            password = password_var.get()

            if not username or not password:
                messagebox.showerror("Error", "All fields are required")
                return

            if username in self.users:
                messagebox.showerror("Error", "Username already exists")
                return

            self.users[username] = {'password': password}
            self.save_users()
            messagebox.showinfo("Success", "Registration successful")
            self.show_login_screen()

        self.create_styled_button(frame, "Register", register, 'success').pack(pady=20)
        self.create_styled_button(frame, "Back", self.show_auth_screen, 'warning').pack()

    def show_login_screen(self):
        frame = self.create_frame('login')
        frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(frame, text="Login", font=('Helvetica', 24, 'bold'),
                bg=self.colors['background'], fg=self.colors['text']).pack(pady=20)

        username_var = tk.StringVar()
        password_var = tk.StringVar()

        tk.Label(frame, text="Username:", bg=self.colors['background'], fg=self.colors['text']).pack()
        ttk.Entry(frame, textvariable=username_var).pack(pady=5)

        tk.Label(frame, text="Password:", bg=self.colors['background'], fg=self.colors['text']).pack()
        ttk.Entry(frame, textvariable=password_var, show="*").pack(pady=5)

        def login():
            username = username_var.get()
            password = password_var.get()

            if username in self.users and self.users[username]['password'] == password:
                self.current_user = username
                self.show_main_screen()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        self.create_styled_button(frame, "Login", login).pack(pady=20)
        self.create_styled_button(frame, "Back", self.show_auth_screen, 'warning').pack()

    def show_main_screen(self):
        frame = self.create_frame('main')
        frame.pack(expand=True)

        tk.Label(frame, text="Smart Home Control Panel", font=('Helvetica', 24, 'bold'),
                bg=self.colors['background'], fg=self.colors['text']).pack(pady=20)

        device_frame = tk.Frame(frame, bg=self.colors['background'])
        device_frame.pack(pady=20)

        devices = ["Lights", "Thermostat", "Security Camera", "Fan"]
        for device in devices:
            device_type = device.lower().replace(' ', '_')
            self.create_styled_button(
                device_frame,
                f"Manage {device}",
                lambda d=device_type: self.show_device_management(d)
            ).pack(pady=10)

        self.create_styled_button(frame, "Generate Status Report",
            self.generate_report, 'warning').pack(pady=10)
        self.create_styled_button(frame, "Logout",
            self.show_auth_screen, 'error').pack(pady=10)

    def show_device_management(self, device_type):
        frame = self.create_frame('device_management')
        frame.pack(expand=True)

        display_name = device_type.replace('_', ' ').title()
        tk.Label(frame, text=f"{display_name} Management", font=('Helvetica', 24, 'bold'),
                bg=self.colors['background'], fg=self.colors['text']).pack(pady=20)

        self.create_styled_button(frame, "Add Device",
            lambda: self.add_device_window(device_type)).pack(pady=10)
        self.create_styled_button(frame, "Control Device",
            lambda: self.control_device_window(device_type)).pack(pady=10)
        self.create_styled_button(frame, "Remove Device",
            lambda: self.remove_device_window(device_type)).pack(pady=10)
        self.create_styled_button(frame, "Back",
            self.show_main_screen, 'warning').pack(pady=10)

    def add_device_window(self, device_type):
        window = tk.Toplevel(self.root)
        window.title(f"Add {device_type.title()}")
        window.geometry("400x300") 
        window.configure(bg=self.colors['background'])

        frame = tk.Frame(window, bg=self.colors['background'])
        frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(frame, text=f"Add New {device_type.title()}", font=('Helvetica', 18, 'bold'),
                bg=self.colors['background'], fg=self.colors['text']).pack(pady=20)

        name_var = tk.StringVar()
        location_var = tk.StringVar()

        tk.Label(frame, text="Device Name:", bg=self.colors['background'], fg=self.colors['text']).pack()
        ttk.Entry(frame, textvariable=name_var).pack(pady=5)

        tk.Label(frame, text="Location:", bg=self.colors['background'], fg=self.colors['text']).pack()
        ttk.Entry(frame, textvariable=location_var).pack(pady=5)

        def add_device():
            name = name_var.get().strip()
            location = location_var.get().strip()

            if not name or not location:
                messagebox.showerror("Error", "All fields are required")
                return  # Return here after error

            try:
                self.device_manager.add_device(device_type, name, location, self.current_user)
                self.log_status(f"Added new {device_type}: {name}")
                messagebox.showinfo("Success", "Device added successfully")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        self.create_styled_button(frame, "Add Device", add_device, 'success').pack(pady=20)
        self.create_styled_button(frame, "Cancel", window.destroy, 'warning').pack()
        

    def control_device_window(self, device_type):
        devices = self.device_manager.get_user_devices(device_type, self.current_user)
        if not devices:
            messagebox.showinfo("Info", f"No {device_type} found")
            return

        window = tk.Toplevel(self.root)
        window.title(f"Control {device_type.title()}")
        window.geometry("500x400")
        window.configure(bg=self.colors['background'])

        frame = tk.Frame(window, bg=self.colors['background'])
        frame.pack(padx=20, pady=20, fill='both', expand=True)

        device_var = tk.StringVar(value=list(devices.keys())[0])
        tk.Label(frame, text="Select Device:", bg=self.colors['background'], fg=self.colors['text']).pack()
        device_menu = ttk.Combobox(frame, textvariable=device_var, values=list(devices.keys()))
        device_menu.pack(pady=10)

        control_frame = tk.Frame(frame, bg=self.colors['background'])
        control_frame.pack(pady=20)

        def update_controls(*args):
            for widget in control_frame.winfo_children():
                widget.destroy()

            device = devices[device_var.get()]
            power_var = tk.BooleanVar(value=device.status == 'on')

            def on_power_change():
                device.toggle_power(power_var.get())
                self.device_manager.save_devices(device_type)
                update_controls()

            tk.Checkbutton(
                control_frame,
                text="Power",
                variable=power_var,
                command=on_power_change,
                bg=self.colors['background']
            ).pack(pady=10)

            if device.status == 'on':
                if isinstance(device, Light):
                    brightness = tk.Scale(
                        control_frame,
                        from_=0, to=100,
                        orient='horizontal',
                        label="Brightness",
                        command=lambda v: (
                            device.set_brightness(float(v)),
                            self.device_manager.save_devices(device_type)
                        )
                    )
                    brightness.set(device.brightness)
                    brightness.pack(pady=10)

                    self.create_styled_button(
                        control_frame,
                        "Change Color",
                        lambda: self.show_color_picker(device_type, device_var.get())
                    ).pack(pady=10)

                elif isinstance(device, Thermostat):
                    temp = tk.Scale(
                        control_frame,
                        from_=60, to=90,
                        orient='horizontal',
                        label="Temperature (°F)",
                        command=lambda v: (
                            device.set_temperature(float(v)),
                            self.device_manager.save_devices(device_type)
                        )
                    )
                    temp.set(device.temperature)
                    temp.pack(pady=10)

                    modes = ['auto', 'heat', 'cool', 'off']
                    mode_var = tk.StringVar(value=device.mode)
                    tk.Label(control_frame, text="Mode:", bg=self.colors['background']).pack()
                    mode_menu = ttk.Combobox(
                        control_frame,
                        textvariable=mode_var,
                        values=modes,
                        state='readonly'
                    )
                    mode_menu.pack(pady=10)
                    mode_var.trace('w', lambda *args: (
                        device.set_mode(mode_var.get()),
                        self.device_manager.save_devices(device_type)
                    ))

                elif isinstance(device, SecurityCamera):
                    recording_var = tk.BooleanVar(value=device.recording)
                    tk.Checkbutton(
                        control_frame,
                        text="Recording",
                        variable=recording_var,
                        command=lambda: (
                            device.toggle_recording(recording_var.get()),
                            self.device_manager.save_devices(device_type)
                        ),
                        bg=self.colors['background']
                    ).pack(pady=10)

                    resolutions = ['720p', '1080p', '4K']
                    res_var = tk.StringVar(value=device.resolution)
                    tk.Label(control_frame, text="Resolution:", bg=self.colors['background']).pack()
                    res_menu = ttk.Combobox(
                        control_frame,
                        textvariable=res_var,
                        values=resolutions,
                        state='readonly'
                    )
                    res_menu.pack(pady=10)
                    res_var.trace('w', lambda *args: (
                        device.set_resolution(res_var.get()),
                        self.device_manager.save_devices(device_type)
                    ))

                elif isinstance(device, Fan):
                    speed = tk.Scale(
                        control_frame,
                        from_=0, to=5,
                        orient='horizontal',
                        label="Speed",
                        command=lambda v: (
                            device.set_speed(float(v)),
                            self.device_manager.save_devices(device_type)
                        )
                    )
                    speed.set(device.speed)
                    speed.pack(pady=10)

        device_var.trace('w', update_controls)
        update_controls()

    def show_color_picker(self, device_type, device_name):
        device = self.device_manager.devices[device_type][device_name]
        
        color_window = tk.Toplevel(self.root)
        color_window.title("Choose Color")
        color_window.geometry("300x400")
        color_window.configure(bg=self.colors['background'])
        
        # Predefined colors
        preset_colors = [
            "#FF0000", "#00FF00", "#0000FF",
            "#FFFF00", "#FF00FF", "#00FFFF",
            "#FFFFFF", "#808080", "#000000"
        ]
        
        def select_color(color):
            try:
                device.set_color(color)
                self.device_manager.save_devices(device_type)
                self.log_status(f"Changed light {device_name} color to: {color}")
                color_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update color: {str(e)}")
        
        preset_frame = tk.Frame(color_window, bg=self.colors['background'])
        preset_frame.pack(pady=10)
        
        for color in preset_colors:
            btn = tk.Button(
                preset_frame,
                bg=color,
                width=2,
                height=1,
                command=lambda c=color: select_color(c)
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        def choose_custom_color():
            try:
                color = askcolor(title="Choose custom color")[1]
                if color:
                    select_color(color)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to choose custom color: {str(e)}")
        
        self.create_styled_button(
            color_window,
            "Choose Custom Color",
            choose_custom_color
        ).pack(pady=10)

    def remove_device_window(self, device_type):
        devices = self.device_manager.get_user_devices(device_type, self.current_user)
        if not devices:
            messagebox.showinfo("Info", f"No {device_type} found")
            return

        window = tk.Toplevel(self.root)
        window.title(f"Remove {device_type}")
        window.geometry("400x300")
        window.configure(bg=self.colors['background'])

        frame = tk.Frame(window, bg=self.colors['background'])
        frame.place(relx=0.5, rely=0.5, anchor='center')

        device_var = tk.StringVar(value=list(devices.keys())[0])
        tk.Label(frame, text="Select Device:", bg=self.colors['background'], fg=self.colors['text']).pack()
        device_menu = ttk.Combobox(frame, textvariable=device_var, values=list(devices.keys()))
        device_menu.pack(pady=10)

        def remove_device():
            device_name = device_var.get()
            if messagebox.askyesno("Confirm", f"Remove {device_name}?"):
                if self.device_manager.remove_device(device_type, device_name):
                    self.log_status(f"Removed {device_type}: {device_name}")
                    messagebox.showinfo("Success", "Device removed")
                    window.destroy()
                else:
                    messagebox.showerror("Error", "Failed to remove device")

        self.create_styled_button(frame, "Remove Device", remove_device, 'error').pack(pady=20)
        self.create_styled_button(frame, "Cancel", window.destroy, 'warning').pack()

    def generate_report(self):
        try:
            window = tk.Toplevel(self.root)
            window.title("Status Report")
            window.geometry("800x600")
            window.configure(bg=self.colors['background'])

            frame = tk.Frame(window, bg=self.colors['background'])
            frame.pack(padx=20, pady=20, fill='both', expand=True)

            text_widget = tk.Text(frame, wrap=tk.WORD, bg=self.colors['surface'], fg=self.colors['text'])
            text_widget.pack(fill='both', expand=True, pady=10)

            report = [
                "=== Smart Home Status Report ===",
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Generated by: {self.current_user}\n"
            ]

            device_types = {
                'lights': 'Lights',
                'thermostat': 'Thermostat',
                'security_camera': 'Security Camera',
                'fan': 'Fan'
            }

            has_devices = False
            for device_type, display_name in device_types.items():
                devices = self.device_manager.get_user_devices(device_type, self.current_user)
                report.append(f"\n=== {display_name} ===")
                
                if not devices:
                    report.append("No devices found")
                    continue
                    
                has_devices = True
                for name, device in devices.items():
                    report.extend([
                        f"\nDevice: {name}",
                        f"Location: {device.location}",
                        f"Status: {device.status}"
                    ])

                    if isinstance(device, Light):
                        report.extend([
                            f"Brightness: {device.brightness}%",
                            f"Color: {device.color}"
                        ])
                    elif isinstance(device, Thermostat):
                        report.extend([
                            f"Temperature: {device.temperature}°F",
                            f"Mode: {device.mode}"
                        ])
                    elif isinstance(device, SecurityCamera):
                        report.extend([
                            f"Recording: {'Yes' if device.recording else 'No'}",
                            f"Resolution: {device.resolution}"
                        ])
                    elif isinstance(device, Fan):
                        report.extend([
                            f"Speed: {device.speed}"
                        ])

            report_text = "\n".join(report)
            text_widget.insert('1.0', report_text)
            text_widget.config(state='disabled')

            def save_report():
                filename = f"smart_home_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                filepath = os.path.join('data', filename)
                with open(filepath, 'w') as f:
                    f.write(report_text)
                messagebox.showinfo("Success", f"Report saved as {filename}")

            button_frame = tk.Frame(frame, bg=self.colors['background'])
            button_frame.pack(pady=10)
                
            self.create_styled_button(button_frame, "Save Report", save_report, 'success').pack(side='left', padx=5)
            self.create_styled_button(button_frame, "Close", window.destroy, 'warning').pack(side='left', padx=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
                                 
    def log_status(self, message):
        try:
            with open(os.path.join('data', 'status_report.txt'), 'a') as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {self.current_user}: {message}\n")
        except Exception as e:
            print(f"Failed to log status: {str(e)}")

class HomeAutomationSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.device_manager = DeviceManager()
        self.ui = UI(self.root, self.device_manager)
        self.ui.show_auth_screen()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = HomeAutomationSystem()
    app.run()
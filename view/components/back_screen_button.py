import customtkinter as ctk

def back_screen_button(master, command):
    return ctk.CTkButton(
        master=master,
        text="←",
        command=command,
        width=40,
        height=40,
        font=ctk.CTkFont(size=20, weight="bold"),
        corner_radius=20,
        fg_color="#E0E0E0",
        hover_color="#C0C0C0",
        text_color="black"
    )

import customtkinter as ctk
from auth import hashing, userdb

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class PasswordEntry(ctk.CTkFrame):

    def __init__(self, master=None, placeholder_text="Password", **kwargs):
        super().__init__(master, fg_color="transparent")

        self.is_password_visible = False

        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder_text, **kwargs)
        self.entry.pack(side="left", fill="x", expand=True)

        self.toggle_btn = ctk.CTkButton(
            self,
            text="👁",
            width=36,
            fg_color="transparent",
            hover_color="#333333",
            command=self.toggle_visibility,
        )
        self.toggle_btn.pack(side="right", padx=(5, 0))

        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, event=None):
        if not self.is_password_visible:
            self.entry.configure(show="*")

    def _on_focus_out(self, event=None):
        if not self.entry.get() or self.is_password_visible:
            self.entry.configure(show="")

    def toggle_visibility(self):
        self.is_password_visible = not self.is_password_visible

        if self.is_password_visible:
            self.entry.configure(show="")
            self.toggle_btn.configure(text="👁")
        else:
            if self.entry.get():
                self.entry.configure(show="*")
            self.toggle_btn.configure(text="🚫")

    def get(self):
        return self.entry.get()

    def reset(self):
        self.is_password_visible = False
        self.toggle_btn.configure(text="👁")
        self.entry.delete(0, "end")
        self.entry.configure(show="")
        if hasattr(self.entry, "_activate_placeholder"):
            self.entry._activate_placeholder()

def reset_entry(entry: ctk.CTkEntry):
    entry.delete(0, "end")
    if hasattr(entry, "_activate_placeholder"):
        entry._activate_placeholder()


class CinemaApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Movieplex++")
        self.geometry("1280x720")
        self.resizable(False, False)
        self.current_user = None
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        self.frames = {}
        for PageClass in (
            LoginPage,
            RegisterPage,
            ChangePasswordPage,
            DashboardPage,
        ):
            frame = PageClass(parent=self.container, controller=self)
            self.frames[PageClass] = frame
        self.show_frame(LoginPage)

    def show_frame(self, page_class):
        for frame in self.frames.values():
            frame.pack_forget()
        frame = self.frames[page_class]
        frame.pack(fill="both", expand=True)
        if hasattr(frame, "on_show"):
            frame.on_show()


class LoginPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(
            self, text="Movieplex++", font=("Arial", 22, "bold"), text_color="red"
        )
        self.label.pack(pady=(20, 15))

        self.user_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.user_entry.pack(pady=8, fill="x", padx=420)

        self.pass_entry = PasswordEntry(self, placeholder_text="Password")
        self.pass_entry.pack(pady=8, fill="x", padx=420)

        self.error_label = ctk.CTkLabel(
            self, text="", text_color="red", font=("Arial", 12)
        )
        self.error_label.pack(pady=4)

        self.login_btn = ctk.CTkButton(
            self, text="Login", command=self.handle_login
        )
        self.login_btn.pack(pady=10, fill="x", padx=420)

        self.signup_btn = ctk.CTkButton(
            self,
            text="Sign up",
            fg_color="transparent",
            border_width=1,
            command=lambda: controller.show_frame(RegisterPage),
        )
        self.signup_btn.pack(pady=10, fill="x", padx=420)

    def on_show(self):
        self.error_label.configure(text="")
        reset_entry(self.user_entry)
        self.pass_entry.reset()
        self.focus_set()

    def handle_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get()

        if not username or not password:
            self.error_label.configure(text="Username or password missing")
            return

        auth_data = userdb.get_user_auth_data(username)
        if not auth_data:
            self.error_label.configure(text="Username or password incorrect")
            return

        stored_hash, is_admin, must_change_pass = auth_data

        if hashing.check_passwd(password, stored_hash):
            self.controller.current_user = username

            if must_change_pass:
                self.controller.show_frame(ChangePasswordPage)
            else:
                self.controller.show_frame(DashboardPage)
        else:
            self.error_label.configure(text="Username or password incorrect")


class RegisterPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(
            self, text="Create new account", font=("Arial", 22, "bold")
        )
        self.label.pack(pady=(20, 15))

        self.user_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.user_entry.pack(pady=8, fill="x", padx=420)

        self.pass_entry = PasswordEntry(self, placeholder_text="Password")
        self.pass_entry.pack(pady=8, fill="x", padx=420)

        self.confirm_entry = PasswordEntry(
            self, placeholder_text="Confirm Password"
        )
        self.confirm_entry.pack(pady=8, fill="x", padx=420)

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=4)

        self.create_btn = ctk.CTkButton(
            self,
            text="Sign up",
            fg_color="green",
            hover_color="#006400",
            command=self.handle_register,
        )
        self.create_btn.pack(pady=10, fill="x", padx=420)

        self.back_btn = ctk.CTkButton(
            self,
            text="Back to login",
            fg_color="transparent",
            border_width=1,
            command=lambda: controller.show_frame(LoginPage),
        )
        self.back_btn.pack(pady=5, fill="x", padx=420)

    def on_show(self):
        self.status_label.configure(text="")
        reset_entry(self.user_entry)
        self.pass_entry.reset()
        self.confirm_entry.reset()
        self.focus_set()

    def handle_register(self):
        username = self.user_entry.get().strip()
        pwd = self.pass_entry.get()
        confirm = self.confirm_entry.get()

        if not username or not pwd:
            self.status_label.configure(
                text="Username or password missing", text_color="red"
            )
            return

        if pwd != confirm:
            self.status_label.configure(
                text="Passwords are not the same", text_color="red"
            )
            return

        pwd_hash = hashing.hash_passwd(pwd)
        if userdb.create_user(username, pwd_hash):
            self.status_label.configure(
                text="Account created, you can login now", text_color="green"
            )
        else:
            self.status_label.configure(
                text="Username already exists", text_color="red"
            )


class ChangePasswordPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(
            self, text="Password change", font=("Arial", 20, "bold")
        )
        self.label.pack(pady=(20, 5))

        self.info_label = ctk.CTkLabel(
            self,
            text="First login for admin \n Password needs to be changed on the first login",
            font=("Arial", 12),
            text_color="orange",
        )
        self.info_label.pack(pady=(0, 15))

        self.new_pass_entry = PasswordEntry(
            self, placeholder_text="New password"
        )
        self.new_pass_entry.pack(pady=8, fill="x", padx=420)

        self.confirm_pass_entry = PasswordEntry(
            self, placeholder_text="Confirm new password"
        )
        self.confirm_pass_entry.pack(pady=8, fill="x", padx=420)

        self.msg_label = ctk.CTkLabel(
            self, text="", text_color="red", font=("Arial", 12)
        )
        self.msg_label.pack(pady=4)

        self.save_btn = ctk.CTkButton(
            self,
            text="Save and enter",
            fg_color="green",
            hover_color="#006400",
            command=self.handle_change_password,
        )
        self.save_btn.pack(pady=10, fill="x", padx=420)

    def on_show(self):
        self.msg_label.configure(text="")
        self.new_pass_entry.reset()
        self.confirm_pass_entry.reset()
        self.focus_set()

    def handle_change_password(self):
        new_pwd = self.new_pass_entry.get()
        confirm = self.confirm_pass_entry.get()

        if not new_pwd:
            self.msg_label.configure(text="Parola nu poate fi goală.")
            return

        if new_pwd != confirm:
            self.msg_label.configure(text="Parolele nu coincid.")
            return

        new_hash = hashing.hash_passwd(new_pwd)
        userdb.update_password(self.controller.current_user, new_hash)
        self.controller.show_frame(DashboardPage)


class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.welcome_label = ctk.CTkLabel(
            self, text="", font=("Arial", 22, "bold")
        )
        self.welcome_label.pack(pady=30)

        self.logout_btn = ctk.CTkButton(
            self,
            text="Log out",
            fg_color="red",
            command=lambda: controller.show_frame(LoginPage),
        )
        self.logout_btn.pack(pady=20)

    def on_show(self):
        self.welcome_label.configure(
            text=f"Welcome,\n{self.controller.current_user}!"
        )


if __name__ == "__main__":
    userdb.init_db()
    userdb.create_default_admin(hashing.hash_passwd("admin123"))

    app = CinemaApp()
    app.mainloop()
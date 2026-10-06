class User:
    def __init__(self,username,password, role):
        self.username = username
        self.password = password
        self.role = role

class Admin(User):
    def __init__(self,username,password:
        super().init__(username, password, role='admin')

class RegularUser(User):
        def __init__(self,username,password:
        super().__init__(username,password,role='user')
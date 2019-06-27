from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals
        # user_model = User
        # print(user_model)
        # watson_search.register(user_model, fields=("first_name", "last_name",))

from users.models import Language

def run():
    f = open("scripts/languages").read().split("\n")
    for l in f:
        Language.objects.get_or_create(language=l)


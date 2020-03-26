from cibling_web.models import PostPhoto


def run():
    id_list = PostPhoto.objects.all().values_list('pk',flat=True)

    for photo_id in id_list:
        try:
            photo_object = PostPhoto.objects.get(id=photo_id)
            print(photo_object.image.path)
        except:
            pass
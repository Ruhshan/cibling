from cibling_web.models import PostPhoto
from PIL import Image
import imghdr

def run():
    id_list = PostPhoto.objects.all().values_list('pk',flat=True)

    for photo_id in id_list:
        try:
            photo_object = PostPhoto.objects.get(id=photo_id)
            if imghdr.what(photo_object.image.path) == "png":
                jpegPath = photo_object.image.path+".jpeg"
                pindex = photo_object.image.path.index("post_pics")
                relativePath = jpegPath[pindex:]

                im = Image.open(photo_object.image.path)
                im.convert("RGB").save(jpegPath,"JPEG")

                photo_object.image = relativePath
                photo_object.save()
        except:
            pass
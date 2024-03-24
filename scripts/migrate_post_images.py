from cibling_web.models import Post, PostPhoto

def run():
    posts = Post.objects.all()

    for p in posts:
        if p.image:
            postPhoto = PostPhoto.objects.create(post=p, image=p.image)
            postPhoto.save()
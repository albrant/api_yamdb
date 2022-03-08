# from django.db.models import Avg
# from django.db.models.signals import post_delete, post_save
# from django.dispatch import receiver

# from .models import Review


# @receiver([post_save, post_delete], sender=Review)
# def get_rating(sender, instance, **kwargs):
#     instance.title.rating = instance.title.reviews.aggregate(
#         (Avg('score'))['score__avg']
#     )
#     instance.title.save()

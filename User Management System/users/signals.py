from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User
from firebase_admin import firestore, storage

# Firestore client
fs_client = firestore.client()

@receiver(post_save, sender=User)
def sync_user_to_firestore(sender, instance, created, **kwargs):

    doc_ref = fs_client.collection("users").document(str(instance.id))
    doc_ref.set({
        'name': instance.name,
        'email': instance.email,
        'role': instance.role,
        'department': instance.department,
        'status': instance.status,
        'phone': instance.phone,
        'profile_picture': str(instance.profile_picture.url) if instance.profile_picture else None,
        'thumbnail': str(instance.thumbnail.url) if instance.thumbnail else None,
        'created_at': str(instance.created_at),
        'updated_at': str(instance.updated_at),
    })

@receiver(post_delete, sender=User)
def delete_user_from_firestore(sender, instance, **kwargs):

    doc_ref = fs_client.collection("users").document(str(instance.id))
    doc_ref.delete()

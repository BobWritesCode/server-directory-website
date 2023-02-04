from django.db.models import Q

from cloudinary import uploader
from datetime import datetime

from .models import Bumps, Images


def daily_jobs():
    clear_bumps()
    delete_rejected_images()


def clear_bumps():
    '''
    Automated task: Finds expired bumps and deletes them.
    '''
    print('clear_bumps(): Starting automated task.')
    # Get bumps that have expired
    query = Q(expiry__lte=datetime.now())
    queryset = Bumps.objects.filter(query)
    print(f'clear_bumps(): Deleting {len(queryset)} bump(s).')
    # Delete expired bumps
    queryset.delete()
    print('clear_bumps(): Completed automated task.')


def delete_rejected_images():
    '''
    Automated task: Finds rejected and expired images and delete
    from the Cloudinary server.
    '''
    print('delete_rejected_images(): Starting automated task.')
    # Get images that have been marked as rejected and expired
    query = Q(expiry__lte=datetime.now()) & Q(status__in=[2, 3])
    queryset = Images.objects.filter(query)
    print(f'delete_rejected_images(): Deleting {len(queryset)} image(s).')
    # Loop through and delete images meeting criteria
    for query in queryset:
        uploader.destroy(query.public_id)
        print(f'delete_rejected_images(): Deleted: {query.public_id}')
    # Delete expired images
    queryset.delete()
    print('delete_rejected_images(): Completed automated task.')

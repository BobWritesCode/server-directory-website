from django.db.models import Q

from datetime import datetime

from .models import Bumps


def clear_bumps():
    '''
    Automated task: Finds expired bumps and deletes them.
    '''
    print('clear_bumps(): Starting automated task.')
    # Get bumps that have expired
    query = Q(expiry__lte = datetime.now())
    queryset = Bumps.objects.filter(query)
    print(f'clear_bumps(): Deleting {len(queryset)} bump(s).')
    # Delete expired bumps
    queryset.delete()
    print('clear_bumps(): Completed automated task.')
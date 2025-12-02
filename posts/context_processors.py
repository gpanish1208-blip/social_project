from .models import Report

def notification_count(request):
    if request.user.is_authenticated:
        count = Report.objects.filter(reported_by=request.user, reply__isnull=False, is_read=False).count()
        return {'notification_count': count}
    return {}
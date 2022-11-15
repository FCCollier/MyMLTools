from django.http import HttpResponse


# Create your views here.

def star_info(request, star_id):
    return HttpResponse("将为您打开 %s 的基本信息。" % star_id)

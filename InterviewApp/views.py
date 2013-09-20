from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

def home(request):
    # redirect to default application
    return HttpResponseRedirect(reverse('SampleISP:index'))

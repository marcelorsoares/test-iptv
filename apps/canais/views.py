from django.http import HttpResponse
from django.shortcuts import render
from .models import Canal


def generate_m3u(request):
    f = open("resultado/lista.m3u", "a")
    f.write("#EXTM3U\n")
    for canal in Canal.objects.filter(status=200).order_by('name'):
        f.write('#EXTINF:{}, tvg-id="{} - {}" tvg-name="{} - {}" tvg-logo="{}" group-title="{}",{}\n{}\n'.format(canal.id, canal.id, canal.name,
                                                                                                                   canal.name,
                                                                                                            canal.id,
                                                                                                                   canal.logo,
                                                                                                                   canal.group_title,
                                                                                                                   canal.name,
                                                                                                                   canal.uri))

    fsock = open("resultado/lista.m3u", "rb")

    return HttpResponse(fsock, content_type='text')


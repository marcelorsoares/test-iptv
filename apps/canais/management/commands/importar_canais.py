from django.core.management.base import BaseCommand
from django.conf import settings
import m3u8
import re
import requests
from canais.models import Canal
from django.db.utils import DataError


class Command(BaseCommand):
    help = 'Importar canais a partir de arquivo m3u'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)
        parser.add_argument('test_stream', type=bool)

    def handle(self, *args, **options):

        m3u8_obj = m3u8.load(settings.BASE_DIR + '/importar/{}'.format(options['filename']))
        x = 1
        for channel in m3u8_obj.segments:
            name = channel.title.split(',')[-1]
            name = name[:255]
            try:
                group_title = re.findall(r'group-title=\"(.*)\" ', channel.title)[0]
                group_title = group_title[:255]
            except IndexError as e:
                group_title = ''
            try:
                logo = re.findall(r'tvg-logo=\"(.*)\" ', channel.title)[0]
                logo = logo[:255]
            except IndexError as e:
                logo = ''
                print('sem logo e:', e)

            uri = channel.uri
            uri = uri[:255]

            print('* {}'.format(x))

            try:
                canal = Canal.objects.get(uri=uri)

                if options['test_stream']:
                    if canal.status == 200:
                        response = requests.get(uri, stream=True)
                        size = 0
                        status = 0
                        for chunk in response.iter_content(256):
                            size += len(chunk)
                            if size > 512:
                                print('size: ', size)
                                status = 200
                                break
                        if status == 0:
                            status = response.status_code
                        canal.status = status
                        canal.save()
                        print('ID: {} - status: {}'.format(canal.id, status))

                print('ID: {}'.format(canal.id))
            except Canal.DoesNotExist:
                try:
                    print('testing: {} ({})'.format(uri, name))
                    response = requests.get(uri, stream=True, timeout=60)
                    headers = requests.head(uri, stream=True, timeout=60).headers
                    content_type = headers.get('content-type')
                    print('Content-type: ', content_type)
                    if content_type == 'application/vnd.apple.mpegurl':
                        status = 200
                    elif content_type == 'application/vnd.apple.mpegURL':
                        status = 200
                    elif content_type == 'video/mp4':
                        status = 200
                    elif content_type == 'application/x-mpegURL':
                        status = 200
                    elif content_type == 'application/vnd.apple.mpegurl, application/vnd.apple.mpegurl':
                        status = 200
                    elif content_type == 'video/mp2t':
                        status = 200
                    elif content_type == 'audio/aacp': # RADIO
                        status = 1
                    elif content_type == 'audio/mpeg': # RADIO
                        status = 1
                    elif content_type == 'audio/x-mpegurl': # RADIO
                        status = 1
                    elif content_type == 'text/html; charset=UTF-8':
                        status = 404
                    elif content_type == 'text/html; charset=utf-8':
                        status = 404
                    elif content_type == 'text/html;charset=UTF-8':
                        status = 404
                    elif content_type == 'image/png':
                        status = 404
                    elif content_type == 'image/jpeg':
                        status = 404
                    elif content_type == 'application/xml':
                        status = 404
                    elif content_type == 'text/plain':
                        status = 404
                    elif content_type == 'text/html':
                        status = 404
                    elif content_type == 'application/octet-stream':
                        status = 2
                    elif content_type is None:
                        status = 0
                    else:
                        status = 404
                        exit(0)

                    if status == 200:
                        size = 0
                        status = 0
                        for chunk in response.iter_content(256):
                            size += len(chunk)
                            if size > 4096:
                                print('size: ',size)
                                status = 200
                                break
                        if status == 0:
                            status = response.status_code
                        canal = Canal(name=name, logo=logo, uri=uri, group_title=group_title, status=status)
                        canal.save()

                        print('#EXTINF:{}, tvg-id="{}" tvg-name="{}" tvg-logo="{}" group-title="{}",{}\n{}'.format(canal.id, name,
                                                                                                                   name,
                                                                                                                   logo,
                                                                                                                   group_title,
                                                                                                                   name,
                                                                                                                   uri))
                    else:
                        canal = Canal(name=name, logo=logo, uri=uri, group_title=group_title, status=status)
                        canal.save()
                        print('status: ', status)
                except requests.exceptions.RequestException as e:
                    print(e)
                    canal = Canal(name=name, logo=logo, uri=uri, group_title=group_title, status=404)
                    canal.save()
                except DataError as e:
                    print(e)
                    canal = Canal(name=name, logo=logo, uri=uri, group_title=group_title, status=404)
                    canal.save()
                except Exception as e:
                    print(e)
                    canal = Canal(name=name, logo=logo, uri=uri, group_title=group_title, status=status)
                    canal.save()
            x += 1


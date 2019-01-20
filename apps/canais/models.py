from django.db import models


class Grupo(models.Model):
    group_title = models.CharField(verbose_name='Group Title', max_length=254, null=True, blank=True)


class Canal(models.Model):
    name = models.CharField(verbose_name='Nome', max_length=254, blank=False, null=False)
    logo = models.URLField(verbose_name='Logo', blank=True, null=True, max_length=254)
    uri = models.URLField(verbose_name='URI', max_length=255)
    group_title = models.CharField(verbose_name='Group Title', max_length=254, null=True, blank=True)
    grupos = models.ManyToManyField(Grupo, verbose_name='grupos', blank=True, related_name='canal_grupos')
    status = models.IntegerField(verbose_name='Status', default=200)

    class Meta:
        verbose_name = 'Canal'
        verbose_name_plural = 'Canais'

    def __str__(self):
        return self.name


from django.db import models


class TGClient(models.Model):
    tg_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tg_id

    class Meta:
        verbose_name = 'TGClient'
        verbose_name_plural = 'TGClients'
        ordering = ['-created_at']


class TGClientQuery(models.Model):
    tg_id = models.CharField(max_length=255)
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tg_id

    class Meta:
        verbose_name = "TGClientQuery"
        verbose_name_plural = "TGClientQueries"
        ordering = ('-created_at',)

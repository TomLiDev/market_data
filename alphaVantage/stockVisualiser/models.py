from django.db import models

class StockData(models.Model):
    symbol = models.TextField(null=True)
    data = models.TextField(null=True)


class ForexData(models.Model):
    symbol = models.TextField(null=True)
    data = models.TextField(null=True)

from django.db import models


class Line(models.Model):
    number = models.IntegerField(max_length=255, null=False, primary_key=True)
    name = models.CharField(max_length=255, null=False)


class Station(models.Model):
    line_id = models.ForeignKey('Line', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)


class Time(models.Model):
    arrive_go = models.CharField(max_length=255, null=True)
    depart_go = models.CharField(max_length=255, null=True)
    arrive_come = models.CharField(max_length=255, null=True)
    depart_come = models.CharField(max_length=255, null=True)
    station_id = models.ForeignKey('Station', on_delete=models.CASCADE)

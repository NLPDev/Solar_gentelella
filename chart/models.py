

# Create your models here.

from django.db import models



class Data(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    precipitable_water = models.FloatField(db_column='Precipitable_water_entire_atmosphere_single_layer', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pressure_surface = models.FloatField(db_column='Pressure_surface', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    relative_humidity= models.FloatField(db_column='Relative_humidity_isobaric', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    temperature_surface = models.FloatField(db_column='Temperature_surface', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    wind_speed= models.FloatField(db_column='Wind_speed_gust_surface', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    solar_zenith = models.FloatField(db_column='solar_zenith', blank=True, null=True)  # Field renamed to remove unsuitable characters. This field type is a guess.
    ghi = models.FloatField(db_column='GHI', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    time = models.DateTimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'data'
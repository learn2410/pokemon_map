from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,on_delete=models.CASCADE,verbose_name='Покемон')
    lon = models.FloatField('Долгота', null=True)
    lat = models.FloatField('Широта', null=True)
    appeared_at = models.DateTimeField('Появится в')
    disappeared_at = models.DateTimeField('Исчезнет в')
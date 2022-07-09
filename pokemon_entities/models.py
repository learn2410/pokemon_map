from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200,default='')
    title_jp = models.CharField(max_length=200,default='')
    image = models.ImageField(null=True,blank=True)
    description = models.TextField(default='')
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="из кого эволюционировал")

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,on_delete=models.CASCADE,verbose_name='Покемон')
    lon = models.FloatField('Долгота', null=True)
    lat = models.FloatField('Широта', null=True)
    appeared_at = models.DateTimeField('Появится в')
    disappeared_at = models.DateTimeField('Исчезнет в')
    level = models.IntegerField('Уровень',default=0)
    health = models.IntegerField('Здоровье',default=0)
    strength = models.IntegerField('Атака',default=0)
    defencr = models.IntegerField('Защита',default=0)
    stamins = models.IntegerField('Выносливость',default=0)
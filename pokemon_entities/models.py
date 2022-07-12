from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField('Название',max_length=200)
    title_en = models.CharField('Название на английском',max_length=200,blank=True)
    title_jp = models.CharField('Название на японском',max_length=200,blank=True)
    image = models.ImageField('Картинка',null=True,blank=True)
    description = models.TextField('Описание',blank=True)
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_evolutions",
        verbose_name="из кого эволюционировал")

    class Meta:
        verbose_name = 'Вид покемона'
        verbose_name_plural = 'Виды покемонов'

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='entities',
        verbose_name='Покемон')
    lon = models.FloatField('Долгота')
    lat = models.FloatField('Широта')
    appeared_at = models.DateTimeField('Появится в')
    disappeared_at = models.DateTimeField('Исчезнет в')
    level = models.IntegerField('Уровень',blank=True,null=True)
    health = models.IntegerField('Здоровье',blank=True,null=True)
    strength = models.IntegerField('Атака',blank=True,null=True)
    defencr = models.IntegerField('Защита',blank=True,null=True)
    stamins = models.IntegerField('Выносливость',blank=True,null=True)

    class Meta:
        verbose_name = 'Покемон'
        verbose_name_plural = 'Покемоны'

    def __str__(self):
        return f'{self.pokemon.title} (id={self.id})'

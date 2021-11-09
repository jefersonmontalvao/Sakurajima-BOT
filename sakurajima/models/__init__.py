import db.models as models


# Test class
class People(models.Model):
    age = models.IntegerField(field_name='Idade')

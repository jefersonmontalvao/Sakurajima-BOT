import db.models as models


# Test class
class People(models.Model):
    age = models.IntegerField()

    id = models.IntegerField(is_nullable=True)


class Animals(models.Model):
    age = models.IntegerField()
    id = models.IntegerField(is_nullable=False, autoincrement=True, primary_key=True)

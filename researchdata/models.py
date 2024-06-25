from django.db import models

class User(models.Model):
    user_id = models.IntegerField(null=False, blank=False, primary_key=True)
    gender = models.CharField(max_length=256, null=False, blank=False)
    birth_year = models.IntegerField(null=False, blank=False)
    ethnicity = models.CharField(max_length=256, null=False, blank=False)
    parent_edu = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.user_id


class Post(models.Model):
    post_id = models.IntegerField(null=False, blank=False, primary_key=True)
    name = models.CharField(max_length=256, null=False, blank=False)
    nature = models.BooleanField(null=False, blank=False)

    def __str__(self):
        return self.post_id


class Personality(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mac1 = models.IntegerField()
    mac2 = models.IntegerField()
    mac3 = models.IntegerField()
    mac4 = models.IntegerField()
    mac5 = models.IntegerField()
    mac6 = models.IntegerField()
    mac7 = models.IntegerField()
    mac8 = models.IntegerField()
    mac9 = models.IntegerField()
    mac10 = models.IntegerField()
    mac11 = models.IntegerField()
    smds1 = models.IntegerField()
    smds2 = models.IntegerField()
    smds3 = models.IntegerField()
    smds4 = models.IntegerField()
    smds5 = models.IntegerField()
    smds6 = models.IntegerField()
    smds7 = models.IntegerField()
    smds8 = models.IntegerField()
    smds9 = models.IntegerField()
    smds10 = models.IntegerField()
    smds11 = models.IntegerField()
    smds12 = models.IntegerField()
    risk1 = models.IntegerField()
    risk2 = models.IntegerField()
    risk3 = models.IntegerField()
    risk4 = models.IntegerField()
    risk5 = models.IntegerField()
    risk6 = models.IntegerField()
    risk7 = models.IntegerField()

class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=512, null=False, blank=False)
    verbal_code = models.CharField(max_length=256, null=False, blank=False)
    post_status_opinion = models.CharField(max_length=256, null=False, blank=False)
    correctness = models.BooleanField(null=False, blank=False)

class Variable(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, primary_key=True)
    description = models.CharField(max_length=256, null=False, blank=False)


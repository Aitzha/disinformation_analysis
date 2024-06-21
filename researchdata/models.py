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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    mac1 = models.IntegerField(null=False, blank=False)
    mac2 = models.IntegerField(null=False, blank=False)
    mac3 = models.IntegerField(null=False, blank=False)
    mac4 = models.IntegerField(null=False, blank=False)
    mac5 = models.IntegerField(null=False, blank=False)
    mac6 = models.IntegerField(null=False, blank=False)
    mac7 = models.IntegerField(null=False, blank=False)
    mac8 = models.IntegerField(null=False, blank=False)
    mac9 = models.IntegerField(null=False, blank=False)
    mac10 = models.IntegerField(null=False, blank=False)
    mac11 = models.IntegerField(null=False, blank=False)
    smds1 = models.IntegerField(null=False, blank=False)
    smds2 = models.IntegerField(null=False, blank=False)
    smds3 = models.IntegerField(null=False, blank=False)
    smds4 = models.IntegerField(null=False, blank=False)
    smds5 = models.IntegerField(null=False, blank=False)
    smds6 = models.IntegerField(null=False, blank=False)
    smds7 = models.IntegerField(null=False, blank=False)
    smds8 = models.IntegerField(null=False, blank=False)
    smds9 = models.IntegerField(null=False, blank=False)
    smds10 = models.IntegerField(null=False, blank=False)
    smds11 = models.IntegerField(null=False, blank=False)
    smds12 = models.IntegerField(null=False, blank=False)
    risk1 = models.IntegerField(null=False, blank=False)
    risk2 = models.IntegerField(null=False, blank=False)
    risk3 = models.IntegerField(null=False, blank=False)
    risk4 = models.IntegerField(null=False, blank=False)
    risk5 = models.IntegerField(null=False, blank=False)
    risk6 = models.IntegerField(null=False, blank=False)
    risk7 = models.IntegerField(null=False, blank=False)

class Response(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    reason = models.CharField(max_length=512, null=False, blank=False)
    verbal_code = models.CharField(max_length=256, null=False, blank=False)
    post_status_opinion = models.CharField(max_length=256, null=False, blank=False)
    correctness = models.BooleanField(null=False, blank=False)

class Variable(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False, primary_key=True)
    description = models.CharField(max_length=256, null=False, blank=False)


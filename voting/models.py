from django.db import models

class Voter(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    has_voted = models.BooleanField(default=False)

class Candidate(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    party = models.CharField(max_length=200, blank=True)
    votes = models.PositiveIntegerField(default=0)

class Vote(models.Model):
    voter = models.OneToOneField(Voter, on_delete=models.CASCADE, related_name="vote")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="vote_records")

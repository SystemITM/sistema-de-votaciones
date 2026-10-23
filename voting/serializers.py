from rest_framework import serializers
from .models import Candidate, Vote, Voter

class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ["id", "name", "email", "has_voted"]
        read_only_fields = ["id", "has_voted"]

    def validate_email(self, value):
        if Candidate.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado como candidato.")
        return value

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ["id", "name", "email", "party", "votes"]
        read_only_fields = ["id", "votes"]

    def validate_email(self, value):
        if Voter.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado como votante.")
        return value

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "voter", "candidate"]
        read_only_fields = ["id"]

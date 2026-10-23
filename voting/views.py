from django.db import IntegrityError, transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Candidate, Vote, Voter
from .serializers import CandidateSerializer, VoteSerializer, VoterSerializer

class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "El registro está relacionado con votos y no puede eliminarse."
    default_code = "conflict"

class VoterListCreateView(generics.ListCreateAPIView):
    queryset = Voter.objects.all().order_by("id")
    serializer_class = VoterSerializer

class VoterDetailView(generics.RetrieveDestroyAPIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer

    def perform_destroy(self, instance):
        if instance.has_voted or Vote.objects.filter(voter=instance).exists():
            raise Conflict()
        instance.delete()

class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all().order_by("id")
    serializer_class = CandidateSerializer

class CandidateDetailView(generics.RetrieveDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def perform_destroy(self, instance):
        if instance.votes or Vote.objects.filter(candidate=instance).exists():
            raise Conflict()
        instance.delete()

class VoteCreateView(APIView):
    def get(self, request):
        votes = Vote.objects.select_related("voter", "candidate").order_by("id")
        return Response(VoteSerializer(votes, many=True).data)

    @extend_schema(request=VoteSerializer, responses={201: VoteSerializer})
    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        voter_id = serializer.validated_data["voter"].pk
        candidate_id = serializer.validated_data["candidate"].pk
        try:
            with transaction.atomic():
                voter = get_object_or_404(Voter.objects.select_for_update(), pk=voter_id)
                candidate = get_object_or_404(Candidate.objects.select_for_update(), pk=candidate_id)
                if voter.has_voted or Vote.objects.filter(voter=voter).exists():
                    raise ValidationError({"voter": "Este votante ya ha votado."})
                vote = Vote.objects.create(voter=voter, candidate=candidate)
                Voter.objects.filter(pk=voter.pk).update(has_voted=True)
                Candidate.objects.filter(pk=candidate.pk).update(votes=F("votes") + 1)
        except IntegrityError:
            raise ValidationError({"voter": "Este votante ya ha votado."})
        return Response(VoteSerializer(vote).data, status=status.HTTP_201_CREATED)

class VoteStatisticsView(APIView):
    def get(self, request):
        total = Vote.objects.count()
        candidates = []
        for candidate in Candidate.objects.all().order_by("id"):
            candidates.append({"id": candidate.id, "name": candidate.name, "votes": candidate.votes,
                               "percentage": round(candidate.votes * 100 / total, 1) if total else 0.0})
        return Response({"total_votes": total, "total_voters_voted": Voter.objects.filter(has_voted=True).count(), "candidates": candidates})

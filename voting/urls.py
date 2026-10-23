from django.urls import path
from .views import CandidateDetailView, CandidateListCreateView, VoteCreateView, VoteStatisticsView, VoterDetailView, VoterListCreateView

urlpatterns = [
    path("voters", VoterListCreateView.as_view()),
    path("voters/<int:pk>", VoterDetailView.as_view()),
    path("candidates", CandidateListCreateView.as_view()),
    path("candidates/<int:pk>", CandidateDetailView.as_view()),
    path("votes", VoteCreateView.as_view()),
    path("votes/statistics", VoteStatisticsView.as_view()),
]

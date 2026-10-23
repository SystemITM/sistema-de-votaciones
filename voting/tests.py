from rest_framework.test import APITestCase
from .models import Candidate, Vote, Voter

class VotingAPITests(APITestCase):
    def setUp(self):
        self.voter_data = {"name": "Ana", "email": "ana@example.com"}
        self.candidate_data = {"name": "Luis", "email": "luis@example.com", "party": "A"}

    def test_register_and_duplicate_emails(self):
        self.assertEqual(self.client.post("/voters", self.voter_data).status_code, 201)
        self.assertEqual(self.client.post("/voters", self.voter_data).status_code, 400)
        self.assertEqual(self.client.post("/candidates", self.candidate_data).status_code, 201)
        self.assertEqual(self.client.post("/candidates", {**self.candidate_data, "name": "Otro"}).status_code, 400)
        self.assertEqual(self.client.post("/candidates", {"name": "Ana", "email": "ana@example.com"}).status_code, 400)

    def test_vote_updates_and_rejects_duplicate_or_missing_records(self):
        voter = Voter.objects.create(**self.voter_data)
        candidate = Candidate.objects.create(**self.candidate_data)
        payload = {"voter": voter.pk, "candidate": candidate.pk}
        response = self.client.post("/votes", payload)
        self.assertEqual(response.status_code, 201)
        voter.refresh_from_db()
        candidate.refresh_from_db()
        self.assertTrue(voter.has_voted)
        self.assertEqual(candidate.votes, 1)
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(self.client.post("/votes", payload).status_code, 400)
        self.assertEqual(self.client.post("/votes", {"voter": 999, "candidate": candidate.pk}).status_code, 400)
        self.assertEqual(self.client.post("/votes", {"voter": voter.pk, "candidate": 999}).status_code, 400)

    def test_statistics_and_deletion_rules(self):
        voter = Voter.objects.create(**self.voter_data)
        candidate = Candidate.objects.create(**self.candidate_data)
        other = Candidate.objects.create(name="Cero", email="cero@example.com")
        self.client.post("/votes", {"voter": voter.pk, "candidate": candidate.pk})
        stats = self.client.get("/votes/statistics").data
        self.assertEqual(stats["total_votes"], 1)
        self.assertEqual(stats["total_voters_voted"], 1)
        self.assertEqual(stats["candidates"][0]["percentage"], 100.0)
        self.assertEqual(stats["candidates"][1]["votes"], 0)
        self.assertEqual(self.client.delete(f"/voters/{voter.pk}").status_code, 409)
        self.assertEqual(self.client.delete(f"/candidates/{candidate.pk}").status_code, 409)
        fresh_voter = Voter.objects.create(name="B", email="b@example.com")
        self.assertEqual(self.client.delete(f"/voters/{fresh_voter.pk}").status_code, 204)
        self.assertEqual(self.client.delete(f"/candidates/{other.pk}").status_code, 204)

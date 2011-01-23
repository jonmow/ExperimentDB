"""This file contains tests for the hypotheses application.

These tests include model tests for Hypothesis objects.
"""
import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from experimentdb.hypotheses.models import Hypothesis, Manipulation, Effect, Process, Context, Evidence

MODELS = [Hypothesis, Manipulation, Effect, Process, Context, Evidence]

class HypothesisModelTests(TestCase):
    """Tests the model attributes of Hypothesis objects contained in the hypotheses app."""

    fixtures = ['test_manipulation','test_protein', 'test_process', 'test_entity', 'test_context', 'test_evidence', 'test_hypothesis']
    
    def setUp(self):
        """Instantiate the test client.  Creates a test user."""
        self.client = Client()
        self.test_user = User.objects.create_user('blah', 'blah@blah.com', 'blah')
        self.test_user.is_superuser = True
        self.test_user.save()
        self.client.login(username='blah', password='blah')

    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()

    def test_create_hypothesis_minimal(self):
        """This is a test for creating a new Hypothesis object, with only the minimum fields being entered.  It also tests the unicode representation."""
        test_hypothesis = Hypothesis(
		    manipulation = Manipulation.objects.get(pk=1), 
			effect = Effect.objects.get(pk=1),
			process = Process.objects.get(pk=1)
			)
        test_hypothesis.save()
        self.assertEquals(test_hypothesis.__unicode__(), "Fixture Protein Overexpression positively regulates glucose import")
		
    def test_create_hypothesis_all_fields_process(self):
        """This is a test for creating a new Hypothesis object, with all fields being entered.  There is one test for process and one for entity (since both cannot be entered simultaneously).  It also tests the unicode representation."""
        test_hypothesis = Hypothesis(
		    manipulation = Manipulation.objects.get(pk=1), 
			effect = Effect.objects.get(pk=1),
			process = Process.objects.get(pk=1),
			context = Context.objects.get(pk=1),
			)
        test_hypothesis.save()
        test_evidence = Evidence.objects.get(pk=1)
        test_hypothesis.evidence.add(test_evidence) # tests the addition of evidence as a m2m field
        test_hypothesis.identical_hypotheses.add(test_hypothesis)	# tests the addition of a symmetrical hypothesis as a m2m field
        self.assertEquals(test_hypothesis.__unicode__(), 'Fixture Protein Overexpression positively regulates glucose import in Fixture Context')

def test_create_hypothesis_all_fields_entity(self):		
        """This is a test for creating a new Hypothesis object, with all fields being entered.  There is one test for process and one for entity (since both cannot be entered simultaneously).  It also tests the unicode representation."""
	
        test_hypothesis = Hypothesis(
		    manipulation = Manipulation.objects.get(pk=1), 
			effect = Effect.objects.get(pk=1),
			process = Process.objects.get(pk=1),
			context = Context.objects.get(pk=1),
			evidence = Evidence.objects.get(pk=1),
			)
        test_hypothesis.save()
        test_evidence = Evidence.objects.get(pk=1)
        test_hypothesis.evidence.add(test_evidence) # tests the addition of evidence as a m2m field
        test_hypothesis.identical_hypotheses.add(test_hypothesis)	# tests the addition of a symmetrical hypothesis as a m2m field		
        self.assertEquals(test_hypothesis.__unicode__(), 'Fixture Protein Overexpression positively regulates glucose import in Fixture Context')			
		
def test_create_hypothesis_create_date(self):
        """This is a test for checking that the create and modified date are being set correctly."""
        test_hypothesis = Hypothesis(
		    manipulation = Manipulation.objects.get(pk=1), 
			effect = Effect.objects.get(pk=1),
			process = Process.objects.get(pk=1)
			)
        test_hypothesis.save()
        self.assertEquals(test_hypothesis.__unicode__(), "Fixture Protein Overexpression positively regulates glucose import")
        self.assertEquals(test_hypothesis.create_date, datetime.date.today())		
        self.assertEquals(test_hypothesis.modified_date, datetime.date.today())			
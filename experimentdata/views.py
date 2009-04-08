from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from experimentdb.data.models import Experiment, Result, Protocol, Cloning
from experimentdb.proteins.models import Protein
from experimentdb.reagents.models import Chemical, Antibody, Cell
from experimentdb.projects.models import Project, SubProject
from experimentdb.external.models import Reference, Contact
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	experiment_list = Experiment.objects.order_by('-experiment_date')
	return render_to_response('data/experiment_list.html', {'experiment_list': experiment_list})

@login_required
def experiment(request, experimentID):
	experiment = get_object_or_404(Experiment, pk=experimentID)
	exp_ID = experiment.experimentID
	exp_result=Result.objects.filter(experiment__experimentID=exp_ID)
	exp_protocol=Protocol.objects.filter(experiment__experimentID=exp_ID)
	exp_researcher=Contact.objects.filter(experiment__experimentID=exp_ID)
	exp_chemical=Chemical.objects.filter(experiment__experimentID=exp_ID)
	exp_antibody=Antibody.objects.filter(experiment__experimentID=exp_ID)
	exp_cell=Cell.objects.filter(experiment__experimentID=exp_ID)
	exp_protein=Protein.objects.filter(experiment__experimentID=exp_ID)
	exp_project=Project.objects.filter(experiment__experimentID=exp_ID)
	exp_subproject=SubProject.objects.filter(experiment__experimentID=exp_ID)
	return render_to_response('data/experiment.html', {'experiment':experiment, 'exp_result':exp_result, 'exp_protocol':exp_protocol, 'exp_researcher':exp_researcher, 'exp_chemical':exp_chemical, 'exp_cell': exp_cell,  'exp_project': exp_project, 'exp_protein': exp_protein, 'exp_subproject':exp_subproject})





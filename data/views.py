from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from experimentdb.data.models import Experiment, Result, Protocol
from experimentdb.data.forms import ResultForm
from experimentdb.proteins.models import Protein
from experimentdb.reagents.models import Chemical, Antibody, Cell
from experimentdb.projects.models import Project, SubProject
from experimentdb.external.models import Reference, Contact
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

@login_required
def index(request):
	"""This view shows a list of all experiments.

	This list is ordered by the experiment date in descending order.  This view could potentially be rendered by a generic view.
	"""
	experiment_list = Experiment.objects.order_by('-experiment_date')
	return render_to_response('experiment_list.html', {'experiment_list': experiment_list},context_instance=RequestContext(request))

@login_required
def experiment(request, experimentID):
	"""This renders a detailed page of an experiment.

	The view will show the experiment, and all associated reagents, proteins, projects and results associated with this object.
	"""
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
	return render_to_response('experiment.html', {'experiment':experiment, 'exp_result':exp_result, 'exp_protocol':exp_protocol, 'exp_researcher':exp_researcher, 'exp_chemical':exp_chemical, 'exp_cell': exp_cell,  'exp_project': exp_project, 'exp_protein': exp_protein, 'exp_subproject':exp_subproject}, context_instance=RequestContext(request))

@login_required
def protocol_list(request):
	"""This renders a view in which all protocols are displayed.

	In the case of deprecated protocols (i.e. protocols not marked as active), these are not shown.  This view could also be rendered as a generic view.
	"""
	protocol_list = Protocol.objects.all()
	return render_to_response('protocol_list.html', {'protocol_list':protocol_list, },context_instance=RequestContext(request))

@login_required
def protocol_detail(request, protocol_slug):
	"""This renders a view in which a protocol detail page is shown.

	This view should be deprecated in favor of a redirection directly to the wiki page for this protocol
	"""
	protocol = get_object_or_404(Protocol, protocol_slug=protocol_slug)
	protocol_experiments = Experiment.objects.filter(protocol=protocol)	
	return render_to_response ('protocol_detail.html', {'protocol': protocol, 'protocol_experiments':protocol_experiments},context_instance=RequestContext(request))

@login_required
def result_new(request, experimentID):
	"""This renders a form to add a new result.

	This view will be sent from a particular experiment and will attach the result to that particular experiment.	
	"""
	experiment = get_object_or_404(Experiment, pk=experimentID)
	if request.method == "POST":
		form = ResultForm(request.POST, request.FILES)
		if form.is_valid():
			result = form.save(commit=False)
			result.experiment_id = experiment.experimentID
			result.save()
			form.save()
			return HttpResponseRedirect("/experimentdb/experiments/")
	else:
		form = ResultForm()
	return render_to_response('result_form.html', {'form':form, 'experiment':experiment},context_instance=RequestContext(request))

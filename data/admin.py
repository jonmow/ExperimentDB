from experimentdb.data.models import Protocol, Experiment, Result, Sequencing
from django.contrib import admin

class ResultInline(admin.TabularInline):
	model = Result
	fields = ('conclusions','result_figure1', 'result_figure2','file1','file2','file3','rawscan1','rawscan2','rawscan3','rawscan4','rawscan5' )
	extra = 1

class ProtocolAdmin(admin.ModelAdmin):
	pass
admin.site.register(Protocol, ProtocolAdmin)

class ExperimentAdmin(admin.ModelAdmin):
	fields = ('project', 'subproject', 'experimentID', 'experiment', 'protocol', 'assay', 'experiment_date', 'cellline', 'antibodies', 'chemicals', 'constructs', 'siRNA', 'researcher', 'protein', 'purified_protein')
	inlines = [ResultInline, ]
	date_hierarchy = 'experiment_date'
	list_filter = ('protein', 'assay')
	list_display = ('experiment_date', 'assay', 'experiment')
	
admin.site.register(Experiment, ExperimentAdmin)

class ResultAdmin(admin.ModelAdmin):
	pass
admin.site.register(Result, ResultAdmin)

class SequencingAdmin(admin.ModelAdmin):
	pass
admin.site.register(Sequencing, SequencingAdmin)


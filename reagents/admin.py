from experimentdb.reagents.models import Antibody, Chemical, Cell, Purified_Protein, Construct, Primer, Strain, Selection
from django.contrib import admin

class AntibodyAdmin(admin.ModelAdmin):
	list_display = ('antibody', 'protein_size', 'source_species', 'source', 'catalog')
	fields = ('antibody', 'protein', 'protein_size', 'source_species', 'source', 'vendor', 'location', 'catalog', 'notes', 'antibody_slug')
	radio_fields = {"source_species" : admin.HORIZONTAL}
	prepopulated_fields = {"antibody_slug" : ("antibody",)}
admin.site.register(Antibody, AntibodyAdmin)

class ChemicalAdmin(admin.ModelAdmin):
	list_display = ('name', 'source')
admin.site.register(Chemical, ChemicalAdmin)

class CellAdmin(admin.ModelAdmin):
	list_display = ('description', 'species', 'source')
	fields = ('description', 'species', 'notes', 'name')
	prepopulated_fields = {"name" : ("description",)}
admin.site.register(Cell, CellAdmin)

class ConstructAdmin(admin.ModelAdmin):
	fields = ('construct', 'plasmid', 'protein', 'selection', 'source', 'location', 'box', 'sequencing_contig', 'sequenced_object','notes', 'contact')
	list_display = ('construct', 'plasmid', 'location', 'box', 'selection', 'source')
	list_filter = ('protein', 'plasmid')
admin.site.register(Construct, ConstructAdmin)

class Purified_ProteinAdmin(admin.ModelAdmin):
	list_display = ('name', 'purification_date', 'construct')
	list_filter = ('purification_date', 'protein', 'construct')
admin.site.register(Purified_Protein, Purified_ProteinAdmin)

class PrimerAdmin(admin.ModelAdmin):
	list_display = ('name', 'primer_type', 'date_ordered', 'vendor', 'protein', 'sequence')
	list_filter = ('primer_type', 'protein')
admin.site.register(Primer, PrimerAdmin)

class StrainAdmin(admin.ModelAdmin):
	list_display = ('name', 'genotype', 'selection')
admin.site.register(Strain, StrainAdmin)

class SelectionAdmin(admin.ModelAdmin):
	pass
admin.site.register(Selection, SelectionAdmin)
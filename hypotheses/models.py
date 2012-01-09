"""
The this file controls the data models in the hypotheses application.

The purpose of this app is to organize results and observations or summaries of experimental hypotheses in a systematic way.  A hypothesis is something that is observed about a biological process or biological entity.  It is supported by evidence, which could be an external publication or an experiment contained in this database.  The goal is to be able to say "X causes Y in this context, with the following evidence" 

The hypothesis app has 7 data models:
* Hypothesis
* Manipulation
* Effect
* Process
* Entity
* Context
* Evidence 
* CitationType
"""

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from experimentdb.reagents.models import Primer, Construct, Chemical, Species, Cell, Strain
from experimentdb.proteins.models import Protein
from experimentdb.data.models import Protocol, Experiment
from experimentdb.external.models import Contact, Reference


MANIPULATION_TYPE = (
	('Treatment', 'Treatment'),
	('Overexpression', 'Overexpression'),
	('Knockdown', 'Knockdown'),
	('Knockout', 'Knockout'),
)

CONTEXT_TYPE = (
	('Species', 'Species'),
	('Tissues', 'Tissues'),
	('Cells', 'Cells'),
	('Sub-Cellular Location', 'Sub-Cellular Location'),
	('Multi-Protein Complex', 'Multi-Protein Complex'),
)

EVIDENCE_TYPE = (
	('Publication', 'Publication'),
	('Experiment', 'Experiment'),
	('Un-Published Communication', 'Un-Published Communication'),
	('Presentation', 'Presentation'),
    ('Figure','Figure')
)

CITATION_GROUP = (
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
    ('Neutral', 'Neutral'),
    ('No Opinion', 'No Opinion')
)

class Hypothesis(models.Model):
    """This model is the main model for this app, defining the particular hypothesis under consideration.

    This app has many to many field links to Manipulation, Context and Evidence and a ForeignKey link to an Effect and either a Process or Entity.  The required fields are manipulation, effect and either a process or entity.  The unicode representation of this model is going to be "(manipulation) (effects)/(process or entity in which there could be several).  The absolute url for an instance is /experimentdb/hypothesis/# where # is the primary key.  Tests are generated to test model formation with required and all fields, as well as to test the clean and absolute_url.  
    """
	
    manipulation = models.ForeignKey('Manipulation')
    effect = models.ForeignKey('Effect')
    process = models.ForeignKey('Process', blank=True, null=True, help_text="A biological process such as glucose uptake or endocytosis.  Select either an entity or a process but not both")	
    entity = models.ForeignKey('Entity', blank=True, null=True, help_text="A particular biological entity such as a protein or phosphorylation site.  Select either an entity or a process but not both.")
    context = models.ForeignKey('Context', blank=True, null=True, help_text="Describes the model system and potential restrictions.  Since only one context might be selected, the context may need to be quite specific.")	
    evidence = models.ManyToManyField('Evidence', blank=True, null=True)
    identical_hypotheses = models.ManyToManyField("self", blank=True, null=True, help_text="Some processes or entities may generally correlate.  As an example, the process activation of mTORC1 generally correlates wth activation of pThr 389 phosphorylation.  In these cases, both hypotheses are symmetrically linked.")
    create_date = models.DateField(auto_now_add = True)
    modified_date = models.DateField(auto_now = True)

    def clean(self):
        """This validates that either a process or an entity (but not both) are selected."""
        if self.process and self.entity:
            raise ValidationError('Choose either a process or an entity but not both.')
        if self.process == None and self.entity == None:
            raise ValidationError('Choose a process or entity')		
	
    def __unicode__(self):
        """The unicode string for this model will show entity of entity is present and process if process is present.  The over-riding of clean should ensure that only one of the two is present."""
        if self.process and self.context:
            return u'%s %s %s in %s' % (self.manipulation, self.effect, self.process, self.context)
        elif self.process:
            return u'%s %s %s' % (self.manipulation, self.effect, self.process)
        elif self.entity and self.context:
            return u'%s %s %s in %s' % (self.manipulation, self.effect, self.entity, self.context)
        elif self.entity:
            return u'%s %s %s' % (self.manipulation, self.effect, self.entity)
        else:
            return "Unspecified Hypothesis"
			
    @models.permalink
    def get_absolute_url(self):
        return ('hypothesis-detail', [str(self.id)])			

    class Meta:
        verbose_name_plural = 'hypotheses'			

	
class Manipulation(models.Model):
    """This model defines particular manipulations of experimental systems.
	
	This Manipulation or (treatment), could be several things.  It may refer to the manipulation of a protein.  This could be a knockout of a gene/knockdown with a siRNA, overexpression with a construct, or treatment with a chemical or another protein.  The required fields are type plus the appropriate chemical, protein_added or protien.  There are optional fields for manipulation time and concentration (if needed).  There are validators to validate each type.  The unicode representation of a manipulation is "something - type" depending on the type.
    """
    type = models.CharField(max_length=25, choices=MANIPULATION_TYPE)
    time = models.TimeField(blank=True, null=True, help_text = "Enter if an incubation time is relevant.  Use format hour,min,sec with min and sec")
    concentration = models.CharField(max_length=25, blank=True, null=True, help_text = "Enter if a particular concentration or amount of chemical/protein is used")
    chemical = models.ForeignKey(Chemical, blank=True, null=True, help_text="Enter a chemical or a protein_added when type is treatment")
    protein_added = models.ForeignKey(Protein, blank=True, null=True, related_name="stimulating_protein", help_text="Use this or chemical when type is treatment.  This refers to a stimulating protein, not a protein being tested")	
    protein = models.ForeignKey(Protein, blank=True, null=True, related_name="target_protein", help_text="Select the target of the knockdown/knockout/inhibition/overexpression.")
	
    def clean(self):
        """This validates that a treatment has a chemical or a protein_added."""
        if self.type == "Treatment" and self.chemical == None and self.protein_added == None:
            raise ValidationError('Choose either a chemical or protein for a treatment.')	
        """This validates that an overexpression has a construct."""
        if self.type == "Overexpression" and self.protein == None:
            raise ValidationError('Choose an overexpressed protein')
        """This validates that a knockdown has a protein target."""
        if self.type == "Knockdown" and self.protein == None:
            raise ValidationError('Choose a protein which is knocked down.')
        """This validates that a knockout has a protein target.""" 
        if self.type == "Knockout"	and self.protein == None:
            raise ValidationError('Choose a protein which is knocked out')

			
    def __unicode__(self):
        """The unicode representation depends on the type of manipulation."""	
        if self.type == "Treatment" and self.chemical and self.protein_added:
            return u'%s and %s %s' % (self.chemical, self.protein_added, self.type)
        elif self.type == "Treatment" and self.chemical:
            return u'%s %s' % (self.chemical, self.type)
        elif self.type == "Treatment" and self.protein_added:
            return u'%s %s' % (self.protein_added, self.type)
        else:
            return u'%s %s' % (self.protein, self.type)
            
    @models.permalink
    def get_absolute_url(self):
        return ('manipulation-detail', [str(self.id)])	            
			
class Effect(models.Model):
    """The effect is a linker between a manipulation and a process.
	
    Typically a manipulation stimulates, has no effect or inhibits a process or entity.  This model is populated as an initial data fixutre, but other modifiers can be added through the admin interface.  The effects have specified ontology representations."""
	
    effect = models.CharField(max_length=50)
    description = models.TextField(max_length=250, blank=True, null=True)
    ontology = models.URLField(blank=True, null=True, help_text = "A defined ontology describing the effect")
	
    def __unicode__(self):
        return u'%s' % self.effect


class Process(models.Model):
    """Each hypothesis involves a potential manipulation of either a process or an entity.
	
	A process is typically a biological process such as endocytosis.  A particular process could be readout by a particular biological entity.  The reverse is also possibly true.  These cases are defined by symmetrical hypotheses at the Hypothesis levelIt is defined by the Gene Ontology as "Any process specifically pertinent to the functioning of integrated living units: cells, tissues, organs, and organisms. A process is a collection of molecular events with a defined beginning and end." See GO:0008150 for the accurate record.
	
    This data model has a name, gene_ontology_id and definition, each of which should match the Gene Ontology definitions.  It also has an optional asssay field which references a Protocol instance from the data application.  The unicode representation of a process is the name and the slug field is automatically generated from the name field."""

    name = models.CharField(max_length=100, help_text="A biological process, such as endocytosis")
    gene_ontology_id = models.CharField(blank = True, null= True, max_length=15, help_text="This is a gene ontology accesion number in the format GO:0046323 where the number can change.  Find an appropriate gene ontology id at http://amigo.geneontology.org/cgi-bin/amigo/search.cgi")
    definition = models.CharField(max_length=100, blank=True, null=True)
    assay = models.ManyToManyField(Protocol, blank=True, null=True, help_text="The assay we use to monitor this process")
    slug = models.SlugField(max_length=100, blank=True, null=True, editable=False)

    def save(self):
        """The save is over-ridden to slugify the name field into a slugfield."""
        self.slug = slugify( self.name )
        super( Process, self ).save()

    def __unicode__(self):
        """The unicode representation of a process is its name."""
        return u'%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('process-detail', [str(self.id)])	        

    class Meta:
        verbose_name_plural = 'processes'			

class Entity(models.Model):
    """Each hypothesis involves a potential :class:`~experimentdb.hypotheses.models.Manipulation` of either a :class:`~experimentdb.hypotheses.models.Process` or an :class:`~experimentdb.hypotheses.models.Entity`.
	
	An :class:`~experimentdb.hypotheses.models.Entity`, generally a biological thing, but is usually a specific :class:`~experimentdb.protein.models.Protein` or part of a protein or alternatively a :class:`~experimentdb.reagents.models.Chemical`.  
    It could be a whole protein, or a phosphorylation site or a transcript.  
    If it is a part of a protein then that should be specified under the name field.
    An entity has to be something which can be regulated positively, negatively or unaffected by the :class:`~experimentdb.hypotheses.models.Manipulation` as part of a :class:`~experimentdb.hypotheses.models.Hypothesis`.  A :class:`~experimentdb.hypotheses.models.Hypothesis` should test either a :class:`~experimentdb.hypotheses.models.Process` or an :class:`~experimentdb.hypotheses.models.Entity` but not both.  With that said, a particular :class:`~experimentdb.hypotheses.models.Entity` could be a readout for a biological function.  The reverse is also possibly true.  These cases are defined by symmetrical hypotheses at the :class:`~experimentdb.hypotheses.models.Hypothesis` level.
	
    A unique name is a required field, and either a protein or a chemical must be chosen."""
	
    name = models.CharField(max_length=100, unique=True, help_text="The specific name for the entity, such as pSer 473 or Akt mRNA")
    protein = models.ManyToManyField(Protein, blank=True, null=True, help_text="Select either a protein or a chemcial.")
    chemical = models.ManyToManyField(Chemical, 
        blank=True, 
        null=True,
        verbose_name="Small Molecule",
        help_text="Select either a protein or a chemcial.") 
    slug = models.SlugField(max_length=100, blank=True, null=True, editable=False)
	
    def save(self):
        """The save is over-ridden to slugify the name field into a slugfield."""
        self.slug = slugify( self.name )
        super( Entity, self ).save()

    def __unicode__(self):
        """The unicode representation of an entity is its name."""
        return u'%s' % self.name
		
    def clean(self):
        """This validates that an entity has either a chemical or a protein noted."""
        if self.chemical == None and self.protein == None:
            raise ValidationError('Choose either a chemical or protein.')	
        
    class Meta:
        verbose_name_plural = 'processes'
        
	
class Context(models.Model):
    """A context specifies the model system under which the hypothesis is tested.

    The context has optional parameters for cell lines, yeast strain.  It is slugified upon save into a slug field.  The required fiels are name and type.  There are several optional fields."""	

    name = models.CharField(max_length=100, help_text="A description of the specific context of the hypotheses.")
    type = models.CharField(max_length=50, choices=CONTEXT_TYPE, help_text="A general category")
    strain = models.ManyToManyField(Strain, blank=True, null=True, help_text="Strain specific context")
    cell_line = models.ManyToManyField(Cell, blank=True, null=True, help_text="Cell line specific context")
    species = models.ManyToManyField(Species, blank=True, null=True, help_text="Species specific context.")	
    uri = models.URLField(blank=True, null=True, help_text="If a specific URI is known for this context enter it here.  Search BioOntology at http://clkb.ncibi.org/browse.php for possible URI's")
    slug = models.SlugField(blank=True, null=True, editable=False)
	
    def save(self):
        """The save is over-ridden to slugify the name field into a slugfield."""
        self.slug = slugify( self.name )
        super( Context, self ).save()

    def __unicode__(self):
        """The unicode representation of a context is its name."""
        return u'%s' % self.name	

	
class Evidence(models.Model):
    """Evidence instances are supporting or dissenting experiments, papers or communications regarding a hypothesis.

    The required fields for a piece of evidence are the evidence_type, the citation_type and whether it is public (which is set to False as a default).  There are optional fields for paper or contact.  The clean method is over-ridden to ensure that when a evidence_type is a reference, a paper is entered and when a evidence_type is a communication then a contact is entered."""

    evidence_type = models.CharField(max_length=50, choices = EVIDENCE_TYPE, help_text="Type of evidence")
    citation_type = models.ForeignKey('CitationType')
    experiment = models.ForeignKey(Experiment, blank=True, null=True)	
    paper = models.ForeignKey(Reference, blank=True, null=True)	
    contact = models.ForeignKey(Contact, blank=True, null=True, help_text="Source of unpublished evidence.")
    figure = models.ImageField(upload_to='evidence/%Y/%m/%d', blank=True, null=True, help_text="Select a file to upload.")
    notes = models.TextField(max_length=500, blank=True, null=True, help_text="Description of evidence")
    public = models.BooleanField(help_text="Is the evidence to be made public?")
    create_date = models.DateField(auto_now_add = True)
    modified_date = models.DateField(auto_now = True)

    def clean(self):
        """This validates that evidence with a paper has a reference."""
        if self.evidence_type == "Publication" and self.paper == None:
            raise ValidationError('Enter a paper for evidence from a publication')	
        """This validates that evidence with an experiment has a experiment."""
        if self.evidence_type == "Experiment" and self.experiment == None:
            raise ValidationError('Select an experiment for evidence from an experiment')	
        """This validates that evidence with a communication has a contact."""
        if self.evidence_type == "Un-Published Communication" and self.contact == None:
            raise ValidationError('Enter a contact for evidence from a communication')	
        """This validates that evidence with a communication has a contact."""
        if self.evidence_type == "Presentation" and self.contact == None:
            raise ValidationError('Enter a contact for evidence from a presentation')
        if self.evidence_type == "Figure" and self.figure == None:
            raise ValidationError('Enter a contact for evidence from a presentation')            

    def __unicode__(self):
        """The unicode representation of a context is its evidence_type and its experiment."""
        if self.experiment:
            return u'Experiment - %s' % self.experiment
        if self.paper:
            return u'Paper - %s' % self.paper 		
        if self.contact:
            return u'Un-Published Communication - %s' % self.contact
            
    def get_absolute_url(self):
        """The absolute url of evidence depends on the evidence type, and directs to that objects absolute url."""
        if self.experiment:
            return self.experiment.get_absolute_url()
        if self.paper:
            return self.paper.get_absolute_url()
        if self.contact:
            return self.contact.get_absolute_url()      
            
    class Meta:
            verbose_name_plural = 'evidence'				

		
class CitationType(models.Model):
    """The citation type is a series of classifiers to link evidence to its opinion of a hypothesis.
	
    This class is based on the cito ontology (see http://purl.org/net/cito/).  Some but not all instances of this ontology are loaded upon installation as initial data.  Other potential citation types may be added as well.  Although optional, it is recommended that alternate citation types have URI's included.  The class is not part of the cito schema, and is added to orient evidences as positive or negative."""

    group = models.CharField(max_length=50, choices=CITATION_GROUP)	
    label = models.CharField(max_length=50)
    uri = models.URLField(blank=True, null=True)
    comment = models.TextField(max_length=250, blank=True, null=True)	
	
    def __unicode__(self):
        """The unicode representation of a CitationType is the label."""	
        return u'%s' % self.label	
		
    class Meta:
        verbose_name_plural = 'citation types'			
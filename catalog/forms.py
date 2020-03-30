from django import forms


class SearchForm(forms.Form):            #Form per ricerca oggetti
    SCHOOL_LEVEL = (
        ('M', 'Medie'),
        ('S', 'Superiori'),
        ('U', 'Università'),
    )
    name=forms.CharField(max_length=50,required=False,label="Nome dell'oggetto")
    subject=forms.CharField(max_length=50,required=False,label="Materia/Disciplina")
    school_level=forms.ChoiceField(choices=SCHOOL_LEVEL,required=False,widget=forms.RadioSelect,label="Livello scolastico")

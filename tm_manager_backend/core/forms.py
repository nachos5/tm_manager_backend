from django import forms


class ModelFormCreateOrUpdate(forms.ModelForm):
    def clean(self, *args, **kwargs):
        super().clean()
        # ef update
        if self.instance.pk:
            cleaned_data_new = self.cleaned_data.copy()
            for field in self.cleaned_data:
                # eyðum fieldum sem við erum ekki að nota í update-inu
                if field not in self.fields_to_update:
                    cleaned_data_new.pop(field)
            self.cleaned_data = cleaned_data_new


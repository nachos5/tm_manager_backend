from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_jwt.decorators import login_required

# passar usernum inn í form saveið
class DjangoModelFormMutationUser(DjangoModelFormMutation):
    class Meta:
        abstract = True

    # override-um til að passa usernum í form save
    @classmethod
    @login_required
    def perform_mutate(cls, form, info):
        user = info.context.user
        obj = form.save(user=user)
        kwargs = {cls._meta.return_field_name: obj}
        return cls(errors=[], **kwargs)

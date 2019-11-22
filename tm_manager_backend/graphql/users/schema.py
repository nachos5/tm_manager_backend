import graphene
import graphql_jwt

from graphql_jwt.decorators import login_required

from . import types
from .mutations import UserCreateMutation
from .resolvers import resolve_me, resolve_user, resolve_users
from ..core.fields import PrefetchingConnectionField


class UsersQueries(graphene.ObjectType):
    me = graphene.Field(types.User)
    user = graphene.Field(types.User, id=graphene.Argument(graphene.ID))
    user_jwt = graphene.Field(types.User, token=graphene.Argument(graphene.String))
    users = PrefetchingConnectionField(types.User)

    def resolve_me(self, info, **kwargs):
        return resolve_me(info)

    @login_required
    def resolve_user_jwt(self, info, **kwargs):
        return info.context.user

    def resolve_user(self, info, id, **kwargs):
        return resolve_user(info, id)

    def resolve_users(self, info, **kwargs):
        return resolve_users(info)


class UsersMutations(graphene.ObjectType):
    # jwt
    token_create = graphql_jwt.ObtainJSONWebToken.Field()
    token_refresh = graphql_jwt.Verify.Field()
    token_verify = graphql_jwt.Refresh.Field()

    user_create = UserCreateMutation.Field()


from django.db.models.query import QuerySet

from graphene.relay import PageInfo
from graphene_django.fields import DjangoConnectionField
from graphql_relay.connection.arrayconnection import connection_from_list_slice


class PrefetchingConnectionField(DjangoConnectionField):
    @classmethod
    def connection_resolver(
        cls,
        resolver,
        connection,
        default_manager,
        max_limit,
        enforce_first_or_last,
        root,
        info,
        **args
    ):

        # Disable `enforce_first_or_last` if not querying for `edges`.
        values = [
            field.name.value for field in info.field_asts[0].selection_set.selections
        ]
        if "edges" not in values:
            enforce_first_or_last = False

        return super().connection_resolver(
            resolver,
            connection,
            default_manager,
            max_limit,
            enforce_first_or_last,
            root,
            info,
            **args
        )

    @classmethod
    def resolve_connection(cls, connection, default_manager, args, iterable):
        if iterable is None:
            iterable = default_manager

        if isinstance(iterable, QuerySet):
            _len = iterable.count()
        else:
            _len = len(iterable)

        connection = connection_from_list_slice(
            iterable,
            args,
            slice_start=0,
            list_length=_len,
            list_slice_length=_len,
            connection_type=connection,
            edge_type=connection.Edge,
            pageinfo_type=PageInfo,
        )
        connection.iterable = iterable
        connection.length = _len
        return connection

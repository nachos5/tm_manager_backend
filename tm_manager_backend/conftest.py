# pylint: disable=redefined-outer-name, unused-argument
import pytest
from django.conf import settings
from django.test import RequestFactory

from tm_manager_backend.users.tests.factories import UserFactory

from tm_manager_backend.tournament import models as TournamentModels


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def user2():
    return UserFactory()


@pytest.fixture
def user3():
    return UserFactory()


@pytest.fixture
def super_category(db):
    return TournamentModels.SuperCategory.objects.create(name="super1")


@pytest.fixture
def category_first(db, super_category):
    return TournamentModels.Category.objects.create(
        name="category first", super_category=super_category
    )


@pytest.fixture
def category_second(db, super_category):
    return TournamentModels.Category.objects.create(
        name="category second", super_category=super_category
    )


@pytest.fixture
def tournament(db, user, user2, user3, category_first):
    t = TournamentModels.Tournament.objects.create(
        creator=user, category=category_first, name="test tournament"
    )
    t.admins.add(user2)
    t.registered_users.add(user3)
    return t


# @pytest.fixture
# def match(db, tournament):
#   m = Match.objects.create(tournament=tournament, )

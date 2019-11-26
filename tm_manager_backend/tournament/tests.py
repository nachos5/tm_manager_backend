def test_tournament_models(super_category, category_first, category_second, tournament):
    categories = super_category.sub_categories.all()
    assert len(categories) == 2
    assert category_first in categories
    assert category_second in categories
    assert tournament in category_first.tournaments.all()
    assert len(tournament.admins.all()) == 1
    assert len(tournament.registered_users.all()) == 1


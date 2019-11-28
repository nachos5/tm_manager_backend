import math
import time

from .. import models


def init_single_elim(tournament):
    root = models.Match.objects.create(tournament=tournament)
    split_match_node(tournament, root, tournament.n_rounds)


def split_match_node(tournament, match_node, n_rounds):
    # komin fram yfir heildarumferðir þá hættum við
    if match_node.level >= n_rounds:
        return
    # splittum hverri match nóðu í tvær undirnóður
    first_subnode = models.Match.objects.create(
        tournament=tournament, parent=match_node
    )
    second_subnode = models.Match.objects.create(
        tournament=tournament, parent=match_node
    )
    # endurkvæmni
    split_match_node(tournament, first_subnode, n_rounds)
    split_match_node(tournament, second_subnode, n_rounds)


def parent_seeding(match):
    # parent matchinn fær winnerinn
    parent = match.parent
    if not parent:
        return
    # efri matchinn með hærra
    higher_id = max(list(parent.children.all().values_list("id", flat=True)))
    if match.id == higher_id:
        parent.user_home = match.winner
    else:
        parent.user_visitor = match.winner

    parent.save()


def free_match_win(match):
    """ 
    einn user í matchi => frítt win,
    pössum áfram þangað til hann mun mæta einhverjum.
    """
    match.winner = match.user_home if match.user_home else match.user_visitor
    match.save()
    parent_seeding(match=match)
    parent = match.parent
    # gerum þetta endurkvæmt þangað til userinn mun mæta einhverjum
    if parent and not parent.users_both_sides:
        free_match_win(match=parent)


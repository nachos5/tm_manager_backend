import math

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

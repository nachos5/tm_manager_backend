import time


def match_bracket(match, matches, users):
    """ setur bracketinn á form eins og react-tournament-bracket biður um """
    # fyrsti userinn
    if match.user_home_id:
        home_user = [u for u in users if u.id == match.user_home_id][0]
        home_user_dict = dict({"id": home_user.id, "name": home_user.username})
    else:
        home_user_dict = dict()
    # annar userinn
    if match.user_visitor_id:
        visitor_user = [u for u in users if u.id == match.user_visitor_id][0]
        visitor_user_dict = dict({"id": visitor_user.id, "name": visitor_user.username})
    else:
        visitor_user_dict = dict()

    # tékkum hvort matchinn hafi "börn" ("seeding matches")
    children = [x for x in matches if x.parent_id == match.id]
    if children:
        # sækjum leiki recursive
        home_game = match_bracket(children[0], matches, users)
        visitor_game = match_bracket(children[1], matches, users)

        home = dict(
            {
                "seed": {
                    "displayName": "",
                    "rank": 1,
                    "sourcePool": dict(),
                    "sourceGame": home_game,
                },
                "team": home_user_dict,
                "score": {"score": match.user_home_points},
            }
        )

        visitor = dict(
            {
                "seed": {
                    "displayName": "",
                    "rank": 1,
                    "sourcePool": dict(),
                    "sourceGame": visitor_game,
                },
                "team": visitor_user_dict,
                "score": {"score": match.user_visitor_points},
            }
        )
    else:
        home = dict(
            {"team": home_user_dict, "score": {"score": match.user_home_points}}
        )
        visitor = dict(
            {"team": visitor_user_dict, "score": {"score": match.user_visitor_points}}
        )

    d = dict(
        {
            "id": match.id,
            "name": "",
            "scheduled": int(
                round(time.mktime(match.tournament.date.timetuple()) * 1000)
            ),
            "sides": {"home": home, "visitor": visitor},
        }
    )

    return d

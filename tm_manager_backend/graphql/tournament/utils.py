import time


def match_bracket(match):
    """ setur bracketinn á form eins og react-tournament-bracket biður um """
    # tékkum hvort það séu userar fyrir þennan match
    users = match.users.all()
    # fyrsti userinn
    if len(users) > 0:
        home_user = users[0]
        home_user_dict = dict({"id": home_user.id, "name": home_user.username})
    else:
        home_user_dict = dict()
    # annar userinn
    if len(users) == 2:
        visitor_user = users[1]
        visitor_user_dict = dict({"id": visitor_user.id, "name": visitor_user.username})
    else:
        visitor_user_dict = dict()

    # tékkum hvort matchinn hafi "börn" ("seeding matches")
    children = match.children.all()
    if children:
        # sækjum leiki recursive
        home_game = match_bracket(children[0])
        visitor_game = match_bracket(children[1])

        home = dict(
            {
                "seed": {
                    "displayName": "",
                    "rank": 1,
                    "sourcePool": dict(),
                    "sourceGame": home_game,
                },
                "team": home_user_dict,
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
            }
        )
    else:
        home = dict({"team": home_user_dict})
        visitor = dict({"team": visitor_user_dict})

    d = dict(
        {
            "id": match.id,
            "name": "",
            "scheduled": int(round(time.time() * 1000)),
            "sides": {"home": home, "visitor": visitor},
        }
    )

    return d

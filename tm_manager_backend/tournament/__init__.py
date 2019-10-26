# Text dótið er það eina sem við sýnum á frontendanum, hitt er til að geyma í database-inu
class TournamentStatus:
    OPEN = "open"
    OPEN_TEXT = "Open"
    CLOSED = "closed"
    CLOSED_TEXT = "Closed"
    ONGOING = "ongoing"
    ONGOING_TEXT = "Ongoing"
    FINISHED = "finished"
    FINISHED_TEXT = "Finished"
    CANCELED = "canceled"
    CANCELED_TEXT = "Canceled"

    CHOICES = [
        (OPEN, OPEN_TEXT),
        (CLOSED, CLOSED_TEXT),
        (ONGOING, ONGOING_TEXT),
        (FINISHED, FINISHED_TEXT),
        (CANCELED, CANCELED_TEXT),
    ]

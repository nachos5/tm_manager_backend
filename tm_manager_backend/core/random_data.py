import random

from datetime import datetime, time, timedelta
from faker import Faker

from ..tournament import models as TModels
from ..users.forms import UserCreationForm
from ..users.models import User

# setjum testsorp í database-ið
def generate_initial_data():
    print("Generating initial data...")
    fake = Faker()
    # búum til 100 usera
    for i in range(100):
        create_test_user()

    # búum til yfirflokka
    sports = TModels.SuperCategory.objects.create(name="Sports")
    gaming = TModels.SuperCategory.objects.create(name="Gaming")
    # búum til undirflokka
    foosball = TModels.Category.objects.create(name="Foosball", super_category=sports)
    table_tennis = TModels.Category.objects.create(
        name="Table Tennis", super_category=sports
    )
    competetive_eating = TModels.Category.objects.create(
        name="Competetive Eating", super_category=sports
    )
    cs_go = TModels.Category.objects.create(name="CS:GO", super_category=gaming)
    dota = TModels.Category.objects.create(name="DotA", super_category=gaming)
    lol = TModels.Category.objects.create(name="LoL", super_category=gaming)
    flokkar = [foosball, table_tennis, competetive_eating, cs_go, dota, lol]

    # mót
    users = list(User.objects.all())
    # superuser = User.objects.get(is_superuser=True)
    slots = [8, 16, 32, 64, 128]
    dates = [datetime.now(), datetime.now() + timedelta(weeks=1)]
    times = [time(hour=17, minute=0), time(hour=19, minute=30), time(hour=20, minute=0)]
    locations = ["Nörd", "Hallgrímskirkja"]
    for f in flokkar:
        # 10 mót fyrir hvern flokk
        for i in range(10):
            creator = random.choice(users)
            slots_curr = random.choice(slots)
            t = TModels.Tournament.objects.create(
                creator=creator,
                name=" ".join(fake.words()) + " tournament",
                category=f,
                slots=slots_curr,
                date=random.choice(dates),
                time=random.choice(times),
                location=random.choice(locations),
            )
            users_max = slots_curr if len(users) >= slots_curr else len(users)
            random_users = random.sample(users, random.randint(0, users_max))
            t.registered_users.set(random_users)

    print("Generating initial data done")


def create_test_user():
    fake = Faker()
    test_pw = "epli1234"
    form = UserCreationForm(
        {"username": fake.user_name(), "password1": test_pw, "password2": test_pw}
    )
    if form.is_valid():
        form.save()
        return "User created"
    return form.errors


def drop_all_data():
    pass

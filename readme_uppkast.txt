SETUP:

environment:
python -m venv venv
bash: source <venv>/bin/activate
cmd: C:\> <venv>\Scripts\activate.bat
powershell: PS C:\> <venv>\Scripts\Activate.ps1

installa python pökkum:
geri ráð fyrir að séuð búnir að activate-a environmentið og cd-aðir í tm-manager-backend möppuna
pip install -r ./requirements/local.txt

database:
installa postgres (ég er með 11.3)
fara í psql og búa til nýtt database
fylla út env upplýsingar, postgres://user:password@localhost:5432/db
python manage.py migrate


python manage.py createsuperuser

black:
    "[python]": {
        "editor.formatOnSave": true,
    },


python manage.py graph_models -a > ./test.dot

tslint
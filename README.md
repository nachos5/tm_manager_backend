# Info

* **Frontend repo**
  * https://github.com/nachos5/tm_manager_frontend
* **Trello**
  * https://trello.com/b/qrljEtcc/tm-manager
* **Heroku síður** (frí dynos svo gæti verið lengi að initialize-ast):
  * bakendi:
    * https://tmmanagerbackend.herokuapp.com/graphql
  * framendi:
    * https://tmmanagerfrontend.herokuapp.com

# Requirements
* **Python**
  * https://www.python.org/downloads/
* **PostgreSQL**
  * https://www.postgresql.org/download/

# Easy setup (only works on unix)

* Install
```
git clone https://github.com/nachos5/tm_manager_backend.git
cd tm_manager_backend
chmod 744 install.sh start.sh
./install.sh
```

* Start server
```
./start.sh
```

### ./install.sh
* Setur upp alla pakka
* Setur upp database
* Setur upp .env
* Setur random gögn i database

### ./start.sh
* Activate'ar `manage.py` fyrir enviromentið
* Keyrir serverinn

# Setup

## Install

1. Download repo
```
git clone https://github.com/nachos5/tm_manager_backend.git
cd tm_manager_backend
```
2. Set up python environment for the project
```
python3 -m venv venv
```
3. Activate the environment

* Unix/MacOs
```
source venv/bin/activate
```
* Command prompt
```
venv\Scripts\activate.bat
```
* Powershell
```
venv\Scripts\activate.ps1
```
4. Install the python packages
```
pip install -r requirements/local.txt
```
6. Make a **.env** file in the root of the project and put your database url, username and password.
```
echo "DATABASE_URL=postgres://<MY_USERNAME>:<MY_PASSWORD>@localhost:5432/<MY_DATABASE>" > .env
```
8. Manually create a database in postgreSQL
```
createdb -O <MY_USERNAME> <MY_DATABASE>
```
9.  Populate the database with relations
```
python manage.py migrate
```
10. Extra, to create a superuser
```
python manage.py createsuperuser
```

## Start server

1. Activate the environment using **step 3.** from the install above/
2. Run the server
```
python manage.py runserver
```

The server launches at **127.0.0.1:8000**

# Django projects

* Undir config eru Django settings, getið skoðað base.py og local.py en er ekki priority, getið gert það í rólegheitum.

* Mappan *tm_manager_backend* er sú sem þið þurfið að skoða mest, þar eru "öppin". Django project er byggt á "öppum" sem inniheldur oftast einn eða fleiri af þessum file-um (mæli með að skoða tournament appið sem ég setti upp):

  * models.py - hér geymir maður töflurnar, semsagt eftir clössunum er búin til sql create table skipun, en síðan getur maður líka haft 'utils' aðferðir eða slíkt fyrir modelin. T.d. ef þið skoðið *Tournament* modelið sem ég bjó til eru efst django fieldar sem mynda töfluna en fyrir neðan er ýmislegt utils dót. Meta classinn skilgreinir t.d. hvað er default orderingið þegar hlutir eru fetchaðir og svo getur maður bætt við aðferðum sem hægt er að kalla á fyrir hluti. Django docs: https://docs.djangoproject.com/en/2.2/topics/db/models/

  * urls.py og views.py - þetta þarf maður bara fyrir server-side rendering. Hér myndi maður skilgreina urla og fyrir hvern url fetcha hluti og rendera í template, þetta er mjög svipað því sem við vorum að gera með *ejs* í vefforritun 2. Við erum ekki að fara nota þetta þar sem við notum frontend rendering og API en mæli samt með að tékka á þessu (django documentationin eru góð). Er smá server-side rendering í þessu repo-i þar sem ég nennti ekki að cleana það úr þessu template projecti, en í rauninni erum við bara að nota þetta repo fyrir API-inn og þá er eini urlinn sem þið þurfið að nota /graphql (tala um graphql hér neðar).

  * forms.py - django forms býr til form í bakendanum sem maður getur renderað sem html form á frontendanum, er ógeðslega þægilegt dót, sérstaklega með server-side rendering. Maður getur líka notað það með graphql. Tékkiði formin sem ég gerði í Tournaments appinu, er frekar basic.

  * admin.py - prófiði að fara á 127.0.0.1:8000/admin og logga ykkur inn með superusernum. Hér er hægt að bæta við og breyta objectum. Maður registerar model á admin síðuna í admin.py.

  * apps.py - til að 'registera' appið. Þarf svo líka að bæta því við í settings. Tékkiði *LOCAL_APPS* listann í config/settings/base.py.

* **Migrations** - Django býr ekki sjálfkrafa til töflur út frá models.py heldur þarf maður að runa skipunum fyrir það. Þetta virkar þannig að það er geymt 'history' af öllum breytingum undir migrations möppunni fyrir hvert app (viljum alls ekki messa við þessa filea). Í setupinu runnuðu þið **python manage.py migrate**. Það sem gerðist þá er að það var runnað í gegnum alla migrations fileana og databaseið uppdateað útfrá þeim. Þannig að sama þótt þið séuð með tómt database eða nokkrum eða mörgum migrations eftirá er hægt að update-a databaseið með þessari skipun. Ef þið gerið breytingar á fieldum eða bætið við fieldum í models.py þarf að búa til migrations. Þannig að segjum að þið mynduð bæta við t.d. *location* field í Tournament appið þá þyrfti að runa **python manage.py makemigrations** til að búa til migration file og svo **python manage.py migrate** til að apply-a því. Þetta virkar oftast frekar smooth en geta komið upp vesen t.d. þegar verið er að mergea git branches, ég skal díla við það.

* **Shell** - ein besta leiðin til að læra á og testa Django er shellið. Prófiði að runa **python manage.py shell_plus**, plus auto importar modulum sem er mjög þægilegt. Skoðiði svo core/random_data.py fileinn sem ég bjó til. Bjó til fall til að inserta test drasli inn í database-ið, þægilegt til að byrja með. Runniði **generate_initial_data()** í shellinu, ætti þá að inserta einhverju sorpi í databaseið.

* **queries** - eftir að hafa insertað sorpi í databaseið mæli ég með að tékka rétt svo hvernig hlutir eru fetchaðir úr databaseinu. get sækir einn hlut, all og filter marga. Prófiði t.d. í shellinu að gera þetta í röð:
  
  * t = Tournament.objects.get(id=1)
  * t.\_\_dict\_\_
  * t.name

  Svo líka t.d. þetta:

  * c = Category.objects.first()
  * qs = Tournament.objects.filter(category=c)
  * qs

  qs er þá QuerySet sem er sett af objectum. Annars eru fullt af möguleikum, hér eru docs: https://docs.djangoproject.com/en/2.2/ref/models/querysets/


# GraphQL

* Graphql er 'query-api tungumál' sem er að mínu mati snilld. *Graphene* er framework library-ið fyrir það í Python. Fariði á **127.0.0.1:8000/graphql** og í textagluggann paste-iði þessu og ýtið svo á ctrl+enter:

  query {
    tournaments {
      edges {
        node {
          id
          name
        }
      }
    }
  }

  Ættuð þá að fetcha öll tournaments úr databaseinu. Edges er listi af nodes þar sem hvert node er tournament í þessu tilviki. Þið getið svo bætt við eða fjarlægt fielda úr nóðunni. Til að sjá hvaða fieldar og query eru í boði tékkiði docs takkann efst í hægra horninu og ýtið svo á gula Query textann.

* Til að gera hluti aðgengilega í gegnum graphql api-inn þarf að skoða graphql appið/möppuna. Tékkiði fyrst api.py, þetta er root fællinn fyrir api-inn. Tékkið svo graphql/tournament/schema.py, þetta er þá rootið fyrir tournament aðferðirnar. Skiptist upp í **Queries** og **Mutations**. Getið hugsað Queries sem get requests og mutations sem post/patch requests (eða conceptlega séð, annars tæknilega séð eru öll graphql requests post). Svo eru þessir file-ar sem schemað er að referenca:

  * types.py - Skilgreinir object týpur, oftast þurfa þær bara að vera alveg eins og modelið sem þær referenca en líka hægt að bæta við öðrum custom hlutum til að fetcha eins og ég geri t.d. með Tournament týpuna.

  * resolvers.py - fetchar gögn, hægt að setja beint inní schema.py en þægilegt svona fyrir lesanleika.

  * filters.py - hér eru skilgreind filterset sem hægt er að setja á týpur. Prófiði t.d. þetta query: 
  
    query { tournaments(name_Icontains: "a") { edges { node { id name } } } }

    Þá fær maður öll tournaments sem innihalda a í nafninu, i-ið í icontains þýðir ignore case.
  
  * mutations.py - hér eru mutations, þau búa til eða update-a gögn, mér finnst þægilegast að nota DjangoModelFormMutation.

# TASK

## 1. Sukurti Django projektą, naudojantį SQLite duomenų bazę.

## 2. Projekte sukurti tokius modelius:

* User - naudotojas, turintis tokius parametrus:
    * username
    * password
    * permissions
        1. create_book
        2. read_book
        3. update_book
        4. delete_book
        5. administrator
* Book - modelis, atspindintis privačius duomenis. Privalo turėti foreign key į User, bei turėtų turėti kitokius parametrus, apibūdinančius knygą.
* User token - modelis, autentikuojantis prisijungusį naudotoją, Turi turėti token_string bei expiration. Alternatyva: vietoje šio modelio gali naudoti JWT, kuris duomenų bazėje nesaugomas.

## 3. Projekte sukurti tokias funkcijas:

* Registracija. Sukuriamas User, turintis permissions 1-4. User, turintys administrator
permission kuriami tik per Django Admin platformą.
* Prisijungimas. Naudotojas įveda username ir password, ir jeigu jie teisingi, response
grąžinamas token, galiojantis 1 valandą.
* Book ViewSet. Tai Django Rest Framework RESTful ViewSet, palaikantis GET,
POST, PUT, PATCH bei DELETE metodus. ViewSet autentikuojamas user token.
Kiekvienas metodas leidžiamas tik turint atitinkamus permissions (pvz. create_book
POST metodui)
    * Jeigu user neturi administrator permissions, ji gali matyti/valdyti tik savo knygas. Jeigu turi administrator permission, gali gali matyti/valdyti bet kieno knygas
    * GET metodai turi būti dviejų tipų - list bei detail, t.y. `GET books/` bei `GET books/{book-id}/`. List endpoint turėtų būti mažiau informacijos, nei detail. List
endpoint taip pat turėtų turėti:
        1. puslapiavimą - pagal query parametrus `page_number` bei `items_per_page`
        2. filtravimą - paieška pagal knygos pavadinimą (`icontains` filtras) bei filtravimas pagal knygos įkėlimo datą (date_from, date_to). Filtrai taip pat paduodami query parametruose.

## 4. Projektą įkelti į GitHub kaip privatų projektą bei pasidalinti su naudotoju `deitam`, kad galėtume jį matyti.

## TODO

* backend app:
    * ~~User model~~
    * ~~Book model~~
        * ~~Add book cover field~~
* api app:
    * ~~Login handler~~
    * ~~Register handler~~
    * ~~JWT~~
* book app:
    * Book ViewSet:
        * ~~POST~~
        * ~~PUT~~
        * ~~PATCH~~
        * ~~DELETE~~
        * ~~GET detailView~~
        * GET listView:
            * pagination (query and drf)
            * ~~filters (icontains and date_from - date_to)~~
        * ~~auth with token~~
        * permissions
* frontend app:
    * ~~Register form~~
    * ~~Login form~~
    * ~~Dashboard~~
    * ~~Search bar~~
    * Administrator panel
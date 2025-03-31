# Pobieranie danych z PRG do bazy danych PostGIS

## Kroki

1.  **Uruchom serwer PostgreSQL z PostGISem:**

    ```bash
    docker run --name "postgis" --shm-size=4g -e MAINTAINANCE_WORK_MEM=512MB -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=1234 -e POSTGRES_DBNAME=postgres -d -t postgis/postgis
    export PGPASSWORD="1234"
    ```

2.  **Uruchom skrypt do pobrania danych z PRG do bazy danych PostGIS:**

    Uruchom skrypt `prg_to_postgis.py` z katalogu, w którym się znajduje:

    ```bash
    python prg_to_postgis.py
    ```

    * Narzędzie `ogr2ogr` jest wymagane do importowania danych z WFS.
    * Skrypt zawiera logikę pobierania danych z PRG i importowania ich do bazy danych PostGIS.


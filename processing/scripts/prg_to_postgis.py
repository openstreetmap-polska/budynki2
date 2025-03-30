import subprocess

# Dane połączenia z bazą PostGIS
db_host = "0.0.0.0"
db_port = "5432"
db_name = "postgres"
db_user = "postgres"
db_password = "1234"
record_limit = 100

# URL WFS z parametrami STARTINDEX i COUNT
wfs_url = f"https://mapy.geoportal.gov.pl/wss/ext/KrajowaIntegracjaNumeracjiAdresowej?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=ms:prg-adresy&STARTINDEX=0&COUNT={record_limit}"

# Nazwa tabeli w PostGIS
table_name = "prg_adresy"

# Ciąg połączenia z PostGIS
connection_string = f"PG:host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password}"

# Polecenie ogr2ogr
ogr2ogr_command = [
    "ogr2ogr",
    "-f", "PostgreSQL",
    connection_string,
    wfs_url,
    "-nln", table_name,
    "-overwrite",
    "-forceNullable" # For some reason the data from GUGiK had gml_id='.1'
]

subprocess.run(ogr2ogr_command, check=True)
print(f"Succesfully imported {record_limit} records from PRG to PostGIS.")

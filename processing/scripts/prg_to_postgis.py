import subprocess
import click
import tempfile
import requests

@click.command()
@click.option('--db-host', default="0.0.0.0", help='PostGIS database host', show_default=True)
@click.option('--db-port', default="5432", help='PostGIS database port', show_default=True)
@click.option('--db-name', default="postgres", help='PostGIS database name', show_default=True)
@click.option('--db-user', default="postgres", help='PostGIS database user', show_default=True)
@click.option('--db-password', default="1234", help='PostGIS database password', show_default=True)
@click.option('--record-limit', default=1000, help='Number of records to import', show_default=True, type=int)
@click.option('--record-batch', default=100, help='Number of records to import in a single batch', show_default=True, type=int)
@click.option('--table-name', default="prg_adresy", help='PostGIS table name', show_default=True)
@click.option('--wfs-url', default="https://mapy.geoportal.gov.pl/wss/ext/KrajowaIntegracjaNumeracjiAdresowej?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=ms:prg-adresy&SRSNAME=urn:ogc:def:crs:EPSG::2180", help='WFS URL', show_default=True)
def import_prg_to_postgis(db_host, db_port, db_name, db_user, db_password, record_limit, record_batch, table_name, wfs_url):
    """
    Imports PRG address data from a WFS service into a PostGIS database.
    """

    connection_string = f"PG:host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password}"
    full_request = f"{wfs_url}&STARTINDEX=0&COUNT={record_limit}"

    click.echo(click.style(f"Connecting to {full_request}", fg="green"))
    r = requests.get(full_request)
    if r.status_code != 200:
        raise Exception(f"Error fetching data from {wfs_url}: {r.status_code}")
    click.echo(click.style(f"Fetched {len(r.text)} bytes of data", fg="green"))

    with tempfile.NamedTemporaryFile(mode="w", suffix=".gml", delete=False) as f:
        f.write(r.text)
        f.flush()
        ogr2ogr_command = [
            "ogr2ogr",
            "-f", "PostgreSQL",
            "-nln", table_name,
            "-overwrite",
            "-forceNullable",
            connection_string,
            f.name
        ]
        try:
            subprocess.run(ogr2ogr_command, check=True)
            click.echo(click.style(f"Imported {record_limit} records into {db_host}:{db_port}/{db_name}.{table_name}", fg="green"))
        except subprocess.CalledProcessError as e:
            click.echo(click.style(f"Error importing data: {str(e)}", fg="red"))


if __name__ == "__main__":
    import_prg_to_postgis()

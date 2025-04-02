import subprocess
import click

@click.command()
@click.option('--db-host', default="0.0.0.0", help='PostGIS database host', show_default=True)
@click.option('--db-port', default="5432", help='PostGIS database port', show_default=True)
@click.option('--db-name', default="postgres", help='PostGIS database name', show_default=True)
@click.option('--db-user', default="postgres", help='PostGIS database user', show_default=True)
@click.option('--db-password', default="1234", help='PostGIS database password', show_default=True)
@click.option('--record-limit', default=1000, help='Number of records to import', show_default=True, type=int)
@click.option('--record-batch', default=100, help='Number of records to import in a single batch', show_default=True, type=int)
@click.option('--table-name', default="prg_adresy", help='PostGIS table name', show_default=True)
@click.option('--wfs-url', default="https://mapy.geoportal.gov.pl/wss/ext/KrajowaIntegracjaNumeracjiAdresowej?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=ms:prg-adresy", help='WFS URL', show_default=True)
def import_prg_to_postgis(db_host, db_port, db_name, db_user, db_password, record_limit, record_batch, table_name, wfs_url):
    """
    Imports PRG address data from a WFS service into a PostGIS database.
    """

    connection_string = f"PG:host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password}"
    # full_wfs_url = f"{wfs_url}&STARTINDEX=0&COUNT={record_limit}"
    # full_wfs_url = f"{wfs_url}&BBOX=486671.93941567128058523,637882.46590459416620433,486708.02003817853983492,637916.3392419598530978"

    ogr2ogr_command = [
        "ogr2ogr",
        "-f", "PostgreSQL",
        connection_string,
        f"https://mapy.geoportal.gov.pl/wss/ext/KrajowaIntegracjaNumeracjiAdresowej?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=ms:prg-adresy&TYPENAME=ms:prg-adresy&STARTINDEX=0&COUNT={record_limit}&SRSNAME=urn:ogc:def:crs:EPSG::2180",
        "-nln", table_name,
        "-overwrite",
        "-forceNullable"
    ]

    click.echo(f"Importing {record_limit} records from PRG to PostGIS...")

    try:
        subprocess.run(ogr2ogr_command, check=True)
        click.echo(click.style(f"Successfully imported {record_limit} records from PRG to PostGIS.", fg='green'))
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error importing data: {e}", fg='red'))

if __name__ == "__main__":
    import_prg_to_postgis()

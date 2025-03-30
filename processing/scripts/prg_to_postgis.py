import subprocess
import click

@click.command()
@click.option('--db-host', default="0.0.0.0", help='PostGIS database host')
@click.option('--db-port', default="5432", help='PostGIS database port')
@click.option('--db-name', default="postgres", help='PostGIS database name')
@click.option('--db-user', default="postgres", help='PostGIS database user')
@click.option('--db-password', default="1234", help='PostGIS database password')
@click.option('--record-limit', default=100, help='Number of records to import')
@click.option('--table-name', default="prg_adresy", help='PostGIS table name')
@click.option('--wfs-url', default="https://mapy.geoportal.gov.pl/wss/ext/KrajowaIntegracjaNumeracjiAdresowej?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=ms:prg-adresy", help='WFS URL')
def import_prg_to_postgis(db_host, db_port, db_name, db_user, db_password, record_limit, table_name, wfs_url):
    """
    Imports PRG address data from a WFS service into a PostGIS database.
    """

    connection_string = f"PG:host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password}"
    full_wfs_url = f"{wfs_url}&STARTINDEX=0&COUNT={record_limit}"

    ogr2ogr_command = [
        "ogr2ogr",
        "-f", "PostgreSQL",
        connection_string,
        full_wfs_url,
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

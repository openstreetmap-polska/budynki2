import requests
import subprocess
import click
import os

# download address data from OSM and save to postgis with osm2pgsql

@click.command()
@click.option('--osm_url', default="https://download.geofabrik.de/europe/poland/opolskie-latest.osm.pbf", help='OSM address data URL', type=str)
@click.option('--db_host', default="0.0.0.0", help='PostGIS database host', type=str)
@click.option('--db_port', default=5432, help='PostGIS database port', type=int)
@click.option('--db_name', default="postgres", help='PostGIS database name', type=str)
@click.option('--db_user', default="postgres", help='PostGIS database user', type=str)
@click.option('--db_password', default="1234", help='PostGIS database password', type=str)
@click.option('--cache_size', default=2000, help='Cache MB size limit', type=int)
@click.option('--download_dir', type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True), default=os.getcwd(), help='Directory to download OSM address data')
def download_osm_addres_data(osm_url, db_host, db_port, db_name, db_user, db_password, cache_size, download_dir):
    click.echo(f"Downloading OSM address data...")
    r = requests.get(osm_url)
    output_file_name = 'output.osm.pbf'
    with open(os.path.join(download_dir, output_file_name), 'wb') as f:
        f.write(r.content)
    click.echo(click.style(f"Successfully downloaded OSM address data.", fg='green'))

    click.echo(f"Importing OSM address data to PostGIS...")
    osm2pgsql_command = [
        "osm2pgsql",
        "-d", db_name,
        "-U", db_user,
        "-H", db_host,
        "-P", str(db_port),
        "-s",
        "-C", str(cache_size),
        "-p", db_password,
        output_file_name
    ]
    subprocess.run(osm2pgsql_command, check=True)
    click.echo(click.style(f"Successfully imported OSM address data to PostGIS.", fg='green'))

if __name__ == "__main__":
    download_osm_addres_data()

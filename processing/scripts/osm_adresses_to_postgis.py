import requests
import subprocess
import click
import os
import tempfile

# download address data from a .osm.pdf and save to postgis with osm2pgsql

@click.command()
@click.option('--osm_url', default="https://download.geofabrik.de/europe/poland/opolskie-latest.osm.pbf", help='OSM address data URL', type=str)
@click.option('--db_host', default="0.0.0.0", help='PostGIS database host', type=str)
@click.option('--db_port', default=5432, help='PostGIS database port', type=int)
@click.option('--db_name', default="postgres", help='PostGIS database name', type=str)
@click.option('--db_user', default="postgres", help='PostGIS database user', type=str)
@click.option('--cache_size', default=2000, help='Cache MB size limit', type=int)
def download_osm_addres_data(osm_url, db_host, db_port, db_name, db_user, cache_size):
    """Downloads OSM address data and imports it into PostGIS."""

    # Check if the PGPASSWORD environment variable is set
    if os.environ.get("PGPASSWORD") is None:
        click.echo(click.style("Error: PGPASSWORD environment variable not set.", fg='red'))
        exit(1)

    click.echo(f"Downloading OSM address data...")
    r = requests.get(osm_url)
    r.raise_for_status()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".osm.pbf") as temp_file:
        temp_file.write(r.content)
        temp_file_path = temp_file.name

    click.echo(click.style(f"Successfully downloaded OSM address data to: {temp_file_path}", fg='green'))

    click.echo(f"Importing OSM address data to PostGIS...")
    osm2pgsql_command = [
        "osm2pgsql",
        "-d", db_name,
        "-U", db_user,
        "-H", db_host,
        "-P", str(db_port),
        "-s",
        "-C", str(cache_size),
        temp_file_path,
    ]
    try:
        subprocess.run(osm2pgsql_command, check=True)
        click.echo(click.style(f"Successfully imported OSM address data to PostGIS.", fg='green'))
    except subprocess.CalledProcessError as e:
         click.echo(click.style(f"Error importing OSM data:\n{e}", fg='red'))
    finally:
        os.remove(temp_file_path) # Clean up the temporary file

if __name__ == "__main__":
    download_osm_addres_data()

import subprocess
import click
import os
import tempfile
from pathlib import Path
import requests

@click.command()
@click.option('--osm_url', default="https://download.geofabrik.de/europe/poland/opolskie-latest.osm.pbf", help='URL to a .osm.pbf file', type=str, show_default=True)
@click.option('--db_host', default="0.0.0.0", help='PostGIS database host', type=str, show_default=True)
@click.option('--db_port', default=5432, help='PostGIS database port', type=int, show_default=True)
@click.option('--db_name', default="postgres", help='PostGIS database name', type=str, show_default=True)
@click.option('--db_user', default="postgres", help='PostGIS database user', type=str, show_default=True)
@click.option('--proj_srid', default="2180", help='Projection SRID to load the data in', type=str, show_default=True)
@click.option('--cache_size', default=2000, help='Cache MB size limit', type=int, show_default=True)
@click.option('--style_path', default="adress.style", help='Path to a style file that filters the data to only contain adresses', type=click.Path(exists=True, dir_okay=False, path_type=Path), show_default=True)
def download_osm_addres_data(osm_url, db_host, db_port, db_name, db_user, proj_srid, cache_size, style_path):
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

    click.echo(f"Importing OSM address data to PostGIS with EPSG:{proj_srid}...")
    osm2pgsql_command = [
        "osm2pgsql",
        "-d", db_name,
        "-U", db_user,
        "-H", db_host,
        "-P", str(db_port),
        "-S", str(style_path),
        "-C", str(cache_size),
        "--proj", proj_srid,
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

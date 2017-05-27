import click
import pandas as pd


@click.command()
@click.option('--server_host', default='localhost')
@click.option('--server_port', default='8000')
@click.option('--outdir', default=r'C:\temp')
@click.option('--ticker', default='IWM')
def main(server_host, server_port, outdir, ticker):
    pass

if __name__ == '__main__':
    main()

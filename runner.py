import click
from sstservice import SingleTestHandler


@click.command()
@click.option('--server_host', default='localhost')
@click.option('--server_port', default='8000')
@click.option('--outdir', default=r'C:\temp')
@click.option('--ticker', default='IWM')
def main(server_host, server_port, outdir, ticker):
    sth = SingleTestHandler(server_host, server_port, ticker)
    sth.run_date('20170515')

if __name__ == '__main__':
    main()

import click
from sstservice import SingleTestHandler


@click.command()
@click.option('--server_host', default='localhost')
@click.option('--server_port', default='8000')
@click.option('--outdir', default=r'C:\temp')
@click.option('--ticker', default='IWM')
@click.option('--multiproc')
@click.option('--qt-support')
@click.option('--client')
@click.option('--port')
@click.option('--file')
def main(server_host, server_port, outdir, ticker, multiproc, client, qt_support, port, file):
    sth = SingleTestHandler(server_host, server_port, ticker)
    sth.run_date('20170512')

if __name__ == '__main__':
    main()

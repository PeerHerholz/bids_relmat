import argparse


# define parser to collect required inputs
def get_parser():

    __version__ = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    '_version.py')).read()



    parser = argparse.ArgumentParser(description='A small python package to add Relationship Matrix metadata to BIDS derivatives datasets.')
    parser.add_argument('-v', '--version', action='version',
                        version='bids_relmat version {}'.format(__version__))
    return parser


# define the CLI
def run_bids_relmat():

    # get arguments from parser
    args = get_parser().parse_args()

    # special variable set in the container
    if os.getenv('IS_DOCKER'):
        exec_env = 'singularity'
        cgroup = Path('/proc/1/cgroup')
        if cgroup.exists() and 'docker' in cgroup.read_text():
            exec_env = 'docker'
    else:
        exec_env = 'local'


# run the CLI
if __name__ == "__main__":

    run_bids_relmat()

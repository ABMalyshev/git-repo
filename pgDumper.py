import paramiko
from scp import SCPClient
from datetime import datetime
import sys
import os


def main():
    current_daytime = datetime.strftime(datetime.now(), "%Y.%m.%d.%H:%M")
    source_file = '/tmp/' + 'dump_' + current_daytime + '.sql'

    os.system('pg_dump -Fc > ' + source_file)

    if os.path.exists(source_file):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(os.environ.get("SSH_HOST"), username=os.environ.get("SSH_USER"), password=os.environ.get("SSH_PASSWORD"))

        with SCPClient(ssh_client.get_transport()) as scp:
            scp.put(source_file, sys.argv[1])


if __name__ == '__main__':
    main()
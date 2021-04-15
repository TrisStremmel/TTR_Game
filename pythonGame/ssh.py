import paramiko
import time
import getpass
import gzip
import shutil
import os
import logging

from paramiko import AuthenticationException

host = "intuition.thayer.dartmouth.edu"
port = 22

class ssh:
    def __init__(self, folder, loops, player1Strat, player2Strat, features, username, password):
        self.username = username
        self.password = password
        self.folder = folder
        self.loops = loops
        feat = 'ex' if features == 'extended' else 'lim'
        target = '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/{}/{}/target/'.format(username, folder, features)
        other = '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/{}/{}/other/'.format(username, folder, features)

        logging.basicConfig(level=logging.DEBUG, filename='output_CSVs/{}/{}/log.txt'.format(folder, features))
        filename = 'output_CSVs/{}/{}/target/list.files'.format(folder, features)
        f = open(filename, 'w')
        filename1 = 'output_CSVs/{}/{}/other/list.files'.format(folder, features)
        f1 = open(filename1, 'w')
        for x in range(1, loops+1):
            f.write('TTR_auto/{}/{}/target/{}_{}_{}.csv\n'.format(folder, features, player1Strat, feat, x))
            f1.write('TTR_auto/{}/{}/other/{}_{}_{}.csv\n'.format(folder, features, player2Strat, feat, x))
        f.close()
        f1.close()

        server_ssh = paramiko.SSHClient()
        server_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        server_ssh.connect(host, port, username, password)

        stdin, stdout, stderr = server_ssh.exec_command("/admin/clust report c")

        for line in stdout.readlines()[1:]:
            line = line.split()
            if len(line) == 8:
                node_name = line[0]
                break
        #node_name = 'c-dell-m630-0-7'
        if node_name[:6] != 'c-dell':
            print("all nodes in use, quiting run. I am very sorry.")
            exit(-1)
        node_name = 'c-hp-bl465c-0-6'

        transport = server_ssh.get_transport()
        node_dest = (node_name, port)
        server_dest = (host, port)
        tunnel = transport.open_channel('direct-tcpip', node_dest, server_dest)


        sshConnection = paramiko.SSHClient()
        sshConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(node_name)
        sshConnection.connect(node_name, username=username, password=password, sock=tunnel)

        sftp = sshConnection.open_sftp()

        cdms = ['cd src/C++/DTM/ToyDTMs/TTR_auto', 'mkdir {}'.format(folder), 'cd {}'.format(folder),
                'mkdir {}'.format(features), 'cd {}'.format(features), 'mkdir {}'.format('target'), 'mkdir {}'.format('other')]
        stdin, stdout, stderr = sshConnection.exec_command(';'.join(cdms))
        print('Made ' + str(folder) + ' folder inside TTR_auto')

        sftp.put(
            'dtmFiles/actions.csv',
            target + '/actions.csv')
        sftp.put(
            'dtmFiles/actions.csv',
            other + '/actions.csv')

        sftp.put(
            'dtmFiles/{}/attributes.csv'.format(feat),
            target + '/attributes.csv')
        sftp.put(
            'dtmFiles/{}/attributes.csv'.format(feat),
            other + '/attributes.csv')

        sftp.put(
            'output_CSVs/{}/{}/target/list.files'.format(folder, features),
            target + '/list.files')
        sftp.put(
            'output_CSVs/{}/{}/other/list.files'.format(folder, features),
            other + '/list.files')

        toPrint = 10
        totalCSVs = 0
        for x in range(1, loops + 1):
            totalCSVs += 1
            if toPrint == x:
                print(x, "csvs have been uploaded to intuition.")
                toPrint *= 5
            sftp.put(
                'output_CSVs/{}/{}_{}_{}.csv'.format(folder, player1Strat, feat, x),
                target + '/{}_{}_{}.csv'.format(player1Strat, feat, x))
            sftp.put(
                'output_CSVs/{}/{}_{}_{}.csv'.format(folder, player2Strat, feat, x),
                other + '/{}_{}_{}.csv'.format(player2Strat, feat, x))

        print("All csvs have been uploaded")

        cdms = ['cd src/C++/DTM/ToyDTMs/',
                'python3.8 runRoMDP.py "TTR_auto/{}/{}/target" "TTR_auto/{}/{}/other" "" "" 100 BARON "TTR_auto/{}/{}/output" >& "TTR_auto/{}/{}/RunNotes.txt" &'.format(folder, features, folder, features, folder, features, folder, features)]
                #,"disown -r"]

        if sshConnection.get_transport() is not None:
            if sshConnection.get_transport().is_active():
                try:
                    transport = sshConnection.get_transport()
                    transport.send_ignore()
                    print("still connected")
                except EOFError:
                    print("connection is closed")

        sshConnection.exec_command(';'.join(cdms))

        print('python3.8 runRoMDP.py "TTR_auto/{}/{}/target" "TTR_auto/{}/{}/other" "" "" 100 BARON "TTR_auto/{}/{}/output" >& "TTR_auto/{}/{}/RunNotes.txt" &'.format(folder, features, folder, features, folder, features, folder, features))

        if sshConnection.get_transport() is not None:
            if sshConnection.get_transport().is_active():
                try:
                    transport = sshConnection.get_transport()
                    transport.send_ignore()
                    print("still connected")
                except EOFError:
                    print("connection is closed")

        print("Waiting", totalCSVs/10.0, "seconds to allow for RoMDP to finish running before trying to retrieve results")
        time.sleep(totalCSVs/10.0)

        fileNames = ["res.lst", "RoMDP-BARON.graphml.gz", "RoMDP-BARON.lp", "RoMDP_analytics-BARON.compressed_pickle",
                     "RoMDP_mappings-BARON.csv.gz", "RoMDP_probabilities-BARON.csv.gz", "RoMDP_rewards_BARON.csv.gz",
                     "RoMDP_soln-BARON.csv.gz", "sum.lst", "tim.lst"]

        if sshConnection.get_transport() is not None:
            if sshConnection.get_transport().is_active():
                try:
                    transport = sshConnection.get_transport()
                    transport.send_ignore()
                    print("still connected")
                except EOFError:
                    print("connection is closed")

        try:
            for file in fileNames:
                print(file)
                sftp.get(
                    '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/{}/{}/output-RoMDP-BARON/{}'.format(username, folder, features, file),
                    'output_CSVs/{}/{}/DTM/{}'.format(folder, features, file))
                if file[-2:] == "gz":
                    with gzip.open('output_CSVs/{}/{}/DTM/{}'.format(folder, features, file), 'rb') as f_in:
                        with open('output_CSVs/{}/{}/DTM/{}'.format(folder, features, file[:-3]), 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    os.remove('output_CSVs/{}/{}/DTM/{}'.format(folder, features, file))

            sftp.get(
                    '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/{}/{}/RunNotes.txt'.format(username, folder, features),
                    'output_CSVs/{}/{}/DTM/RunNotes.txt'.format(folder, features))
            sftp.close()
            sshConnection.close()
            server_ssh.close()
        except:
            print("File not found.")
            sftp.close()
            sshConnection.close()
            server_ssh.close()


        #14511110
        #/src/C++/DTM/ToyDTMs/TTR_auto

class test:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def test(self):
        try:
            server_ssh = paramiko.SSHClient()
            server_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            server_ssh.connect(host, port, self.username, self.password)
            server_ssh.close()
            return True
        except AuthenticationException:
            print("Wrong username or password")
            return False

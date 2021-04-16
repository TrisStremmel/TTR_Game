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


class newSSH:

    def __init__(self, folder, loops, player1Strat, player2Strat, featuresList, username, password):
        TTR_auto = '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/'.format(username)
        for features in featuresList:
            feat = 'ex' if features == 'extended' else 'lim' if features == 'limited' else 'hy'
            target = '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/{}/{}/target/'.format(username, folder, features)
            other = '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/{}/{}/other/'.format(username, folder, features)

            # creating list.files for target and other
            filename = 'output_CSVs/{}/{}/target/list.files'.format(folder, features)
            f = open(filename, 'w')
            filename1 = 'output_CSVs/{}/{}/other/list.files'.format(folder, features)
            f1 = open(filename1, 'w')
            for x in range(1, loops + 1):
                f.write('TTR_auto/{}/{}/target/{}_{}_{}.csv\n'.format(folder, features, player1Strat, feat, x))
                f1.write('TTR_auto/{}/{}/other/{}_{}_{}.csv\n'.format(folder, features, player2Strat, feat, x))
            f.close()
            f1.close()

            # adding actions.csv and attributes.csv to the target and other folder
            shutil.copy('dtmFiles/{}/attributes.csv'.format(feat),
                        'output_CSVs/{}/{}/target/attributes.csv'.format(folder, features))
            shutil.copy('dtmFiles/{}/attributes.csv'.format(feat),
                        'output_CSVs/{}/{}/other/attributes.csv'.format(folder, features))
            shutil.copy('dtmFiles/actions.csv', 'output_CSVs/{}/{}/target/actions.csv'.format(folder, features))
            shutil.copy('dtmFiles/actions.csv', 'output_CSVs/{}/{}/other/actions.csv'.format(folder, features))

        time.sleep(5)
        # compress 'folder'
        shutil.make_archive('output_CSVs/{}'.format(folder), 'zip', 'output_CSVs/{}'.format(folder))

        # connect to intuition and a node on it
        logging.basicConfig(level=logging.DEBUG, filename='output_CSVs/{}/log.txt'.format(folder))
        server_ssh, sshConnection, sftp = self.establishConnection(username, password)

        # send the compressed folder to src/C++/DTM/ToyDTMs/TTR_auto location on intuition
        breaker = False
        while not breaker:
            try:
                sftp.put('output_CSVs/{}.zip'.format(folder), '{}/{}.zip'.format(TTR_auto, folder))
                breaker = True
            except Exception as e:
                print(e)
                print("failed to send zipped folder to server.")
        print("zipped folder was uploaded to intuition")

        time.sleep(min(max(loops/25.0, 5), 120))
        # decompress the folder on intuition
        commands = ['cd src/C++/DTM/ToyDTMs/TTR_auto', 'unzip {}.zip -d {}'.format(folder, folder)]
        stdin, stdout, stderr = sshConnection.exec_command(';'.join(commands))
        print('decompressed the folder on intuition')

        # reconnect to intuition then the node if connection is lost
        if not self.stillConnected(sshConnection):
            sftp.close()
            sshConnection.close()
            server_ssh.close()
            server_ssh, sshConnection, sftp = self.establishConnection(username, password)

        time.sleep(min(max(loops/10.0, 5), 240))

        # run romdp
        for features in featuresList:
            # creates folder for RoMDP output results
            os.makedirs("output_CSVs/{}/{}/RoMDP_output".format(folder, features))
            breaker = False
            hasFailed = 1
            while not breaker:
                try:
                    # reconnect to intuition then the node
                    sftp.close()
                    sshConnection.close()
                    server_ssh.close()
                    server_ssh, sshConnection, sftp = self.establishConnection(username, password)

                    commands = ['cd src/C++/DTM/ToyDTMs/',
                                'python3.8 runRoMDP.py "TTR_auto/{}/{}/target" "TTR_auto/{}/{}/other" "" "" 100 BARON '
                                '"TTR_auto/{}/{}/output" >& "TTR_auto/{}/{}/RunNotes.txt" &'.format(folder, features,
                                                                                                    folder, features,
                                                                                                    folder, features,
                                                                                                    folder, features)]
                    stdin, stdout, stderr = sshConnection.exec_command(';'.join(commands))
                    # print('stdin, stdout, stderr:', stderr)
                    print('python3.8 runRoMDP.py "TTR_auto/{}/{}/target" "TTR_auto/{}/{}/other" "" "" 100 BARON '
                          '"TTR_auto/{}/{}/output" >& "TTR_auto/{}/{}/RunNotes.txt" &'.format(folder, features,
                                                                                              folder, features, folder,
                                                                                              features, folder, features))
                    print("Waiting", min(max(int(loops/30.0), 5), 3600)*hasFailed,
                          "seconds to allow for RoMDP to finish running before trying to retrieve results")
                    #change the 3600 to 600 after I know that 10k can run faster then 1hr
                    time.sleep(min(max(int(loops/30.0), 5), 3600)*hasFailed)

                    # retrieve dtm output files
                    fileNames = ["res.lst", "RoMDP-BARON.graphml.gz", "RoMDP-BARON.lp",
                                 "RoMDP_analytics-BARON.compressed_pickle",
                                 "RoMDP_mappings-BARON.csv.gz", "RoMDP_probabilities-BARON.csv.gz",
                                 "RoMDP_rewards_BARON.csv.gz",
                                 "RoMDP_soln-BARON.csv.gz", "sum.lst", "tim.lst"]

                    # reconnect to intuition then the node if connection is lost
                    if not self.stillConnected(sshConnection):
                        sftp.close()
                        sshConnection.close()
                        server_ssh.close()
                        server_ssh, sshConnection, sftp = self.establishConnection(username, password)

                    print("retrieving file:", end=' ')
                    for file in fileNames:
                        print(file, end=', ')
                        sftp.get(
                            '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/{}/{}/output-RoMDP-BARON/{}'.format(username, folder,
                                                                                                       features, file),
                            'output_CSVs/{}/{}/RoMDP_output/{}'.format(folder, features, file))
                        if file[-2:] == "gz":
                            with gzip.open('output_CSVs/{}/{}/RoMDP_output/{}'.format(folder, features, file), 'rb') as f_in:
                                with open('output_CSVs/{}/{}/RoMDP_output/{}'.format(folder, features, file[:-3]), 'wb') as f_out:
                                    shutil.copyfileobj(f_in, f_out)
                            os.remove('output_CSVs/{}/{}/RoMDP_output/{}'.format(folder, features, file))
                    print('RunNotes.txt')
                    sftp.get(
                        '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/{}/{}/RunNotes.txt'.format(username, folder, features),
                        'output_CSVs/{}/{}/RoMDP_output/RunNotes.txt'.format(folder, features))
                    print("All files retrieved")
                    breaker = True
                except Exception as e:
                    print(e)
                    print('failed to generated RoMDP or retrieve its files, trying again...')
                    hasFailed = 2

        # reconnect to intuition then the node if connection is lost
        if not self.stillConnected(sshConnection):
            sftp.close()
            sshConnection.close()
            server_ssh.close()
            server_ssh, sshConnection, sftp = self.establishConnection(username, password)


        '''I want to keep a record of all files for testing and checking for now
        # delete the compressed folder from intuition
        commands = ['cd src/C++/DTM/ToyDTMs/TTR_auto', 'rm {}.zip'.format(folder)]
        stdin, stdout, stderr = sshConnection.exec_command(';'.join(commands))
        # print('stdin, stdout, stderr:', stderr)

        # delete the compressed folder from local
        os.remove('output_CSVs/{}.zip'.format(folder))
        '''
        sftp.close()
        sshConnection.close()
        server_ssh.close()
        # celebrate




        # 14511110
        # /src/C++/DTM/ToyDTMs/TTR_auto

    def establishConnection(self, username, password):
        server_ssh = paramiko.SSHClient()
        server_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        server_ssh.connect(host, port, username, password)

        stdin, stdout, stderr = server_ssh.exec_command("/admin/clust report c")

        # finding a node that is free
        node_name = None
        for line in stdout.readlines()[1:]:
            line = line.split()
            if len(line) == 8 and line[1] == 'Up':
                node_name = line[0]
                break

        # if there are no free nodes- quit
        if node_name is None:  # [:6] != 'c-dell':
            print("all nodes in use, quiting run. I am very sorry.")
            exit(-1)

        transport = server_ssh.get_transport()
        node_dest = (node_name, port)
        server_dest = (host, port)
        tunnel = transport.open_channel('direct-tcpip', node_dest, server_dest)

        sshConnection = paramiko.SSHClient()
        sshConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("Connected to node:", node_name)
        sshConnection.connect(node_name, username=username, password=password, sock=tunnel)

        sftp = sshConnection.open_sftp()

        return server_ssh, sshConnection, sftp

    def stillConnected(self, sshConnection):
        if sshConnection.get_transport() is not None:
            if sshConnection.get_transport().is_active():
                try:
                    transport = sshConnection.get_transport()
                    transport.send_ignore()
                    print("still connected")
                    return True
                except EOFError:
                    print("connection is lost")
                    return False
        print("connection is lost")
        return False


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

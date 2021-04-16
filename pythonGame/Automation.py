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

#uncomment line at bottom to run this file stand alone

class Automation:

    @staticmethod
    def TTRAutomation(csvCount, username, password, folder, featuresList, player1Strat, player2Strat):

        for features in featuresList:
            feat = 'ex' if features == 'extended' else 'lim' if features == 'limited' else 'hy'
            target = '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/{}/{}/target/'.format(username, folder, features)
            other = '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/{}/{}/other/'.format(username, folder, features)

            # creating list.files for target and other
            filename = 'output_CSVs/{}/{}/target/list.files'.format(folder, features)
            f = open(filename, 'w')
            filename1 = 'output_CSVs/{}/{}/other/list.files'.format(folder, features)
            f1 = open(filename1, 'w')
            for x in range(1, csvCount + 1):
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

        print("Finished generating local files.")

        failCount = 1.0  # it is used as a wait multiplier.
        breaker = False
        while not breaker:
            try:
                if failCount > 1:
                    for feature in featuresList:
                        Automation.deletePossibleDuplicateLocal(folder, 'output_CSVs/', feature)
                    Automation.deletePossibleDuplicateRemote(csvCount, username, password, folder, 'TTR_auto')

                Automation.compress_send_decompress(failCount, csvCount, username, password, folder,
                                                   'TTR_auto', 'output_CSVs/')
                for feature in featuresList:
                    Automation.runRoMDP(failCount, csvCount, username, password, folder + '/' + feature,
                                       'TTR_auto', 'output_CSVs/')
                    Automation.retrieveRoMDPResults(username, password, folder + '/' + feature,
                                                   'TTR_auto', 'output_CSVs/')

                breaker = True
                Automation.deleteCompressedFolderLocal(folder, 'output_CSVs/')
                Automation.deleteCompressedFolderRemote(csvCount, username, password, folder, 'TTR_auto', 'output_CSVs/')

            except Exception as e:
                print(e)
                failCount += .5
                print("This is failure number:", (failCount-1)*2)

    @staticmethod
    def generalAutomation():
        target = True
        translator = {'yes': True, 'no': False}
        other = translator[input("Do you have an other folder? ")]
        synTarget = translator[input("Do you have an synTarget folder? ")]
        synOther = translator[input("Do you have an synOther folder? ")]
        csvCount = int(input("How many csvs do you have? "))

        username = ''
        password = ''
        check = False
        while not check:
            username = input("Enter intuition username: ")
            password = getpass.getpass("Enter intuition password: ")
            if Test(username, password).test():
                check = True
        folder = input("Enter the name of the folder to upload (must be exact): ")
        remoteFolder = input("Enter the name of the folder you made on intuition inside "
                             "ToyDTMs where this will generate: ")

        localPath = input("Enter the path the the folder to upload (leave blank and hit enter if you called this "
                          "file is in the same directory as that folder [end it with a /]): ")


        failCount = 1.0  # it is used as a wait multiplier.
        breaker = False
        while not breaker:
            time.sleep(1)
            try:
                if failCount > 1:
                    Automation.deletePossibleDuplicateLocal(folder, localPath)
                    Automation.deletePossibleDuplicateRemote(csvCount, username, password, folder, remoteFolder)

                Automation.compress_send_decompress(failCount, csvCount, username, password, folder,
                                                   remoteFolder, localPath)
                Automation.runRoMDP(failCount, csvCount, username, password, folder, remoteFolder, localPath,
                                   target, other, synTarget, synOther)

                Automation.retrieveRoMDPResults(username, password, folder, remoteFolder, localPath)
                breaker = True
            except Exception as e:
                print(e)
                failCount += .5
                print("This is failure number:", (failCount - 1) * 2)

    @staticmethod
    def compress_send_decompress(failCount, csvCount, username, password, folder, remoteFolder, localPath):

        # zip the file locally
        shutil.make_archive('{}{}'.format(localPath, folder), 'zip', '{}{}'.format(localPath, folder))

        remotePath = '/home/{}/src/C++/DTM/ToyDTMs/{}/'.format(username, remoteFolder)

        # connect to intuition and a node on it
        server_ssh, sshConnection, sftp = Automation.establishConnection(username, password)

        # send the compressed <folder> to src/C++/DTM/ToyDTMs/<remotePath> location on intuition
        sftp.put('{}{}.zip'.format(localPath, folder), '{}{}.zip'.format(remotePath, folder))

        waitAmount = min(max(csvCount / 25.0, 5), 120) * failCount
        print("Waiting", waitAmount, "seconds while uploading zipped folder to intuition...")
        time.sleep(waitAmount)

        # decompress the <folder> on intuition
        commands = ['cd {}'.format(remotePath), 'unzip {}.zip -d {}'.format(folder, folder)]
        stdin, stdout, stderr = sshConnection.exec_command(';'.join(commands))

        waitAmount = min(max(csvCount / 10.0, 5), 240)
        print("Waiting", waitAmount, "seconds while decompressing the folder on intuition...")
        time.sleep(waitAmount)

        sftp.close()
        sshConnection.close()
        server_ssh.close()

    #also gets results and sends to local
    @staticmethod
    def runRoMDP(failCount, csvCount, username, password, folder, remoteFolder, localPath, target=True, other=True,
                 synTarget=False, synOther=False):

        os.makedirs("{}{}/RoMDP_output".format(localPath, folder))  # creates folder for RoMDP output results

        # connect to intuition then the node
        server_ssh, sshConnection, sftp = Automation.establishConnection(username, password)

        RoMDPCommand = Automation.buildRoMDPCall(remoteFolder+'/'+folder, target, other, synTarget, synOther)

        commands = ['cd src/C++/DTM/ToyDTMs/', RoMDPCommand]

        stdin, stdout, stderr = sshConnection.exec_command(';'.join(commands))
        # print('stdin, stdout, stderr:', stderr)
        print("The command used to run the RoMDP:\n" + RoMDPCommand, end="\n\n")

        waitAmount = min(max(int(csvCount / 30.0), 5), 3600) * failCount
        print("Waiting", waitAmount,
              "seconds to allow for RoMDP to finish running before trying to retrieve results...")
        # change the 3600 to 600 after I know that 10k can run faster then 1hr
        time.sleep(waitAmount)

        sftp.close()
        sshConnection.close()
        server_ssh.close()

    @staticmethod
    def retrieveRoMDPResults(username, password, folder, remoteFolder, localPath):
        # retrieve output files
        fileNames = ["res.lst", "RoMDP-BARON.graphml.gz", "RoMDP-BARON.lp",
                     "RoMDP_analytics-BARON.compressed_pickle",
                     "RoMDP_mappings-BARON.csv.gz", "RoMDP_probabilities-BARON.csv.gz",
                     "RoMDP_rewards_BARON.csv.gz",
                     "RoMDP_soln-BARON.csv.gz", "sum.lst", "tim.lst"]

        # reconnect to intuition then the node
        server_ssh, sshConnection, sftp = Automation.establishConnection(username, password)

        remotePath = '/home/{}/src/C++/DTM/ToyDTMs/{}/'.format(username, remoteFolder)
        print("retrieving file:", end=' ')
        for file in fileNames:
            print(file, end=', ')
            sftp.get(
                '{}/{}/output-RoMDP-BARON/{}'.format(remotePath, folder, file),
                '{}/{}/RoMDP_output/{}'.format(localPath, folder, file))
            if file[-2:] == "gz":
                with gzip.open('{}/{}/RoMDP_output/{}'.format(localPath, folder, file), 'rb') as f_in:
                    with open('{}/{}/RoMDP_output/{}'.format(localPath, folder, file[:-3]), 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove('{}/{}/RoMDP_output/{}'.format(localPath, folder, file))
        print('RunNotes.txt')
        sftp.get(
            '{}/{}/RunNotes.txt'.format(remotePath, folder),
            '{}/{}/RoMDP_output/RunNotes.txt'.format(localPath, folder))
        print("All files retrieved")

        sftp.close()
        sshConnection.close()
        server_ssh.close()

    @staticmethod
    def deletePossibleDuplicateLocal(folder, localPath, feature=''):
        path = "{}{}{}/RoMDP_output".format(localPath, folder, feature)
        # deletes the RoMDP_output folder and its contents if it already exists.
        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except OSError as e:
                print("Error: %s : %s" % (path, e.strerror))

        Automation.deleteCompressedFolderLocal(folder, localPath)

    @staticmethod
    def deletePossibleDuplicateRemote(csvCount, username, password, folder, remoteFolder):
        server_ssh, sshConnection, sftp = Automation.establishConnection(username, password)

        # delete the <folder> from intuition so it can work from scratch
        commands = ['cd src/C++/DTM/ToyDTMs/{}'.format(remoteFolder), 'rm -r {}'.format(folder)]
        stdin, stdout, stderr = sshConnection.exec_command(';'.join(commands))
        # print('stdin, stdout, stderr:', stderr)

        waitAmount = min(max(int(csvCount / 50.0), 5), 240)
        print("Waiting", waitAmount, "seconds to allow for possible duplicate files to be removed from intuition...")
        time.sleep(waitAmount)

        sftp.close()
        sshConnection.close()
        server_ssh.close()

        Automation.deleteCompressedFolderRemote(csvCount, username, password, folder, remoteFolder)

    @staticmethod
    def deleteCompressedFolderRemote(csvCount, username, password, folder, remoteFolder, localPath):

        server_ssh, sshConnection, sftp = Automation.establishConnection(username, password)

        #I want to keep a record of all files for testing and checking for now
        # delete the compressed folder from intuition
        commands = ['cd src/C++/DTM/ToyDTMs/{}'.format(remoteFolder), 'rm {}.zip'.format(folder)]
        stdin, stdout, stderr = sshConnection.exec_command(';'.join(commands))
        # print('stdin, stdout, stderr:', stderr)

        waitAmount = min(max(int(csvCount / 100.0), 5), 120)
        print("Waiting", waitAmount, "more seconds to allow for possible duplicate files to be removed from intuition...")
        time.sleep(waitAmount)

        sftp.close()
        sshConnection.close()
        server_ssh.close()

    @staticmethod
    def deleteCompressedFolderLocal(folder, localPath):
        try:
            # delete the compressed folder from local if it exists
            path = '{}{}.zip'.format(localPath, folder)
            if os.path.isfile(path):
                os.remove(path)
        except FileNotFoundError as e:
            print(e)
            print("Failed to delete local zip folder, it likely did not exits.")

    @staticmethod
    def buildRoMDPCall(remotePath, target, other, synTarget, synOther, rewardNum=100):
        command = 'python3.8 runRoMDP.py '
        command += '"{}/target" '.format(remotePath) if target else '"" '
        command += '"{}/other" '.format(remotePath) if other else '"" '
        command += '"{}/synTarget" '.format(remotePath) if synTarget else '"" '
        command += '"{}/synOther" '.format(remotePath) if synOther else '"" '
        command += '{} BARON "{}/output" >& "{}/RunNotes.txt" &'.format(rewardNum, remotePath, remotePath)
        return command

    @staticmethod
    def establishConnection(username, password):
        try:
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

            # if there are no free nodes so quit
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

        except Exception as e:
            print(e)
            print('unable to connect to intuition')
            exit(-1)



    @staticmethod
    def stillConnected(sshConnection):
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

class Test:
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

#uncomment the bellow line to run general automation
#Automation.generalAutomation()

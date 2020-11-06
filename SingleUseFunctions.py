import mysql.connector
import paramiko
import os


#Create CSV labels from paths
#Path tuple
def create_CSV(path,dst):
    with open(dst,'w') as f:
        f.write("id,label\n")
        for i,fname in enumerate(path):
            fil = fname[0]
            fil = os.path.basename(os.path.normpath(fil))
            f.write("{},{}\n".format(fil.replace('.jpg',''),fil[0:4]))


def get_Data(images,sftp,dest):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dest = os.path.join(dir_path,dest)
    if not os.path.exists(dest):
        os.mkdir(dest)
    for image in images:
        fname = os.path.basename(os.path.normpath(image[0]))
        if not os.path.exists(os.path.join(dest,fname)):
            sftp.get(image[0],os.path.join(dest,fname))


def main():
    mydb = mysql.connector.connect(
    host="10.8.0.1",
    user="kacper",
    password="5fUwXohpL6rh5xvK",
    database="baza_do_nauki"
    )
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.8.0.1", 22, "kacper", "5fUwXohpL6rh5xvK")
    sftp = ssh.open_sftp()

    mycursor = mydb.cursor()
    mycursor.execute("SELECT sciezka FROM znaki")
    images = mycursor.fetchall()

    create_CSV(images,"TrainLabels.csv")
    #get_Data(images[0:round(len(images) * 0.02)],sftp,"TrainData")
    #get_Data(images[round(len(images) * 0.02):round(len(images) * 0.025)],sftp,"ValidationData")

    sftp.close()
    ssh.close()


if __name__ == "__main__":
    main()
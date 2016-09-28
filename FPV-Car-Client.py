import socket

def Main():
    host = '127.0.0.1'
    port = 5000

    mySocket = socket.socket()
    mySocket.connect((host,port))
    move_list = []

    while True:
        data = mySocket.recv(1024).decode()

        move_list = str(data).split()

        N1 = move_list[len(move_list)-2]
        N2 = move_list[len(move_list)-1]

        lor = float(N2)
        fab = float(N1)

        if lor < -0.3:
            print("Left")
        if lor > 0.3:
            print("Right")
        if lor > -0.3 and lor < 0.3:
            print("Straight")


        if fab == -1:
            print("Backwards")
        if fab == 0:
            print("Idle")
        if fab == 1:
            print("Forwards")





if __name__ == '__main__':
    Main()

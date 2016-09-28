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

        


        if fab == -1:
            print("Backwards")
        elif fab == 1:
            print("Forwards")
        else:
            print("Idle")

        if lor < -0.3:
            print("Left")
        elif lor > 0.3:
            print("Right")
        else:
            print("Straight")


try:
if __name__ == '__main__':
    Main()

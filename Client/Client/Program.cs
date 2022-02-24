using System.Net.Sockets;
using System.Text;



class Program
{
    static void Main(string[] args)
    {
        if (args.Length != 3)
        {
            Console.WriteLine("Please run the Client with the nickname, address and port as arguments.");
        }
        else
        {
            Client myClient = new Client(args[0], args[1], int.Parse(args[2]));
        }
    }
}

public class Client
{
    private string    nickname;
    private TcpClient clientSocket;
    
    private Thread    receiveThread;
    private Thread    sendThread;
    private Thread    logInThread;

    private NetworkStream serverStream;
    int bufferSize = 1024;

    public Client(string name, string ip, int port)
    {
        clientSocket = new TcpClient();
        clientSocket.Connect(ip, port);
        serverStream = clientSocket.GetStream();

        nickname = name;
        
        LogIn();
    }
 
    /// <summary>
    /// Log into the server with the given nickname
    /// </summary>
    void LogIn()
    {
        // Send the Client nickname to the server
        SendMsg(nickname);

        // Get the server response. 
        // Server response are filled with \0 to fill the buffer
        string returndata = ReadSocket().Replace("\0", string.Empty);
        Console.WriteLine("@server: " + returndata);

        if (returndata != "Connected to server!")
        {
            ExitChat();
        }
        else
        {
            try
            {
                // Start threading
                receiveThread = new Thread(new ThreadStart(getMessage));
                receiveThread.Start();

                sendThread = new Thread(new ThreadStart(Chat));
                sendThread.Start();
            }
            catch (Exception e)
            {
                Console.Out.WriteLine("Error on threading " + e);
            }

        }
    }

    /// <summary>
    /// Get message from the server and print it
    /// </summary>
    private void getMessage()
    {
        while (true)
        {
            Console.WriteLine(ReadSocket());
        }
    }

    /// <summary>
    /// Allow the client to write and send message to the server
    /// </summary>
    void Chat()
    {
        string? menssage = null;
        while (menssage != "/exit")
        {
            while (menssage == null)
            {
                menssage = Console.ReadLine();
            }
            SendMsg(menssage);
            menssage = null;
        }
        ExitChat();
    }

    /// <summary>
    /// Send a message to the server
    /// </summary>
    /// <param name="msg">message to send</param>
    void SendMsg(string msg)
    {
        if (clientSocket == null) return;

        try
        {
            byte[] buffer = new byte[bufferSize];
            buffer = Encoding.ASCII.GetBytes(msg);
            serverStream.Write(buffer, 0, buffer.Length);
        }
        catch (SocketException socketException)
        {
            Console.Out.WriteLine("Socket exception: " + socketException);
        }
    }

    /// <summary>
    /// Read from socket
    /// </summary>
    /// <returns>socket data converted into ASCII string</returns>
    private string ReadSocket()
    {
        byte[] buffer = new byte[bufferSize];
        serverStream.Read(buffer, 0, buffer.Length);
        string response = Encoding.ASCII.GetString(buffer);
        return response;
    }

    /// <summary>
    /// Close threads and connection to the server
    /// </summary>
    void ExitChat()
    {
        receiveThread.Abort();
        logInThread.Abort();
        serverStream.Close();
        clientSocket.Close();
    }
}

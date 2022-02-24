# Chat Server

This repository contains an attempt at chat room.

The server is written in Python and the client in C#.

## Usage

The server must first be launched. 
```bash
python Server/Server/Server.py --help
```
Example:
```bash
python Server/Server/Server.py --address 127.0.0.1 --port 8080
```
Compile the client using a c# compiler (or open the Visual Studio project and compile from the IDE).

Open as many instances of the client as you want. You must pass as arguments the user's nickname, server address and port.

Example:
```bash
Client.exe fulanito 127.0.0.1 8080
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
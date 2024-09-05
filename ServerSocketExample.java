import java.io.*;
import java.net.*;

class ServerSocketExample {
    public static void main(String[] argv) {
        try {
            int port = 7777;
            ServerSocket serverSocket = new ServerSocket(port);
            while (true) {
                Socket socket = serverSocket.accept();
                System.out.println("Cliente conectado.");
                InputStream inputStream = socket.getInputStream();
                DataInputStream dataInputStream = new DataInputStream(inputStream);
                DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());

                int command = dataInputStream.readInt();

                switch (command) {
                    case 1:
                        String imageName = dataInputStream.readUTF();
                        ByteArrayOutputStream buffer = new ByteArrayOutputStream();

                        int nRead;
                        byte[] data = new byte[1024];
                        while ((nRead = inputStream.read(data, 0, data.length)) != -1) {
                            buffer.write(data, 0, nRead);
                        }
                        buffer.flush();

                        byte[] imageData = buffer.toByteArray();

                        FileOutputStream outputStream = new FileOutputStream("Images/" + imageName);
                        outputStream.write(imageData);

                        System.out.println("Imagem recebida e salva com sucesso.");
                        outputStream.close();
                        break;

                    case 2:
                        File directory = new File("Images");
                        if (directory.exists() && directory.isDirectory()) {
                            String[] files = directory.list();
                            if (files != null) {
                                dataOutputStream.writeInt(files.length);
                                for (String fileName : files) {
                                    dataOutputStream.writeUTF(fileName);
                                }
                            }
                        } else {
                            dataOutputStream.writeInt(0);
                        }
                        dataOutputStream.flush();
                        break;

                    default:
                        System.out.println("Comando inválido.");
                        break;
                }

                inputStream.close();
                socket.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

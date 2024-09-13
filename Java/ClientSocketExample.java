import java.io.DataOutputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Scanner;

public class ClientSocketExample {
    public static void main(String[] args) {
        try {
            InetAddress host = InetAddress.getLocalHost();
            Socket socket = new Socket(host.getHostName(), 7777);
            OutputStream outputStream = socket.getOutputStream();
            DataOutputStream dataOutputStream = new DataOutputStream(outputStream);
            DataInputStream dataInputStream = new DataInputStream(socket.getInputStream());
            Scanner input = new Scanner(System.in);

            boolean loop = true;
            while (loop) {
                System.out.println("\nSelecione um comando:");
                System.out.println("1 - Enviar imagem");
                System.out.println("2 - Listar imagens salvas");
                System.out.println("3 - Finalizar");

                int command = input.nextInt();
                input.nextLine();

                switch (command) {
                    case 1:
                        dataOutputStream.writeInt(1);
                        String imageName;
                        System.out.print("Imagem a ser enviada: ");
                        imageName = input.nextLine();
                        byte[] imageData = Files.readAllBytes(Paths.get("src/" + imageName));
                        dataOutputStream.writeUTF(imageName);
                        outputStream.write(imageData);
                        outputStream.flush();
                        System.out.println("Imagem enviada com sucesso.");
                        break;

                    case 2:
                        dataOutputStream.writeInt(2);
                        int fileCount = dataInputStream.readInt();
                        if (fileCount > 0) {
                            System.out.println("Imagens salvas:");
                            for (int i = 0; i < fileCount; i++) {
                                String fileName = dataInputStream.readUTF();
                                System.out.println(fileName);
                            }
                        } else {
                            System.out.println("Nenhuma imagem encontrada.");
                        }
                        break;

                    case 3:
                        loop = false;
                        break;

                    default:
                        System.out.println("Comando inválido.");
                        break;
                }
            }

            input.close();
            outputStream.close();
            dataOutputStream.close();
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

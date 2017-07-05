import java.io.*;
import java.net.*;

//This class contains methods to download apks from a list of URL, we used this class to crawl the FDroid Market
public class FDroidCrawler {
    final static int size = 1024;
	
    public static void fileUrl(String fAddress, String localFileName, String destinationDir) {
        OutputStream outStream = null;
        URLConnection uCon = null;

        InputStream is = null;
        try {
            URL url;
            byte[] buf;
            int byteRead, byteWritten = 0;
            url = new URL(fAddress);
            outStream = new BufferedOutputStream(new FileOutputStream(destinationDir + "\\" + localFileName));

            uCon = url.openConnection();
            is = uCon.getInputStream();
            buf = new byte[size];
            while ((byteRead = is.read(buf)) != -1) {
                outStream.write(buf, 0, byteRead);
                byteWritten += byteRead;
            }
            System.out.println("Downloaded Successfully.");
            System.out.println("File name:\"" + localFileName + "\"\nNo ofbytes :" + byteWritten);
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                is.close();
                outStream.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public static void fileDownload(String fAddress, String destinationDir) {
        int slashIndex = fAddress.lastIndexOf('/');
        int periodIndex = fAddress.lastIndexOf('.');

        String fileName = fAddress.substring(slashIndex + 1);

        if (periodIndex >= 1 && slashIndex >= 0 && slashIndex < fAddress.length() - 1) {
            fileUrl(fAddress, fileName, destinationDir);
        } else {
            System.err.println("path or file name.");
        }
    }

    public static void main(String[] args) {
        if (args.length == 2) {
            for (int i = 1; i < args.length; i++) {
                fileDownload(args[i], args[0]);
            }
        } else {
        }
    }
}

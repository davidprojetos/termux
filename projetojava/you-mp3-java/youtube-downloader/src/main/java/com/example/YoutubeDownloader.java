import com.sapher.youtubedl.YoutubeDL;
import com.sapher.youtubedl.YoutubeDLException;
import com.sapher.youtubedl.YoutubeDLRequest;
import com.sapher.youtubedl.YoutubeDLResponse;

public class YoutubeDownloader {

    public static void main(String[] args) {
        String videoUrl = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";

        YoutubeDLRequest request = new YoutubeDLRequest(videoUrl, "/path/to/download/directory");
        
        try {
            YoutubeDLResponse response = YoutubeDL.execute(request);
            System.out.println("Download completo: " + response.getOut());
        } catch (YoutubeDLException e) {
            e.printStackTrace();
        }
    }
}


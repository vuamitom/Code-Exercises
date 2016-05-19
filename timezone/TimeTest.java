import java.text.SimpleDateFormat;
import java.util.Collection;
import java.util.Date;
import java.util.TimeZone;

public class TimeTest {

    public static void main(String[] args){
       SimpleDateFormat dateFormatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");
       dateFormatter.setTimeZone(TimeZone.getTimeZone("UTC")); 
       SimpleDateFormat dateFormatter2 = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");

       // in Java, timezone is not a property of Date object 
       // rather a formatter's concern 
       // In other words, Date object and its timestamp (ms) is timezone independent. 
       // Need to check with .NET. It's kind of different.
       Date date = new Date();
       System.out.println(dateFormatter.format(date));
       System.out.println(dateFormatter2.format(date));
    }
}

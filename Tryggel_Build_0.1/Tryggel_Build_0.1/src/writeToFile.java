import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.text.SimpleDateFormat;
import java.util.Calendar;

public class writeToFile{
	
	File logFile = new File("Test Results");
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}
	
	public void doWriting(RequestData data)
	{
		
		BufferedWriter writer = null;
		
        	try 
        	{
        	
            //Create simple date format
            String timeLog = new SimpleDateFormat("yyyy-MM-dd_HH.mm.ss").format(Calendar.getInstance().getTime());
            
            //***IF YOU NEED TO FIND THE FILE ON YOUR COMPUTER REMOVE "//"***
            // This will output the full path where the file will be written to...
            //System.out.println(logFile.getCanonicalPath());
            
            
            //Write important stuff to file
			writer = new BufferedWriter(new FileWriter(logFile, true));
            writer.newLine();
            writer.write("[" + timeLog + "] ; " + data.getData());
            writer.flush();
            
        	} 
        		catch (Exception e) 
        		{
        			e.printStackTrace();
        		} 
        			finally 
        			{
        				try {
        					// Close the writer regardless of what happens...
        					writer.close();
        					} 
        						catch (Exception e) 
        						{
        						}
        			}
		
	}

}

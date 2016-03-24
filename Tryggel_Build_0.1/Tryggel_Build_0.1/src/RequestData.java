import java.io.IOException;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.ResponseBody;

public class RequestData {
	
public static String Result = null;

	public static void main(String[] args) {
		// TODO Auto-generated method stub
	}
	
	public void update() throws IOException
	{
		
		//THIS GETS THE DATA FROM THE SMART METER
		
		OkHttpClient client = new OkHttpClient();
		Request request = new Request.Builder()
		  .url("https://stagingapi.eon.se/eonapi/ODataProvider.svc/KwStreamLive(0)")
		  .get()
		  .addHeader("content-type", "application/json")
		  .addHeader("accept", "application/json")
		  .addHeader("authorization", "Mi45MTExOkVvbnN2ZXJpZ2Ux")
		  .addHeader("cache-control", "no-cache")
		  .addHeader("postman-token", "dcc584a3-99a6-e97d-f995-2695551f26bd")
		  .build();

		Response response = client.newCall(request).execute();
		
		ResponseBody r = response.body();
		String result = r.string();
		this.cleanData(result);
		
	}
	
	public void setData(String data){	
		Result = data;
	}
	public String getData()
	{
		return Result;
	}
	public void cleanData(String str)
	{
		
		 String[] rawData = str.split(",");
		 
		 String[] cleanedData = rawData[2].split(":");
		
		 cleanedData[1] = cleanedData[1].substring(1, cleanedData[1].length());
		//String cleanedData = null;
		
		/*
		
		if (cleanedData[6] != null && cleanedData[6].length() > 0 && cleanedData[6].charAt(cleanedData[6].length()-1)==',') {
			 cleanedData[6] = cleanedData[6].substring(0, cleanedData[6].length()-1);
			    }
	 	int counter = 0;
		str = str.replace("{", "");
		str = str.replace("}", "");
		for( int i=0; i<str.length(); i++ ) 
		{
		    if( str.charAt(i) == ':' ) 
		    {
		        counter++;
		        if(counter == 6)
		        {
		        	cleanedData = str.substring(i, i + 6);
		        	//System.out.println(fixedResult);
		        }    
		    } 
		}
		cleanedData = cleanedData.replace(":", "");
    	cleanedData = cleanedData.replace(" ", "");
    	cleanedData = cleanedData.replace(",","");
    	*/
		
		this.setData(cleanedData[1]);
	}

}

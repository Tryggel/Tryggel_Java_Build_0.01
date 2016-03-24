import java.io.IOException;

class Handler {

	static writeToFile newFile = new writeToFile();
	static RequestData Data1 = new RequestData();

	
	public static void main(String[] args) throws IOException, InterruptedException {
		
		for(int i = 0; i <= 1000; i++)
		{
			//sending the actual Thread of execution to sleep X milliseconds
			Thread.sleep(20000);
			if(i == 1000)
			{
				System.out.println("The test is done.");
			}
			try {
		        //Update the information from the smart meter
		    	Data1.update();
		    	System.out.println(Data1.getData());
		    	newFile.doWriting(Data1);
		    } catch(Exception e) {
		        System.out.println("Exception : "+e.getMessage());
		    }
			
		}

	}
	
	

}

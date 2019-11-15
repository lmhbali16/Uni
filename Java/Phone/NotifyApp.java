import java.util.Random;
import java.lang.Math;
import java.text.DecimalFormat;

public class NotifyApp implements Notify{


	protected String name;
	protected boolean run;

	public NotifyApp(String name){
		this.name = name;
		this.run = false;

	}

	public String getNameApp(){
			return name;
		
	}

	public void start(){
		this.run = true;
	}

	public void exit(){
		this.run = false;
	}

	public boolean isRunning(){
		return run;
	}

	public String notifyOS(){//notify the user about the current temperature of sydney
		if(run){
			double degree = Math.random() * 49+1;
			DecimalFormat formatting = new DecimalFormat("0.00");
			String notification = "Temperature in Sydney right now is "+formatting.format(degree)+" in Celsius.";
			return notification;	
		}
		else{
			return null;
		}
		

	}
}
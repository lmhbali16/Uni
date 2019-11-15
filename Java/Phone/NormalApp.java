public class NormalApp implements Apps{

	protected String name;
	protected boolean run;
	

	public NormalApp(){

		this.name = "Calculator";
		this.run = false;
		
	}

	public void start(){
		this.run = true;
	}

	public void exit(){
		this.run = false;
	}

	public String getNameApp(){
			return name;
		
		
	}

	public double add(double x, double y){
		if(run){
			return x+y;
		}else{
			return -1;
		}
		
	}


	public double substract(double x, double y){
		
		if(run){
			return x-y;
		}else{
			return -1;
		}
	}

	public double divide(double x, double y){
		if(run){
			return x/y;
		}else{
			return -1;
		}
	}

	public double multiply(double x, double y){
		if(run){
			return x*y;
		}else{
			return -1;
		}
	}

	public boolean isRunning(){
		return run;
	}
	

	
}
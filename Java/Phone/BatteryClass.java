public class BatteryClass extends Battery{

	private int battery;
	public BatteryClass(int battery){//constructor
		this.battery= battery;
	}

	public void setLevel(int value){
		this.battery -= value;//Always substract. We will be carefull when we have to charge
	}

	public int getLevel(){
		return this.battery;//get the battery level
	}
}
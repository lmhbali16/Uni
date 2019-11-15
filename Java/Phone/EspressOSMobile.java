/**
 * EspressOS Mobile Phone Class.
 *
 *
 * EspressOSMobile
 * In this assignment you will be creating an EspressOS Mobile Phone as part of a simulation.
 * The Mobile phone includes several attributes unique to the phone and has simple functionality.
 * You are to complete 2 classes. EspressOSMobile and EspressOSContact
 *
 * The phone has data
 *  Information about the phone state. 
 *    If it is On/Off
 *    Battery level 
 *    If it is connected to network. 
 *    Signal strength when connected to network
 *  Information about the current owner saved as contact information. 
 *    First name
 *    Last name
 *    Phone number
 *  A list of 10 possible contacts.
 *    Each contact stores first name, last name, phone number and chat history up to 20 messages
 *  
 * The phone has functionality
 *  Turning on the phone
 *  Charging the phone. Increase battery level
 *  Change battery (set battery level)
 *  Use phone for k units of battery (decreases battery level by k)
 *  Search/add/remove contacts
 *
 * Attribute features
 *  if the phone is off. It is not connected. 
 *  if the phone is not connected there is no signal strength
 *  the attribute for battery life has valid range [0,100]. 0 is flat, 100 is full.
 *  the attribute for signal strength has a valid range [0, 5]. 0 is no signal, 5 is best signal.
 * 
 * Please implement the methods provided, as some of the marking is
 * making sure that these methods work as specified.
 *
 *
 */
import java.util.ArrayList;
import java.util.List;
import java.io.*;

public class EspressOSMobile{

	public static final int MAXIMUM_CONTACTS = 10;
	

	/* Use this to store contacts. Do not modify. */
	protected EspressOSContact[] contacts;//contacts
	protected boolean phone_on;//whether the phone is on or off
	protected Antenna antenna;//network object: you can find signal strength and connection
	protected Battery battery;//battery object
	protected EspressOSContact owner;//instance for owner details
	protected List<Apps> list_apps;



	/* Every phone manufactured has the following attributes
	 * 
	 * the phone is off
	 * the phone has battery life 25
	 * the phone is not connected
	 * the phone has signal strength 0
	 * Each of the contacts stored in the array contacts has a null value
	 * 
	 * the owner first name "EspressOS"
	 * the owner last name is "Incorporated"
	 * the owner phone number is "180076237867"
	 * the owner chat message should have only one message 
	 *         "Thank you for choosing EspressOS products"
	 *
	 */
	public EspressOSMobile() {
		/* given */
		this.contacts = new EspressOSContact[MAXIMUM_CONTACTS];//max available place for contacts is 10
		
		this.owner = new EspressOSContact("EspressOS", "Incorporated", "180076237867");//default owner's details
		this.owner.addChatMessage("EspressOS", "Thank you for choosing EspressOS products");//immediately add the message to it
		this.phone_on = false;//first the phone is off by default
		this.antenna = new AntennaClass(false, 0);//there is no network conenction and not signal strength therefore. So first argument is network connection and second argument is signal strength
		this.battery = new BatteryClass(25);//The only one argument for battery is the battery level which is always 25
		this.list_apps = new ArrayList<>();//I put all the apps of mine in this list

	}

	/* returns a copy of the owner contact details
	 * return null if the phone is off
	 */
	public EspressOSContact getCopyOfOwnerContact() {
		if(!this.isPhoneOn()){//if the phone is switched off
			return null;
		}
		EspressOSContact new_owner = new EspressOSContact("EspressOS", "Incorporated", "180076237867");;//copy the owner contact by create a new one
		new_owner.addChatMessage("EspressOS", "Thank you for choosing EspressOS products");//add the default message

		return new_owner;//if the phone is on return it

	}


	/* only works if phone is on
	 * will add the contact in the array only if there is space and does not exist
	 * The method will find an element that is null and set it to be the contact
	 */
	public boolean addContact(EspressOSContact contact) {
		if(this.isPhoneOn()&& this.getNumberOfContacts()<MAXIMUM_CONTACTS){//if the phone is on and there is at least 1 place for a new contact
			boolean matched = false;//a flag which will switch as soon as there is a same contact in the list as our argument
			for(int i = 0; i< contacts.length;i++){
				if(contacts[i] == contact){//iterate through the list and find if there is a same one
					matched = true;//if yes, the flag switch
				}
			}
			if(!matched){//if there is no same contact as the argument
				for(int i = 0; i< contacts.length;i++){//iterate through the contact to find an empty place
					if(contacts[i]== null){
						contacts[i] = contact;//as soon as there is one empty place, put the contact in and break out of the loop
						break;
					}
				}
				return true;//return true
			}else if(matched){//if there is already a same contact then just return false and do nothing
				return false;
			}
		}
		return false;//if the phone is off then just return false

	}

	/* only works if phone is on
	 * find the object and set the array element to null
 	 * return true on successful remove
	 */
	public boolean removeContact(EspressOSContact contact) {
		if(!this.isPhoneOn()){//if the phone is off then do nothing
			return false;
		}
		for(int i= 0;i < this.contacts.length;i++){//otherwise iterate the through the list to find the contact
			if(this.contacts[i] == contact){//if it is found set that place in the list to null
				
				this.contacts[i] = null;
				break;
			}
		}
		return true;//return true in the end since even if our loop could not replace anything in the list, we can be sure the contact is not in the list.


	}

	/* only works if phone is on
	 * return the number of contacts, or -1 if phone is off
	 */
	public int getNumberOfContacts() {
		if(!this.isPhoneOn()){//if the phone is off return -1
			return -1;
		}
		int num_contact = 0;//otherwise we use a loop to count all the none null values in our list.
		for(EspressOSContact i : this.contacts){
			if(i != null){
				num_contact +=1;//if it is not null then add it to our num_contact variable
			}
		}
		return num_contact;
	
	}

	/* only works if phone is on
	 * returns all contacts that match firstname OR lastname
	 * if phone is off, or no results, null is returned
	 */
	public EspressOSContact[] searchContact(String name) {
		if(!this.isPhoneOn()){
			return null;//if the phone is off return nothing
		}//of the phone is on
		ArrayList<EspressOSContact> found = new ArrayList<EspressOSContact>();//create a new list to put all the matched contacts.
		if(this.isPhoneOn() && this.getNumberOfContacts() >0){//if there is contacts in the list and the phone is on
			
			for(EspressOSContact i : this.contacts){
				if(i!= null&&(i.getLastName().equals(name)||i.getFirstName().equals(name))){//with for loop search based on name and remember to exclude null
					found.add(i);//as soon as the condition is true add it to the arraylist
				}
			}
			if(found.size()== 0){
				return null;//if the list size is 0 which means there is no matched search, we return null
			}
			EspressOSContact[] matches = new EspressOSContact[found.size()];//otherwise we create an array to put all the contact in the right format
			for(int i = 0;i<found.size();i++){
				matches[i] = found.get(i);//put all the contacts
			}
			return matches;//return the list
		}
		return null;//if any of the above cases does not work, return null
		
	}

	/* returns true if phone is on
	 */
	public boolean isPhoneOn() {
		return phone_on;//check if the phone is on

	}

	/* when phone turns on, it costs 5 battery for startup. network is initially disconnected
	 * when phone turns off it costs 0 battery, network is disconnected
	 * always return true if turning off
	 * return false if do not have enough battery level to turn on
	 * return true otherwise
	 */
	 public boolean setPhoneOn(boolean on) {
	 	if(!this.isPhoneOn()&&on && this.battery.getLevel() >= 6){//if the phone is off,there is enough battery and we want to turn it on
	 		phone_on = on;//turn it on
	 		this.battery.setLevel(5);//set the level to 5
	 		this.antenna.setNetwork(false);//network is disconnected
	 		return true;//return successful turn on
	 	}else if(!on&&this.isPhoneOn()){//if the phone is on and we want to turn off
	 		for(int i = 0; i< list_apps.size();i++){
	 			list_apps.get(i).exit();//we are going to close all the app in our list
	 		}

	 		phone_on = on;//turn off the phone
	 		return true;//return succes
	 	}else if(!this.isPhoneOn()&&on&& this.battery.getLevel() < 6){//if we want to turn on the phone, when it is off and there is not enough battery level
	 		return false;//unsuccessful attempt
	 	}else{
	 		return true;//otherwise true
	 	}

	}
	
	
	/* Return the battery life level. if the phone is off, zero is returned.
	 */
	public int getBatteryLife() {
		if(this.isPhoneOn()){
			return this.battery.getLevel();//only if the phone is on we return the battery life
		}
		return 0;//otherwise return 0
	}
	
	/* Change battery of phone.
	 * On success. The phone is off and new battery level adjusted and returns true
	 * If newBatteryLevel is outside manufacturer specification of [0,100], then 
	 * no changes occur and returns false.
	 */
	public boolean changeBattery(Battery battery) {
		if(battery == null){
			return false;
		}else if(battery.getLevel() >100 || battery.getLevel() < 0){//if the battery is outside of the required range or is null
			return false;//return false
		}else{
			this.battery = new BatteryClass(battery.getLevel());//otherwise change the old battery to a new one
			this.setPhoneOn(false);//turn the phone off
			return true;//return successful change
		}

	}
	
	//change the antenna
	public boolean changeAntenna(Antenna antenna){
		if(antenna == null||this.getBatteryLife()<=2){//if the antenna is null we won't change it
			return false;
		}
		
		if((antenna.getSignalStrength() <0 &&antenna.getSignalStrength() > 5)||!this.isPhoneOn()){
			
			return false;//if the antenna signal strength is not in range we won't change it
		}
		if(this.isPhoneOn() && !this.isConnectedNetwork()&&antenna.getSignalStrength()>0&&antenna.getSignalStrength()<=5){
			this.connectNetwork();
			this.antenna = new AntennaClass(this.isConnectedNetwork(), antenna.getSignalStrength());
			
			
			return true;
		}else if(this.isPhoneOn()&&this.isConnectedNetwork()&&antenna.getSignalStrength()>0&&antenna.getSignalStrength()<=5){
			this.antenna = new AntennaClass(true, antenna.getSignalStrength());
			return true;//if the phone is on and is connected to network, we just change the strength of signal;
		}else{
			return false;
		}

	}
	
	/* only works if phone is on. 
	 * returns true if the phone is connected to the network
	 */
	public boolean isConnectedNetwork() {
		if(!this.isPhoneOn()||this.battery.getLevel()==0){
			this.disconnectNetwork();//if the phone is off or the battery is 0 return false
			return false;
		}
		if(this.antenna.isConnected()){
			return true;//if the phone is on and there is a network connection return true
		}else{
			return false;
		}
	}
	
	/* only works if phone is on. 
	 * when disconnecting, the signal strength becomes zero
	 */
	public void disconnectNetwork() {
		if(this.isPhoneOn()){//if phone is on
			this.antenna.setNetwork(false);//disconnecting and turn the signal strength to 0
			this.antenna.setSignalStrength(0);
		}

	}
	
	/* only works if phone is on. 
	 * Connect to network
	 * if already connected do nothing
	 * if connecting: 
	 *  1) signal strength is set to 1 if it was 0
	 *  2) signal strength will be the previous value if it is not zero
	 *  3) it will cost 2 battery life to do so
	 * returns the network connected status
	 */
	public boolean connectNetwork() {
		if(this.isPhoneOn()&&this.battery.getLevel()>2){//if the phone is on and there is enough battery
			if(!this.isConnectedNetwork()){//if it is not connected yet
				this.battery.setLevel(2);//reduce the battery by two
				this.antenna.setNetwork(true);//set the network 
				if(antenna.getSignalStrength()==0){//if the signal is 0 then set it to 1
					antenna.setSignalStrength(1);

				}
			}
		}else if(this.isPhoneOn()&&this.battery.getLevel()<=2){//if phone is on but not enough battery
			this.battery.setLevel(2);//lose 2%
			this.setPhoneOn(false);//if there is not enought battery for connection turn off


		}

		return this.isConnectedNetwork();//return the status of connection
	}
	
	/* only works if phone is on. 
	 * returns a value in range [1,5] if connected to network
	 * otherwise returns 0
	 */
	public int getSignalStrength() {
		if(this.isPhoneOn()){//if the phone is on
			return this.antenna.getSignalStrength();//return the strength of signal
		}
		else{
			return 0;//if the phone is off then return 0
		}

	}

	/* only works if phone is on. 
	 * sets the signal strength and may change the network connection status to on or off
	 * signal of 0 disconnects network
	 * signal [1,5] can connect to network if not already connected
	 * if the signal is set outside the range [0,5], nothing will occur and will return false
	 */
	public boolean setSignalStrength(int x) {
		if(this.isPhoneOn()){
			if(x == 0){//if the phone is on and the strength is 0
				this.disconnectNetwork();//disconnect network
				this.antenna.setSignalStrength(0);//set it to 0
				return true;
			}else if(x == 1 || x==2 || x==3 || x==4 || x==5){//if the argument is within the required range
				if(this.isConnectedNetwork()){// if it is already connected to network
					this.antenna.setSignalStrength(x);//set the signal strength
					return true;
				}
				else if(!this.isConnectedNetwork()){// if it is not connected to network
					this.connectNetwork();//connect to network
					this.antenna.setSignalStrength(x);//set the strength of signal
					return true;
				}
			}
		}
		return false;//if the phone is off then return false

    }
	
	/* each charge increases battery by 10
	 * the phone has overcharge protection and cannot exceed 100
	 * returns true if the phone was charged by 10
	 */
	public boolean chargePhone() {
		if(this.battery.getLevel() >90&&this.battery.getLevel()<= 100){//if the battery is already more than 90% but not more than 100%
			this.battery.setLevel(-100+this.battery.getLevel());//since our setLevel method use substraction we have to use -100 (add 100) and + current battery level so we make sure it is 100% overall
			return true;//return successful cahrge
		}else if(this.battery.getLevel() >= 100){//if the battery is alread more than 100
			this.battery.setLevel(this.battery.getLevel()-100);//that case we change the battery to 100.
			return true;// return successful charge
		}else if(this.battery.getLevel() < 0){
			this.battery.setLevel(-this.battery.getLevel()-10);//if for some reason the battery level is minus we set the level to 0 and add 10
			return true;
		}else{
			this.battery.setLevel(-10);//just add 10 to the level
			return true;
		}

	}
	
	/* Use the phone which costs k units of battery life.
	 * if the activity exceeds the battery life, the battery automatically 
	 * becomes zero and the phone turns off.
	 */
	public void usePhone(int k) {
		if((this.battery.getLevel() - k) <= 0){//if the cost is larger than the current level of battery
			this.battery.setLevel(this.battery.getLevel());//set it to 0
			this.setPhoneOn(false);//turn it off
			this.disconnectNetwork();//turn off the network as well
		}else{
			this.battery.setLevel(k);//otherwise just substract it from the battery level
		}
	}

//								App methods								   //
//-------------------------------------------------------------------------//
//-------------------------------------------------------------------------//


	public boolean install(Apps app){
		if(this.isPhoneOn()&&this.getBatteryLife()>3){//if the phone is on and have enough battery life, this method cost 3%
			if(app!= null){//if the app is not null
				for(int i = 0; i < this.list_apps.size();i++){
					if(list_apps.get(i) == app){//if there is a same app in the list already
						return false;//return false if the app is already in there;
					}
				}
				//if the app is not there
				list_apps.add(app);//so add it
				this.usePhone(3);//reduce 3%
				return true;
				}
			}
			return false;

		}

	public boolean uninstall(String appname){
		if(appname == null){
			return false;
		}
		if(this.isPhoneOn()&&this.getBatteryLife() >3){//if we have enought battery and the phone is on
			for(int i = 0; i< list_apps.size();i++){
				if(list_apps.get(i)!=null){
					if(list_apps.get(i).getNameApp().equals(appname)){//check the name
						list_apps.remove(list_apps.get(i));//if there is one app with the same name remove it
						this.usePhone(3);//reduce 3%
						
						return true;
					}
				}
				
			}
		}
		return false;
	}

	public List<Apps> getInstalledApps(){
		if(this.isPhoneOn()){
			return this.list_apps;//just get all the apps
		}
		return null;
		
	}

	public List<Background> getBackgroundApps(){
		List<Background> backgroundapp = new ArrayList<>();// I will put all my background apps here
		if(this.isPhoneOn()){
			for(int i = 0; i<list_apps.size();i++){
				if(list_apps.get(i) instanceof Background){//with a loop I will check whether they are background obj
					backgroundapp.add((Background) list_apps.get(i));//if yes, just put into the list
				}
			}
			if(backgroundapp.size()>0){//if there is at least one app in the list return it
				return backgroundapp;
			}else{//otherwise return null
				return null;
			}
		}else{
			return null;//if the phone is off
		}
	}

	public List<Notify> getNotificationApps(){
		if(this.isPhoneOn()){
			List<Notify> notificationapp = new ArrayList<>();//I will put all the notification apps in this list
			for(int i = 0; i < list_apps.size();i++){
				if(list_apps.get(i) instanceof Notify){
					notificationapp.add((Notify) list_apps.get(i));//with for loop I check all the apps and put them into my list accordingly
				}
			}
			if(notificationapp.size()>0){//if there is at least one app then return it
				return notificationapp;
			}
			else{
				return null;
			}
		}else{
			return null;//if the phone is off
		}
	}

	public List<String> getNotifications(){
		List<String> notifications = new ArrayList<>();
		if(this.isPhoneOn()&& this.getBatteryLife()>3){//this method also cost 3%

			if(this.getNotificationApps()!=null){//if there is at least 1 notification app in our list
				for(int i = 0; i<this.getNotificationApps().size();i++){

					if(this.getNotificationApps().get(i).isRunning()){// if the app is running
						
						notifications.add(this.getNotificationApps().get(i).notifyOS());//get the notifications
					}
					
				}
			}
			if(notifications.size() > 0){
				this.usePhone(3);//reduce 3%
				return notifications;//if there is notification in the list return it
			}
		}
		return null;//otherwise return null
	
	}

	public boolean run(String name){
		if(name == null){
			return false;
		}
		if(this.isPhoneOn()&&this.getBatteryLife()>3){//it will cost 3% of battery
			for(int i = 0;i<list_apps.size();i++){
				if(list_apps.get(i).getNameApp().equals(name)){// find the name of the app
					// I will run it if  it can find the app
					list_apps.get(i).start();
					this.usePhone(3);//it will cost 3% of the battery
					if(list_apps.get(i) instanceof Notify && list_apps.get(i) != null){
						Notify app = (Notify) list_apps.get(i);
						System.out.println(app.notifyOS());//print notification
					}
					return true;
				}
			}
		}
		return false;
	}

	public boolean close(String name){
		if(this.isPhoneOn()){// if the phone is on
			for(int i = 0;i<list_apps.size();i++){
				if(list_apps.get(i).getNameApp().equals(name)){
					
					list_apps.get(i).exit();//if they find it then close it;
					return true;
					
				}
			}
		}
		return false;
		
	}

}

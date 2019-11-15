import static org.junit.Assert.*;
import org.junit.Test;

public class BatteryTest{

	@Test
	public void CheckBatteryStart(){//check a new phone's battery when we "buy" it
		EspressOSMobile test = new EspressOSMobile();
		assertEquals(0, test.getBatteryLife());//get the battery life when it is off

	}
	@Test
	public void CheckBatteryTurnOn(){//check battery life after we turn it on
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		assertTrue(test.isPhoneOn());//get the battery life when it is on
		assertEquals(20, test.getBatteryLife());
	}

	@Test
	public void CheckBatteryCharge100times(){//check the charge of the battery
		//check if it exceed 100% by calling the chargePhone() method 100 times
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		for(int i = 0;i <100;i++){
			test.chargePhone();
		}
		assertEquals(100, test.getBatteryLife());//after charging we check the battery level

	}
	@Test
	public void CheckChangeBatteryValid(){// we check if we can change the battery
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		Battery new_battery = new BatteryClass(50);
		test.changeBattery(new_battery);//change it
		test.setPhoneOn(true);//since the change is supposed to be successful, the phone need to be turn on and lose 5%
		assertEquals(new_battery.getLevel()-5,test.getBatteryLife());//check it again
	}
	@Test
	public void CheckChangeBatteryInvalid(){//check invalid battery
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//turn on and lose 5%
		Battery new_battery = new BatteryClass(200);//what if the battery exceed the limit
		test.changeBattery(new_battery);
		
		assertEquals(20, test.getBatteryLife());//we are assuming that the battery has not changed and so the phone's battery level is 20
		Battery low_battery = new BatteryClass(-10);//check if the battery is lower than what is allowed
		
		assertEquals(20, test.getBatteryLife());//we should assume that the change has not happened

	}
	@Test
	public void SequenceofTurnOnPhone(){//check what happens if we turn of and on multiple times
		EspressOSMobile test = new EspressOSMobile();
		Battery new_battery = new BatteryClass(95);//we change the battery for a new one
		test.changeBattery(new_battery);
		for(int i = 0; i<200;i++){//we will turn the phone off and on 200 times
			if(i%2==0){
				test.setPhoneOn(true);//we turn it on
			}else{
				test.setPhoneOn(false);//then turn off
			}
		}

		assertEquals(0, test.getBatteryLife());//we should not be able to turn on the phone because of the battery
		assertFalse(test.isPhoneOn());//the phone should be off

	}
	@Test
	public void ActivitySequence(){//check phone's battery after using it
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		Battery new_battery = new BatteryClass(100);//let's work with 100% battery
		test.changeBattery(new_battery);
		test.setPhoneOn(true);//actually we work with 95%
		test.connectNetwork();//connecting should reduce 2% from the battery
		assertEquals(93, test.getBatteryLife());
		test.usePhone(30); //let's play some game
		assertEquals(63,test.getBatteryLife());
		test.setPhoneOn(false);
		test.setPhoneOn(true);//turn it off and on should reduce 5%
		assertEquals(58,test.getBatteryLife());
		test.usePhone(70); //let's use the phone heavily
		assertEquals(0, test.getBatteryLife());
		assertFalse(test.isPhoneOn());//should turn off the phone and 0 battery life

	}

	@Test
	public void ChangeBatteryNull(){//change the battery with null
		EspressOSMobile test = new EspressOSMobile();
		test.changeBattery(null);
		test.setPhoneOn(true);
		assertEquals(20, test.getBatteryLife());//the battery life should not be changed 

	}

	@Test
	public void AddContactRemoveContactBattery(){
		//based on the assignment adding and removing contact hsould not reduce battery life
		EspressOSMobile test = new EspressOSMobile();
		Battery new_battery = new BatteryClass(100);
		test.changeBattery(new_battery);
		test.setPhoneOn(true);
		EspressOSContact adam = new EspressOSContact("Adam", "Levine","1234567");
		EspressOSContact anna = new EspressOSContact("Anna","Black","76543210");//create some contacts
		test.addContact(adam);
		test.addContact(anna);//add a few contacts

		test.removeContact(adam);//remove one
		assertEquals(95, test.getBatteryLife());//battery level should not change

	}

	@Test
	public void TestBatteryMethods(){//check Battery class construction
		Battery battery = new BatteryClass(100);
		battery.setLevel(20); //we deduce 20%
		assertEquals(80,battery.getLevel());// get the level

	}

	@Test
	public void PhoneoffBatteryChange(){
		EspressOSMobile test = new EspressOSMobile();//check battery life even if the phone is off
		test.changeBattery(new BatteryClass(100));//let's change it
		assertEquals(0, test.getBatteryLife());
		assertFalse(test.isPhoneOn());//should not the battery change and the phone is still off
		
	}
	@Test
	public void PhoneoffBatteryCharge(){
		EspressOSMobile test = new EspressOSMobile();//check battery life even if the phone is off
		test.changeBattery(new BatteryClass(30));//let's change again
		test.chargePhone();//let's check how it charging work
		assertEquals(0, test.getBatteryLife());//should be since 
	}
	@Test
	public void BatteryLifePhoneoff(){
		EspressOSMobile test = new EspressOSMobile();//check battery life even if the phone is off
		assertEquals(0, test.getBatteryLife());

	}
	@Test
	public void PhoneoffBatteryChangeOn(){// check what happens if we turn on the phone after changing battery
		EspressOSMobile test = new EspressOSMobile();//check battery life even if the phone is off
		test.changeBattery(new BatteryClass(100));//let's change it
		test.setPhoneOn(true);//turn on the phone
		assertEquals(95, test.getBatteryLife());//should get an almost full battery
		assertTrue(test.isPhoneOn());

	}
	@Test
	public void PhoneoffBatteryChargeOn(){//check battery after charging and turning on the phone.
		EspressOSMobile test = new EspressOSMobile();//check battery life even if the phone is off
		test.changeBattery(new BatteryClass(30));//let's change again
		test.chargePhone();//let's check how it charging work
		test.setPhoneOn(true);//turn on -5
		assertEquals(35, test.getBatteryLife());//should be able to get the battery life
		assertTrue(test.isPhoneOn());
	} 
}
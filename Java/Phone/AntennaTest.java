import static org.junit.Assert.*;
import org.junit.Test;

public class AntennaTest{


	@Test
	public void TestConstructionAntenna(){
		Antenna test = new AntennaClass(false, 3);//test a random antenna's methods
		assertFalse(test.isConnected());//should get a not connected state
		assertEquals(3, test.getSignalStrength());
		test.setSignalStrength(4);// let's change the signal strength
		assertEquals(4, test.getSignalStrength());//check what we will have after that

	}

	@Test
	public void TestDefaultConnection(){//let's see what we get when we buya new phone

		EspressOSMobile test = new EspressOSMobile();
		assertFalse(test.isConnectedNetwork());//see if it return false as the phone is off
		test.setPhoneOn(true);
		assertFalse(test.isConnectedNetwork());//see if it return false after turning the phone on
	}

	@Test
	public void TestConnectNetwork(){//let see what happen if we try to connect to the net with enough battery
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		test.connectNetwork();
		assertEquals(1,test.getSignalStrength());//since this is the first time we connect, it should give us 1
		assertEquals(18, test.getBatteryLife());//we should get 18% on battery since we had to turn on and connect to network
		assertTrue(test.isConnectedNetwork());//should be connected
	}

	@Test
	public void ConnectNetworkNoBattery(){//try to connect to network without enough battery
		EspressOSMobile test = new EspressOSMobile();
		test.changeBattery(new BatteryClass(7));//we just have enough battery to connect to net and turn on the phone
		test.setPhoneOn(true);//-5 for turning on the phone
		test.connectNetwork();//connect to network -2
		assertEquals(0,test.getBatteryLife());//no battery
		assertFalse(test.isPhoneOn());//should turn off
		assertFalse(test.isConnectedNetwork());//no network

	}
	@Test
	public void ConnectNetworkMinusBattery(){//let see if we dont even have battery for connection
		EspressOSMobile test = new EspressOSMobile();
		test.changeBattery(new BatteryClass(6));//just enough to turn on the phone
		test.setPhoneOn(true);//-5 for turning on the phone
		test.connectNetwork();
		assertEquals(0,test.getSignalStrength());//no signal
		assertEquals(0,test.getBatteryLife());//no battery should be 0 and not -1
		assertFalse(test.isConnectedNetwork());//not connection
		assertFalse(test.isPhoneOn());//phone is off
	}

	@Test
	public void TestSignalStrength(){//check how the signal strength change after reconnection
		EspressOSMobile test = new EspressOSMobile();
		test.changeBattery(new BatteryClass(100));//let's work with full battery life
		test.setPhoneOn(true);//-5
		test.connectNetwork();//-2
		test.disconnectNetwork();
		assertFalse(test.isConnectedNetwork());//should not be connected
		assertEquals(0, test.getSignalStrength());//hence no strength
		
	}

	@Test
	public void TestSignalStrengthReconnect(){
		EspressOSMobile test = new EspressOSMobile();
		test.changeBattery(new BatteryClass(100));//let's work with full battery life
		test.setPhoneOn(true);//-5
		test.connectNetwork();//-2
		test.disconnectNetwork();
		test.connectNetwork();//-2
		assertTrue(test.isConnectedNetwork());//should reconnect
		assertEquals(1,test.getSignalStrength());//and strength should be 1
		assertEquals(91, test.getBatteryLife());
	}

	@Test
	public void getSignalStrengthOff(){
		EspressOSMobile test = new EspressOSMobile();
		assertEquals(0, test.getSignalStrength());//check signal strength method when phone is off
	}
	@Test
	public void getSignalStrengthOn(){
		//check signal strength when phone is on
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		assertTrue(test.isPhoneOn());
		assertEquals(0, test.getSignalStrength());
	}

	@Test
	public void setSignalStrengthOff(){//check if we can set signal strength as the phone is off
		EspressOSMobile test = new EspressOSMobile();
		test.setSignalStrength(3);
		assertEquals(0, test.getSignalStrength());//should not be able to do it
	}

	@Test
	public void setSignalStrengthOn(){//set signal strength as the phone is on and connected
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		test.connectNetwork();
		test.setSignalStrength(3);
		assertEquals(3,test.getSignalStrength());//should the signal strength change
	}
	@Test
	public void SignalSequence(){//check signal strength after some methods
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		test.connectNetwork();//conenct to network, should be 1
		test.setSignalStrength(3);//change it to 3
		test.disconnectNetwork();//should be 0 as it is disconencted
		test.connectNetwork();//should be one as we reconnect
		assertEquals(1, test.getSignalStrength());
		assertTrue(test.isConnectedNetwork());//connected

	}
	@Test
	public void setSignalStrengthInvalid(){//check invalid signal strength
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		test.connectNetwork();//conenct to network, should be 1
		test.setSignalStrength(-4);//should not be changed
		assertEquals(1, test.getSignalStrength());
	}
	@Test
	public void setSignalStrengthInvalid2(){//check invalid signal strength (over 5)
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		test.connectNetwork();//conenct to network, should be 1
		test.setSignalStrength(41);//should not be changed
		assertEquals(1, test.getSignalStrength());
	}
	@Test
	public void UsePhoneConnection(){//let's see how the connection change if we use the phone but don't run out of battery
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//-5
		test.connectNetwork();//-2
		test.usePhone(3);//-3
		assertTrue(test.isPhoneOn());//phone is still on
		assertEquals(15, test.getBatteryLife());
		assertTrue(test.isConnectedNetwork());//still connected
	}

	@Test
	public void UsePhoneConnectionOff(){
		//let's use the phone till it turn of and check conenction
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//-5
		test.connectNetwork();//-2
		test.usePhone(40);//-40
		assertFalse(test.isPhoneOn());//should turn off
		assertFalse(test.isConnectedNetwork());//should not connect
		assertEquals(0,test.getSignalStrength());//should not have any signal
		assertEquals(0,test.getBatteryLife());//no battery life
	}

	@Test
	public void ConnectAlreadConnected(){
		//see what happen if we connect twice to the network
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//-5
		test.connectNetwork();//-2
		test.connectNetwork();//should not reduce 2 since we are already connected
		assertEquals(18, test.getBatteryLife());
		assertTrue(test.isConnectedNetwork());
	}

	@Test
	public void DisconnecteAlreadyDisconnected(){
		//check what happen if we already disconnected and call the method again
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//-5//disconnected already
		test.disconnectNetwork();//disconnect again
		assertFalse(test.isConnectedNetwork());//should return false
	}

	@Test
	public void TestChangeAntenna(){//test normal change, where the new antenna is valid
		EspressOSMobile test = new EspressOSMobile();
		test.changeBattery(new BatteryClass(100));//work with full battery
		test.setPhoneOn(true);//in turn on state
		test.changeAntenna(new AntennaClass(false, 3));//let's work with signal level 3
		assertEquals(3, test.getSignalStrength());//should be changed
		assertTrue(test.changeAntenna(new AntennaClass(false, 3)));//should the method return true
		assertTrue(test.isConnectedNetwork());//should be connected
		assertEquals(93, test.getBatteryLife());//should reduce 2% from battery life
		assertTrue(test.isPhoneOn());//should be still on
	}
	@Test
	public void TestChangeAntennaNull(){
		EspressOSMobile test = new EspressOSMobile();
		test.changeBattery(new BatteryClass(100));//work with full battery
		test.setPhoneOn(true);//in turn on state
		test.changeAntenna(null);//change with an invalid antenna
		assertFalse(test.isConnectedNetwork());//shouldn't change the network state
		assertEquals(95, test.getBatteryLife());//shouldn't change the battery life
		assertTrue(test.isPhoneOn());// should not turn off the phone
		assertFalse(test.changeAntenna(null));//it should return a false boolean
		assertEquals(0, test.getSignalStrength());//not signal strength
	}

	@Test
	public void TestChangeAntennaInvalidRange(){
		EspressOSMobile test = new EspressOSMobile();
		test.changeBattery(new BatteryClass(100));//work with full battery
		test.setPhoneOn(true);//in turn on state
		test.changeAntenna(new AntennaClass(true, 6));//try to change with an invalid antenna
		assertTrue(test.isPhoneOn());//phone should not turn off
		assertFalse(test.changeAntenna(new AntennaClass(true, 6)));//method should return false
		assertEquals(95, test.getBatteryLife());//should not change the battery
		assertFalse(test.isConnectedNetwork());//should not connect to network
	}



}
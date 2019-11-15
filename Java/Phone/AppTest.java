import static org.junit.Assert.*;
import org.junit.Test;

public class AppTest{



	@Test
	public void TestInstall(){

		EspressOSMobile test = new EspressOSMobile();//check install method
		test.setPhoneOn(true);//lost 5% of battery
		assertTrue(test.isPhoneOn());//it should turn on
		Apps notify = new NotifyApp("Weather");//create an app
		assertTrue(test.install(notify));//it should return true if we install the app
		test.install(notify);//should lose 3% of battery
		assertEquals(17,test.getBatteryLife());
		assertEquals(1, test.getInstalledApps().size());//there should be one notification app in our list
		assertEquals(1, test.getNotificationApps().size());//there should be one notification app in the notification list

	}

	@Test
	public void TestInstallNull(){
		EspressOSMobile test = new EspressOSMobile();//check install method
		test.setPhoneOn(true);//lost 5% of battery
		assertFalse(test.install(null));//should be unsuccessful
		assertEquals(20, test.getBatteryLife());

	}

	@Test
	public void TestInstallPhoneOff(){
		EspressOSMobile test = new EspressOSMobile();
		Apps notify = new NotifyApp("Weather");//create an app
		assertFalse(test.install(notify));//should be unsuccessful, since the phone is off
		assertEquals(0, test.getBatteryLife());//no battery change, and since it is off, the battery should be 0


	}

	@Test
	public void TestInstallNoBattery(){
		EspressOSMobile test = new EspressOSMobile();
		Apps notify = new NotifyApp("Weather");//create an app

		Battery battery = new BatteryClass(7);//let's see what happens if we dont have enoug battery
		test.changeBattery(battery);
		test.setPhoneOn(true);//-5% so 2% is left
		assertFalse(test.install(notify));//unsuccessful install
		assertEquals(0,test.getInstalledApps().size());//no app
		assertEquals(2, test.getBatteryLife());//still 2% battery

	}



	@Test
	public void TestUninstall(){
		EspressOSMobile test = new EspressOSMobile();//check install method
		test.setPhoneOn(true);//lost 5% of battery
		Apps notify = new NotifyApp("Weather");//create an app
		assertTrue(test.install(notify));
		test.install(notify);//-3%
		assertTrue(test.uninstall("Weather"));//we were able to uninstall the app
		test.uninstall("Weather");//lose 3% of battery
		assertEquals(0, test.getInstalledApps().size());//no app on the phone
		assertEquals(14,test.getBatteryLife());//final battery level


	}

	@Test
	public void TestUninstallInvalid(){
		EspressOSMobile test = new EspressOSMobile();//check install method
		test.setPhoneOn(true);//lost 5% of battery
		Apps notify = new NotifyApp("Weather");//create an app
		test.install(notify);// install it
		assertFalse(test.uninstall("noapp"));//try to uninstall an invalid one

	}

	@Test
	public void TestUninstallNull(){//uninstall null
		EspressOSMobile test = new EspressOSMobile();//check install method
		test.setPhoneOn(true);//lost 5% of battery
		Apps notify = new NotifyApp("Weather");//create an app
		test.install(notify);// install it
		assertFalse(test.uninstall(null));//see what happens if we uninstall null
	}

	@Test
	public void TestUninstallPhoneOff(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		Apps notify = new NotifyApp("Weather");
		test.install(notify);//turn on the phone, install the app and then turn off
		test.setPhoneOn(false);
		assertFalse(test.uninstall("Weather"));//try to uninstall app, unsuccessful
	}

	@Test
	public void TestUninstallNoBattery(){
		EspressOSMobile test = new EspressOSMobile();
		Battery battery = new BatteryClass(10);
		test.changeBattery(battery);//change battery to a new one
		test.setPhoneOn(true);//-5%, 5 is left
		Apps notify = new NotifyApp("Weather");
		test.install(notify);//turn on the phone, install the app, -3-->2 is left
		assertFalse(test.uninstall("Weather"));//Not able to uninstall

	}

	@Test
	public void TestGetInstalledApps(){
		EspressOSMobile test = new EspressOSMobile();//check the getinstalledapp method
		test.setPhoneOn(true);
		Apps notify = new NotifyApp("Weather");
		BackgroundApp background = new BackgroundApp();//create two apps
		test.install(notify);
		test.install(background);//install two apps
		assertEquals(2, test.getInstalledApps().size());//we should have 2 apps in the list

	}

	@Test
	public void TestGetInstalledAppsPhoneOFF(){//check what happens when we try to call the methos and the phone is off
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//turn on the phone
		Apps notify = new NotifyApp("Weather");
		test.install(notify);//install an app
		test.setPhoneOn(false);//turn of the phone
		assertNull(test.getInstalledApps());//since the phone is off, return null

	}


	@Test
	public void TestgetBackgroundApps(){//check the getbackgroundapp method
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		Apps background = new BackgroundApp();//apps class
		Apps notify = new NotifyApp("Weather");
		BackgroundApp background2 = new BackgroundApp();//create 3 app, this one is a BackgroundApp class
		test.install(background);
		test.install(background2);
		test.install(notify);//install all of them
		assertEquals(2, test.getBackgroundApps().size());//should only return 2 apps;



	}

	@Test
	public void TestgetBackgroundAppsNoApps(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		assertNull(test.getBackgroundApps());//if there is no app it should return null

	}

	@Test
	public void TestgetBackgroundAppsPhoneOff(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		Apps background = new BackgroundApp();
		test.install(background);//install an app
		test.setPhoneOn(false);//turn off the phone
		assertNull(test.getBackgroundApps());//should not return anything other than null

	}

	@Test
	public void TestgetNotificationApps(){//test getnotificationapps method
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		BackgroundApp background = new BackgroundApp();
		Apps notify = new NotifyApp("Weather");//Apps class
		BackgroundApp background2 = new BackgroundApp();
		Apps notify2 = new NotifyApp("hm");//create four apps
		test.install(notify);
		test.install(background2);
		test.install(background);
		test.install(notify2);//install all of them
		assertEquals(2, test.getNotificationApps().size());//should return 2

	}

	@Test
	public void TestgetNotificationAppsNoApps(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		assertNull(test.getNotificationApps());//if there is no app it should return null

	}

	@Test
	public void TestgetNotificationAppsPhoneOff(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		test.install(new NotifyApp("Weather"));//install a notify app
		test.setPhoneOn(false);//turn the phone off
		assertNull(test.getNotificationApps());//should return null

	}


	@Test
	public void TestgetNotifications(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//-5
		Apps notify = new NotifyApp("Weather");
		Apps notify2 = new NotifyApp("hm");
		test.install(notify);//-3,-3
		test.install(notify2);//install two notify apps and run them;
		assertTrue(test.run("Weather"));
		assertTrue(test.run("hm"));//test the run method
		assertEquals(2, test.getNotifications().size());//we should receive 2 notification, 1 from each apps
		 
	}

	@Test
	public void TestgetNotificationNoNotification(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		assertNull(test.getNotifications());//if there is no notification it should return null

	}

	@Test
	public void TestgetNotifPhoneOff(){
		//check if we can get notifications if the phone is off
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		test.install(new NotifyApp("Weather"));//install an app
		test.setPhoneOn(false);//turn off the phone
		assertNull(test.getNotifications());//no notification should we get--> null

	}

	@Test
	public void testGetNotifNoBattery(){
		//Not enought battery to get notifications
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);
		test.install(new NotifyApp("Weather"));
		test.changeBattery(new BatteryClass(7));
		test.setPhoneOn(true);
		assertNull(test.getNotifications());//since we dont have enough battery it should return null


	}

	@Test
	public void TestRun(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//-5
		Apps notify = new NotifyApp("Weather");
		test.install(notify);//install the app
		assertTrue(test.run("Weather"));//run the app
		assertTrue(test.getNotificationApps().get(0).isRunning());//see if the app is running

	}

	@Test
	public void TestRunNull(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//-5
		Apps notify = new NotifyApp("Weather");
		test.install(notify);//install the app
		assertFalse(test.run(null));//run null, it should be unsuccessful

	}

	@Test
	public void TestRunInvalid(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//-5
		Apps notify = new NotifyApp("Weather");
		test.install(notify);//install the app
		assertFalse(test.run("noapp"));//run an invalid app
	}

	@Test
	public void TestRunPhoneOff(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//-5
		Apps notify = new NotifyApp("Weather");
		test.install(notify);//install an app
		test.setPhoneOn(false);//turn off the phone
		assertFalse(test.run("Weather"));//try to run the app when the phone is off


	}
	@Test
	public void TestRunNoBattery(){
		EspressOSMobile test = new EspressOSMobile();
		test.changeBattery(new BatteryClass(10));//battery of 10
		test.setPhoneOn(true);//-5-->5%
		Apps notify = new NotifyApp("Weather");
		test.install(notify);//-3 -->2% left after installing app
		assertFalse(test.run("Weather"));//try to run the program
		assertEquals(2, test.getBatteryLife());//should be still 2%
	}

	@Test
	public void Testclose(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//-5
		Apps notify = new NotifyApp("Weather");
		test.install(notify);//install the app
		test.run("Weather");//run the app
		assertTrue(test.close("Weather"));//close the app
		assertFalse(test.getNotificationApps().get(0).isRunning());//check if the app is running
	}

	@Test
	public void TestcloseNull(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//-5
		Apps notify = new NotifyApp("Weather");
		test.install(notify);//install the app
		test.run("Weather");//run the app
		assertFalse(test.close(null));//close the app, unsuccessful

	}
	@Test
	public void TestcloseInvalid(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//-5
		Apps notify = new NotifyApp("Weather");
		test.install(notify);//install the app
		test.run("Weather");//run the app
		assertFalse(test.close("Weather2"));//close the app, unsuccessful

	}

	@Test
	public void TestclosePhoneOff(){
		EspressOSMobile test = new EspressOSMobile();
		test.setPhoneOn(true);//-5
		Apps notify = new NotifyApp("Weather");
		test.install(notify);//install the app, -3%
		test.run("Weather");//run the app, -3%
		test.setPhoneOn(false);
		test.setPhoneOn(true);//-5, turn on because in an off state we can't have access to the methods
		assertFalse(test.getInstalledApps().get(0).isRunning());//see if the app is running.should not after turning off and then turning on
		assertEquals(9,test.getBatteryLife());//battery life is 9
	}


}
import java.util.Random;
import java.lang.Math;
import java.text.DecimalFormat;
import java.util.*;


public class BackgroundApp implements Background{


	protected String name;
	protected boolean run;
	protected BackgroundThread backgroundapp;
	protected double debt;
	protected double salary;



	public BackgroundApp(){
		this.name = "Student debt counter";//app name
		this.run = false;//current state of the app: whether it is opened and running or not
		this.backgroundapp = new BackgroundThread(this);//object for background run
		this.debt = 10000;//starting student debt, coz why not
		this.salary = 0;//my salary in US$
		
	}

	public void start(){
			this.run = true;
			Scanner scan = new Scanner(System.in);
			System.out.print("Your current weekly salary: ");//input my current salary
			String money = scan.nextLine();
			try{
				this.salary = Double.parseDouble(money);
			}catch(IllegalArgumentException e){
				System.out.println("Invalid salary!");
				this.start();
			}

			backgroundapp.start();//in a loop start to run the the app in the background
		//it will call the backgroundStrart();
	}

	public void exit(){
		backgroundapp.exit();//call the exit and interupt the lhe process
		this.run = false;//

	}

	
	public void backgroundStart(){
		this.debt += debt*0.025;
		//the money I earn is in US$
		double money = Math.random()*1000+salary*0.015;//I put my money into the bank and my parents also help me out paying the loan
		this.debt-= getData(money);//I change my US money to AUD$ to pay my debt
		if(this.debt >= 1000000){
			System.out.println("Too much student debt. No reason to charge u more");
			this.exit();
		}else if(debt <=0){//if there is no debt we just exit from the program
			this.debt = 0;
			System.out.println("Congratulation, you have paid back all of your student loan");
			this.exit();

		}else{
			System.out.println(this.getStudentDebt());
		}


	}

	public double getData(double x){
		return x*1.38;//convert the US money to AUD$ to pay my debt

			
	}

	public boolean isRunning(){
		return run;
	}

	public String getStudentDebt(){
		DecimalFormat formatting = new DecimalFormat("0.00#");
		return formatting.format(debt);//we would like to get our student debt
	}

	public String getNameApp(){
		return name;
	}


}
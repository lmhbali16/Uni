public class AntennaClass extends Antenna{

	private boolean connection;
	private int signal;

	public AntennaClass(boolean connection, int signal){//constructor
		this.connection = connection;
		this.signal = signal;
	}


	public boolean isConnected(){//check connection status
		return this.connection;
	}

	public void setNetwork(boolean isConnected){//change the connection status
		this.connection = isConnected;
	}

	public int getSignalStrength(){//get the strength of signal
		return this.signal;
	}

	public void setSignalStrength(int n){//set the strength of signal
		this.signal = n;
	}
}
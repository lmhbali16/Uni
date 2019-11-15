
/**
 * EspressOS Mobile Phone Contact Class.
 *
 * EspressOSContact
 * 
 * == Contact data ==
 * Each EspressOSContact stores the first name, last name and phone number of a person. 
 * These can be queried by calling the appropriate get method. They are updated 
 * with new values. The phone number can only be a 6 - 14 digit number.
 * The chat history is also stored. 
 * 
 * 
 * == Chat history ==
 * Each EspressOSContact stores the history of chat messages related to this contact. 
 * Suppose there is a conversation between Angus and Beatrice:
 * 
 * Angus: Man, I'm so hungry! Can you buy me a burrito?
 * Beatrice: I don't have any money to buy you a burrito.
 * Angus: Please? I haven't eaten anything all day.
 * 
 * Each time a message is added the name of the person and the message is 
 * combined as above and recorded in the sequence it was received.
 * 
 * The messages are stored in the instance variable String array chatHistory. Provided for you.
 * Unfortunately there are only 20 messages maximum to store and no more. 
 * When there are more than 20 messages, oldest messages from this array are discarded and 
 * only the most recent 20 messages remain. 
 * 
 * The functions for chat history are 
 *   addChatMessage
 *   getLastMessage
 *   getOldestMessage
 *   clearChatHistory()
 *
 * Using the above conversation as an example
 *   addChatMessage("Angus", "Man, I'm so hungry! Can you buy me a burrito?");
 *   addChatMessage("Beatrice", "I don't have any money to buy you a burrito.");
 *   addChatMessage("Angus", "Please? I haven't eaten anything all day.");
 *
 *   getLastMessage() returns "Angus: Please? I haven't eaten anything all day."
 *   getOldestMessage() returns "Angus: Man, I'm so hungry! Can you buy me a burrito?"
 *
 *   clearChatHistory()
 *   getLastMessage() returns null
 *   getOldestMessage() returns null
 *
 *
 * == Copy of contact ==
 * It is necessary to make copy of this object that contains exactly the same data. 
 * There are many hackers working in other parts of EspressOS, so we cannot trust them 
 * changing the data. A copy will have all the private data and chat history included.
 *
 *
 * Please implement the methods provided, as some of the marking is
 * making sure that these methods work as specified.
 *
 *
 */
public class EspressOSContact
{
	public static final int MAXIMUM_CHAT_HISTORY = 20;	
	
	/* given */
	protected String[] chatHistory;
	protected String fname;
	protected String lname;
	protected String pnumber;
	protected int chatHistory_idx;
	
	
	
	
	public EspressOSContact(String fname, String lname, String pnumber) {
		/* given */
		this.fname = fname;//first name
		this.lname = lname;//last name
		this.pnumber = pnumber;//phone number
		chatHistory = new String[MAXIMUM_CHAT_HISTORY];//initiate a new list for chat history with a max capacity
		chatHistory_idx = 0;//index of for the very first empty space in our chat history
		
		

	}
	
	public String getFirstName() {
		return this.fname;//retrun first name

	}
	public String getLastName() {
		return this.lname;//return last name

	}
	public String getPhoneNumber() {
		return this.pnumber;//return phone number

	}

	/* if firstName is null the method will do nothing and return
	 */
	public void updateFirstName(String firstName) {
		if(firstName != null){//if the argument is not null
			this.fname = firstName;//change the name
		}
		

	}
	/* if lastName is null the method will do nothing and return
	 */
	public void updateLastName(String lastName) {
		if(lastName !=null){//if the argument is not null change the last name
			this.lname = lastName;
		}
		

	}
	
	/* only allows integer numbers (long type) between 6 and 14 digits
	 * no spaces allowed, or prefixes of + symbols
	 * leading 0 digits are allowed
	 * return true if successfully updated
	 * if number is null, number is set to an empty string and the method returns false
	 */
	public boolean updatePhoneNumber(String number) {
		String[] numbers = number.split("");//split the string into characters
		boolean update = true;// I use flag to detect invalid characters
		if(number ==null){//if the argument is null then it doesn't do anything
			return false;//return false
		}
		for(String i : numbers){
			//check all the character one by one with for loop
			if((i.equals("0") || i.equals("1") || i.equals("2") || i.equals("3") || i.equals("4") || i.equals("5") || i.equals("6") || i.equals("7") || i.equals("8") || i.equals("9"))&& numbers.length>=6 &&numbers.length<=14){
				continue;
			//if phone number is not valid then the flag will change
			}else{
				update = false;
			}
		}
		if(update){//if the flag have not changed (which mean the number is valid) then we can update the phone number
			this.pnumber = number;
		}
		return update;//return the update

	}
	
	/* add a new message to the chat
	 * The message will take the form
	 * whoSaidIt + ": " + message
	 * 
	 * if the history is full, the oldest message is replaced
	 * Hint: keep track of the position of the oldest or newest message!
	 */
	public void addChatMessage(String whoSaidIt, String message) {
		if(chatHistory_idx<MAXIMUM_CHAT_HISTORY){//check the index if there is still space for message
			chatHistory[chatHistory_idx] = whoSaidIt+": "+message;//add the message
			chatHistory_idx+=1;//we add one to remember where is the next empty space
		}else if(chatHistory_idx >= 20){// if the index is more than our limit of our chat history spaces
			//it means there is no space left in the array
			for(int i = 0; i < chatHistory.length-1;i++){//so with for loop we will reallocate all the messages
				chatHistory[i] = chatHistory[i+1];
			}
			chatHistory[19] = whoSaidIt+": "+message;//the last message in the history will be our new message

		}

		

	}

	/* after this, both last and oldest message should be referring to index 0
	 * all entries of chatHistory are set to null
	 */
	public void clearChatHistory() {
		this.chatHistory = new String[MAXIMUM_CHAT_HISTORY];//we create a new empty array
		chatHistory_idx = 0;//index changed to 0 again as the very first empty place is at the first position of the array

	}

	/* returns the last message 
	 * if no messages, returns null
	 */
	public String getLastMessage() {
		if(chatHistory_idx == 0){
			return chatHistory[chatHistory_idx];//if the last message is also the only message
		}
		else{
			return chatHistory[chatHistory_idx-1];//otherwise we return the last message by substract 1 from the index since it show the very first empty place.
		}

	}
	
	/* returns the oldest message in the chat history
	 * depending on if there was ever MAXIMUM_CHAT_HISTORY messages
	 * 1) less than MAXIMUM_CHAT_HISTORY, returns the first message
	 * 2) more than MAXIMUM_CHAT_HISTORY, returns the oldest
	 * returns null if no messages exist
	 */
	public String getOldestMessage() {
		int num_null = 0;//we use a for loop to check the number of null
		for(int i = 0; i < chatHistory.length;i++){
			if(chatHistory[i]==null){
				num_null +=1;
			}
		}
		if(num_null==chatHistory.length){//if the chat history only contain null, we return null
			return null;
		}
		if(num_null>0 && num_null < chatHistory.length){//if there is less null than the size of array, it means that there is message in the chat history
			//in that case the oldest message must be at the index 0 of the array
			return chatHistory[0];
		}else{
			return chatHistory[0];// just return the first element in case we miss something
		}

	}


	/* creates a copy of this contact
	 * returns a new EspressOSContact object with all data same as the current object
	 */
	public EspressOSContact copy() 
	{
		EspressOSContact new_contact = new EspressOSContact(this.fname,this.lname, this.pnumber);//create a new object with the same name and number as the original
		new_contact.chatHistory = this.chatHistory;//put all the messages in it
		
		return new_contact;//return the new object
	}
	
	/* -- NOT TESTED --
	 * You can impelement this to help with debugging when failing ed tests 
	 * involving chat history. You can print whatever you like
	 * Implementers notes: the format is printf("%d %s\n", index, line); 
	 */
	public void printMessagesOldestToNewest() {

	}
}
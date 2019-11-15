import java.io.IOException;
import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.io.PrintWriter;



/**
 * Maze Game
 *
 * INFO1113 Assignment 1
 * 2018 Semester 2
 *
 * The Maze Game.
 * In this assignment you will be designing a maze game.
 * The player can step left, right, up or down.
 * However, you need to complete the maze within a given number of step.
 *
 * As in any maze, there are walls that you cannot move through. If you try to
 * move through a wall, you lose a life. You have a limited number of lives.
 * There is also gold on the board that you can collect if you move ontop of it.
 *
 * Please implement the methods provided, as some of the marks are allocated to
 * testing these methods directly.
 *
 * @author YOU :)
 * @date 23 August 2018
 *
 */
public class MazeGame {
    /* You can put variables that you need throughout the class up here.
     * You MUST INITIALISE ALL of these class variables in your initialiseGame
     * method.
     */

    // A sample variable to show you can put variables here.
    // You would initialise it in initialiseGame method.
    // e.g. Have the following line in the initialiseGame method.
    // sampleVariable = 1;
    static int lives;
    static int step;
    static int gold;
    static int rows;
    static int col;
    static String[][] board;
    static int x;
    static int y;
    static int x_des;
    static int y_des;



    /**
     * Initialises the game from the given configuration file.
     * This includes the number of lives, the number of steps, the starting gold
     * and the board.
     *
     * If the configuration file name is "DEFAULT", load the default
     * game configuration.
     *
     * NOTE: Please also initialise all of your class variables.
     *
     * @args configFileName The name of the game configuration file to read from.
     * @throws IOException If there was an error reading in the game.
     *         For example, if the input file could not be found.
     */
    public static void initialiseGame(String configFileName) throws IOException {
        if( (!(new File(configFileName)).exists() || !(new File(configFileName)).isFile())&& !configFileName.equals("DEFAULT")){
            throw new IOException();
            
        }
        // TODO: Implement this method.
        if(configFileName.equals("DEFAULT")){
            lives = 3;
            step = 20;
            gold = 0;
            rows = 4;
            col = 10;
            board = new String[][] {{"#","@"," ","#","#"," "," ","&","4","#"},{"#","#"," "," ","#"," ","#","#"," ","#"},{"#","#","#"," "," ","3","#"," "," "," "},{"#","#","#","#","#","#","#"," "," ","#"}};
            x_des = 1;
            y_des = 0;
            x = 7;
            y = 0;
        }else{

            File file = new File(configFileName);
        
            Scanner scan = new Scanner(file);
            ArrayList<String> array = new ArrayList<String>();

            while(scan.hasNextLine()){
                String a = scan.nextLine();
                array.add(a);
                }
            String[] layout = array.get(0).split(" ");
            if(layout.length != 4){
                throw new   IOException();
            }
            try{
                lives = Integer.parseInt(layout[0]);
                step = Integer.parseInt(layout[1]);
                gold = Integer.parseInt(layout[2]);
                rows = Integer.parseInt(layout[3]);
                col = array.get(1).split("").length;
                String[][] b = new String[rows][col];
            }catch(ArrayIndexOutOfBoundsException e){
                System.out.println("Error: Could not load the game configuration from '"+file+"'.");
                return;

            }
            lives = Integer.parseInt(layout[0]);
            step = Integer.parseInt(layout[1]);
            gold = Integer.parseInt(layout[2]);
            rows = Integer.parseInt(layout[3]);
            col = array.get(1).split("").length;
            
            
            String[][] b = new String[rows][col];
            for(int  i=1; i <= rows; i++){
                String[] line = array.get(i).split("");

                for(int j = 0; j < col;j++){
                    b[i-1][j]= line[j];
                }

            }
            board = b;
            for (int i = 0; i < board.length;i++){
                for (int j = 0; j < board[i].length;j++){
                    if(board[i][j].equals("@")){
                        y_des = i;
                        x_des = j;
                    }
                }
            }
        }
        
    }

    /**
     * Save the current board to the given file name.
     * Note: save it in the same format as you read it in.
     * That is:
     *
     * <number of lives> <number of steps> <amount of gold> <number of rows on the board>
     * <BOARD>
     *
     * @args toFileName The name of the file to save the game configuration to.
     * @throws IOException If there was an error writing the game to the file.
     */
    public static void saveGame(String toFileName) throws IOException {
        // TODO: Implement this method.
        
        File f = new File(toFileName);
        PrintWriter write = new PrintWriter(f);
        write.println(lives+" "+step+" "+gold+" "+rows);
        for (String[] i : board){
            String a = "";
            for(int j = 0; j < i.length;j++){
                
                a+=i[j];
            }
            write.println(a);
            
        }
        write.flush();
        write.close();
        System.out.println("Successfully saved the current game configuration to '"+toFileName+"'.");



    }

    /**
     * Gets the current x position of the player.
     *
     * @return The players current x position.
     */
    public static int getCurrentXPosition() {
        // TODO: Implement this method.
        for(int i = 0; i < board.length;i++){
            for(int j = 0; j < board[i].length; j++){
                if(board[i][j].equals("&")){
                    x = j;
                }
            }
        }
        
        return x;
    }

    public static void setPosition(){
        for(int i = 0; i < board.length;i++){
            for(int j = 0; j < board[i].length; j++){
                if(board[i][j].equals("&")){
                    y = i;
                    x = j;
                }
            }
        }
    }
    /**
     * Gets the current y position of the player.
     *
     * @return The players current y position.
     */
    public static int getCurrentYPosition() {
        // TODO: Implement this method.
        for(int i = 0; i < board.length;i++){
            for(int j = 0; j < board[i].length; j++){
                if(board[i][j].equals("&")){
                    y = i;
                    
                }
            }
        }
        return y;
    }

    /**
     * Gets the number of lives the player currently has.
     *
     * @return The number of lives the player currently has.
     */
    public static int numberOfLives() {
        // TODO: Implement this method.
        
        return lives;
    }

    /**
     * Gets the number of remaining steps that the player can use.
     *
     * @return The number of steps remaining in the game.
     */
    public static int numberOfStepsRemaining() {
        // TODO: Implement this method.
        
        return step;
    }

    /**
     * Gets the amount of gold that the player has collected so far.
     *
     * @return The amount of gold the player has collected so far.
     */
    public static int amountOfGold() {
        // TODO: Implement this method.
        
        return gold;
    }


    /**
     * Checks to see if the player has completed the maze.
     * The player has completed the maze if they have reached the destination.
     *
     * @return True if the player has completed the maze.
     */
    public static boolean isMazeCompleted() {
        // TODO: Implement this method.
        setPosition();
        if(y_des==y && x_des==x){
            //System.out.printf("Congratulations! You completed the maze!\nYour final status is:\n");
            //printStatus();
            
            return true;
        }
        
        return false;
    }

    /**
     * Checks to see if it is the end of the game.
     * It is the end of the game if one of the following conditions is true:
     *  - There are no remaining steps.
     *  - The player has no lives.
     *  - The player has completed the maze.
     *
     * @return True if any one of the conditions that end the game is true.
     */
    public static boolean isGameEnd() {
        // TODO: Implement this method.
        
        if(lives <= 0 && step > 0){
            
            System.out.printf("Oh no! You have no lives left.\nBetter luck next time!\n");
            return true;
        }
        else if(step <= 0 && lives > 0&&!isMazeCompleted()){
            
            System.out.printf("Oh no! You have no steps left.\nBetter luck next time!\n");
            return true;
        }
        else if((lives <= 0 && step <= 0)){
            
            System.out.printf("Oh no! You have no lives and no steps left.\nBetter luck next time!\n");
            return true;
        }else if(isMazeCompleted() && (lives > 0 || step >= 0)){
            
            System.out.printf("Congratulations! You completed the maze!\nYour final status is:\n");
            printStatus();
            
            return true;
        }else{
        
        return false;}
    }

    /**
     * Checks if the coordinates (x, y) are valid.
     * That is, if they are on the board.
     *
     * @args x The x coordinate.
     * @args y The y coordinate.
     * @return True if the given coordinates are valid (on the board),
     *         otherwise, false (the coordinates are out or range).
     */
    public static boolean isValidCoordinates(int x_new, int y_new) {
        // TODO: Implement this method.
        setPosition();
        if(x_new < col && x_new >= 0 && y_new < rows && y_new >=0 && x < col  && x >= 0 && y >=0 &&y<rows){
            
            return true;
        }else{
           
            return false;
        }
    }

    /**
     * Checks if a move to the given coordinates is valid.
     * A move is invalid if:
     *  - It is move to a coordinate off the board.
     *  - There is a wall at that coordinate.
     *  - The game is ended.
     *
     * @args x The x coordinate to move to.
     * @args y The y coordinate to move to.
     * @return True if the move is valid, otherwise false.
     */
    public static boolean canMoveTo(int x_new, int y_new) {
        // TODO: Implement this method.
        
       
        if(lives > 0 && step > 0){
            if(isValidCoordinates(x_new,y_new)){
                if(!board[y_new][x_new].equals("#")){
                    if(!isGameEnd()){
                    
                    return true;
                    }else{
                        
                        return false;
                    }
                }
                else{
                    
                    return false;
                }
            }else{
               
                return false;}
        }else{
            
            return false;}

    }

    /**
     * Move the player to the given coordinates on the board.
     * After a successful move, it prints "Moved to (x, y)."
     * where (x, y) were the coordinates given.
     *
     * If there was gold at the position the player moved to,
     * the gold should be collected and the message "Plus n gold."
     * should also be printed, where n is the amount of gold collected.
     *
     * If it is an invalid move, a life is lost.
     * The method prints: "Invalid move. One life lost."
     *
     * @args x The x coordinate to move to.
     * @args y The y coordinate to move to.
     */
    public static void moveTo(int x_new, int y_new) {
        // TODO: Implement this method.
        
        if(canMoveTo(x_new,y_new)){
            System.out.println("Moved to ("+x_new+", "+y_new+").");
            if(board[y_new][x_new].equals("0")||board[y_new][x_new].equals("1")||board[y_new][x_new].equals("2")||board[y_new][x_new].equals("3")||board[y_new][x_new].equals("4")||board[y_new][x_new].equals("5")||board[y_new][x_new].equals("6")||board[y_new][x_new].equals("7")||board[y_new][x_new].equals("8")||board[y_new][x_new].equals("9")){
                gold =gold + Integer.parseInt(board[y_new][x_new]);
                System.out.println("Plus "+board[y_new][x_new]+" gold.");
            }
            step -= 1;
            if(board[y_new][x_new].equals("#") && !isValidCoordinates(x_new, y_new)){
                x = x;
                y = y;
                lives = lives -1;
            }
            board[y][x] = ".";
            board[y_new][x_new] = "&";
        }else{
            System.out.println("Invalid move. One life lost.");
            lives = lives- 1;
            step=step-1;

        }

        
    }

    /**
     * Prints out the help message.
     */
    public static void printHelp() {
        // TODO: Implement this method.
        setPosition();
        System.out.println("Usage: You can type one of the following commands.");
        System.out.println("help         Print this help message.");
        System.out.println("board        Print the current board.");
        System.out.println("status       Print the current status.");
        System.out.println("left         Move the player 1 square to the left.");
        System.out.println("right        Move the player 1 square to the right.");
        System.out.println("up           Move the player 1 square up.");
        System.out.println("down         Move the player 1 square down.");
        System.out.println("save <file>  Save the current game configuration to the given file.");
    }

    /**
     * Prints out the status message.
     */
    public static void printStatus() {
        // TODO: Implement this method.
        
        System.out.println("Number of live(s): "+ lives);
        System.out.println("Number of step(s) remaining: "+ step);
        System.out.println("Amount of gold: "+gold);
    }

    /**
     * Prints out the board.
     */
    public static void printBoard() {
        // TODO: Implement this method.
        
        for (String[] i : board){
            for(int j = 0; j < i.length;j++){
                System.out.print(i[j]);
            }
            System.out.println("");
        }
    }

    /**
     * Performs the given action by calling the appropriate helper methods.
     * [For example, calling the printHelp() method if the action is "help".]
     *
     * The valid actions are "help", "board", "status", "left", "right",
     * "up", "down", and "save".
     * [Note: The actions are case insensitive.]
     * If it is not a valid action, an IllegalArgumentException should be thrown.
     *
     * @args action The action we are performing.
     * @throws IllegalArgumentException If the action given isn't one of the
     *         allowed actions.
     */
    public static void performAction(String action) throws IllegalArgumentException {
        if(action.toLowerCase().equals("help")||action.toLowerCase().equals("board")||action.toLowerCase().equals("status")||action.toLowerCase().equals("up")||action.toLowerCase().equals("down")||action.toLowerCase().equals("left")||action.toLowerCase().equals("right")||(action.length() > 5 && action.toLowerCase().substring(0,5).equals("save "))){
            // TODO: Implement this method.
            setPosition();
            String save = "save ";
            if (action.toLowerCase().equals("help") && action.length() == 4){
                printHelp();
            }else if(action.toLowerCase().equals("board")&& action.length() == 5){
                printBoard();
            }else if(action.toLowerCase().equals("status")&& action.length() == 6){
                printStatus();
            }else if(action.toLowerCase().equals("up")&& action.length() == 2){
                moveTo(x,y-1);
                setPosition();
            }else if(action.toLowerCase().equals("down")&& action.length() == 4){
                moveTo(x,y+1);
                setPosition();
            }else if(action.toLowerCase().equals("right")&& action.length() == 5){
                moveTo(x+1,y);
                setPosition();
            }else if(action.toLowerCase().equals("left")&& action.length() == 4){
                moveTo(x-1,y);
                setPosition();
            }else if(action.length() > 5 && action.substring(0,5).toLowerCase().equals(save)){
                String[] savefile = action.split(" ");
                if(savefile.length == 2){
                    if(savefile[1].length() > 4){
                        if(savefile[1].substring(savefile[1].length()-4,savefile[1].length()).equals(".txt")){
                            try{
                                saveGame(savefile[1]);
                            }catch(IOException e){
                                System.out.println("Error: Could not save the current game configuration to '"+savefile[1]+"'.");
                            }
                        }else{
                            System.out.println("Error: Could not save the current game configuration to '"+savefile[1]+"'.");
                        }
                    }else{
                        System.out.println("Error: Could not save the current game configuration to '"+savefile[1]+"'.");
                    }
                }else{
                    throw new IllegalArgumentException();
                }

            }
            else{
               throw new IllegalArgumentException();
            }
        }else{
            throw new IllegalArgumentException();
        }
        setPosition();
        
    }

    /**
     * The main method of your program.
     *
     * @args args[0] The game configuration file from which to initialise the
     *       maze game. If it is DEFAULT, load the default configuration.
     */
   
    public static void main(String[] args) {
        // Run your program (reading in from args etc) from here.
        if (args.length < 1){
            System.out.println("Error: Too few arguments given. Expected 1 argument, found 0.");
            System.out.println("Usage: MazeGame [<game configuration file>|DEFAULT]");
            return;
        }else if(args.length > 1){
            System.out.println("Error: Too many arguments given. Expected 1 argument, found "+args.length+".");
            System.out.println("Usage: MazeGame [<game configuration file>|DEFAULT]");
        }else{
            String file = args[0];
            if(new File(file).exists() || file.equals("DEFAULT")){
                try{
                    initialiseGame(file);
                }catch(IOException e){
                    System.out.printf ("You did not complete the game.\n");
                }
                
            }else{
                System.out.println("Error: Could not load the game configuration from '"+file+"'.");
                return;
            }
            Scanner keyboard = new Scanner(System.in);

            while (!isGameEnd()) {

                if(!keyboard.hasNextLine()){
                    System.out.printf("You did not complete the game.\n");
                    break;
                }
                if(isMazeCompleted() && !keyboard.hasNextLine()){
                    System.out.println("Your final status is:");
                    printStatus();
                }

                String input = keyboard.nextLine();
                if (!input.isEmpty() && input != null) {
                    try {
                        performAction(input);
                    }
                    catch (IllegalArgumentException e) {
                        System.out.println("Error: Could not find command '"+ input+"'.");
                        System.out.println("To find the list of valid commands, please type 'help'.");
                    }
                }

                

                }
        

        }

    }

}
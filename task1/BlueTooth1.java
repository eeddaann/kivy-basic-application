import java.io.DataInputStream;
import java.io.IOException;

import lejos.nxt.Button;
import lejos.nxt.ButtonListener;
import lejos.nxt.LCD;
import lejos.nxt.comm.Bluetooth;
import lejos.nxt.comm.NXTConnection;


public class LegoMove {

	/**
	 * @param args
	 */
	//Class members are static because we are not using instances.
	static boolean ready=true;
	static NXTConnection btc;
	private static void goOut(){
		ready=false;
	}
	public static void main(String[] args)throws Exception {
		//Listener for the Enter button.
		Button.ENTER.addButtonListener(new ButtonListener() {
		      public void buttonPressed(Button b) {
		        LCD.drawString("ENTER pressed", 0, 0);
		        //Method to quit the loop
		        goOut();
		      }

		      public void buttonReleased(Button b) {
		        LCD.clear();
		      }
		    });
					//Writing states on the Lego lcd screen.
				    LCD.drawString("waiting",0,0);
				    LCD.refresh();
				    //Listen for incoming connection
				    btc = Bluetooth.waitForConnection();
				    btc.setIOMode(NXTConnection.RAW);
				    LCD.clear();
				    LCD.drawString("connected",0,0);
				    LCD.refresh();
				    //The InputStream for read data
				    DataInputStream dis=btc.openDataInputStream();
				    //loop for read data
				    while(ready==true){
				        byte n=-1;
				            try {
								n=dis.readByte();
							} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
							}
				        LCD.clear();
				        LCD.drawInt(n, 4, 4);
				    }
				     try {
						dis.close();
					} catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				 LCD.clear();
				 LCD.drawString("closing",0,0);
				 LCD.refresh();
				 btc.close();
				 LCD.clear();
			}
}
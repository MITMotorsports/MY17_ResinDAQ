#include <wiringPi.h>
#include <cstdlib>
#define DEBUG false

#if DEBUG
	#include <iostream>
#endif

using namespace std;

int main(void) {
	wiringPiSetup();

	const int pin = atoi(getenv("PIN_shutdown"));
	const int led = atoi(getenv("PIN_shutdown_led"));
	#if DEBUG
		cout<<"Pin is: "<<pin<<endl;
		cout<<"Led is: "<<led<<endl;
	#endif

	pinMode(pin, INPUT);
	pullUpDnControl(pin, PUD_DOWN);

	pinMode(led, OUTPUT);
	digitalWrite(led, LOW);

	for(;;) {
		delay(250);
		#if DEBUG
			cout<<digitalRead(pin)<<endl;
		#endif

		if (digitalRead(pin)) {
			bool doit = true;
			for (int i = 0; i<10; ++i) {
				if (!digitalRead(pin)) {
					doit = false;
				}
				delay(300);
			}
			if (doit)
				digitalWrite(led, HIGH);
				system("curl -X POST --header \"Content-Type:application/json\" \"$RESIN_SUPERVISOR_ADDRESS/v1/shutdown?apikey=$RESIN_SUPERVISOR_API_KEY\"");
		}
	}
	return 0;
}

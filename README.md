# QR Code Generator and Telegram Bot
This project consists of two separate scripts: a QR code generator and a Telegram bot. The QR code generator creates unique QR codes for guests and stores their information in an SQLite database. The Telegram bot reads QR codes and checks if the guest is in the database. If the guest is found, the bot displays their name, family members, and whether they have checked in or not. If they haven't checked in, the bot allows the user to check them in. The bot also provides commands to list all guests, list checked-in guests, add family members to a guest, and delete family members from a guest.

## QR Code Generator
The QR code generator script can be used to generate unique QR codes for guests. Each guest is assigned a unique 12-digit code and their information is stored in an SQLite database. The script uses the qrcode library to generate QR code images and saves them as PNG files. The generated codes can be printed out or displayed on a screen for guests to scan.

### Dependencies
This script requires the following libraries to be installed:

```
* qrcode
* Pillow
* sqlite3
```

**Usage**

To generate a QR code for a guest, run the following command:

```
bash
Copy
python qr_maker.py <guest_name> <family_members>
```
*<guest_name>*: The name of the guest.

*<family_members>*: A comma-separated list of family members accompanying the guest.

The script will generate a unique 12-digit code for the guest and save their information in the database. A QR code image will also be generated and saved as a PNG file.


## Telegram Bot
The Telegram bot script can be used to check if a guest is in the database and allow them to check in if they haven't already. The bot can also be used to list all guests, list checked-in guests, add family members to a guest, and delete family members from a guest.

### Dependencies

This script requires the following libraries to be installed:

```
* python-telegram-bot
* pyzbar
* Pillow
* sqlite3
```

**Usage**

To use the Telegram bot, follow these steps:

```
1. Create a new bot using the BotFather on Telegram.
2. Copy the bot token and insert it into the TELEGRAM_TOKEN variable in the bot.py file.
3. Start the bot using the following command:
4. Open terminal/command prompt
5. Insert python bot.py
6. Send a QR code image to the bot. The bot will decode the QR code and check if the guest is in the database. If the guest is found, the bot will display their name, family members, and whether they have checked in or not. If they haven't checked in, the bot will provide a button that allows the user to check them in.
```

Plans for Future Development:

```
1. Update guest information (e.g. name, family members)
2. Export guest information to a CSV file
3. Notify event organizers when guests check in
4. Provide analytics on guest attendance
5. We also plan to improve the error handling and input validation in both scripts to make them more robust and user-friendly.
```

Conclusion
We hope that these scripts are useful for managing guests at events. If you have any questions or feedback, please don't hesitate to reach out to us!

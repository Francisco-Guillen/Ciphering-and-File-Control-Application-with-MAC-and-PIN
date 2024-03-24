# FALL-INTO-OBLIVION

## Description:

The purpose of this application is to control a folder called *FALL-INTO-OBLIVION* where files will be placed and encrypted. It will also calculate the *Message Authentication Code* (MAC) and the key used for encryption will be randomly generated for each file, and will come from a *Personal Identification Number* (PIN). This application only runs in *Client Line Interface* (CLI) mode.

## Job Features:

Basic functionalities of the application:

1. Allows files to be encrypted, saving the result in a folder called *FALL-INTO-OBLIVION*;
2. Calculate the *hash* value of the file, also saving the result together with the cryptogram (in separate files);
3. Automatically generate a **PIN**, and use it as the key to encrypt each file;
4. Calculate the **HMAC** of the cryptograms;
5. Allow the file to be decrypted by guessing the **PIN**. Only up to 3 attempts should be allowed; 
6. Check the integrity of the file if the **PIN** has been guessed.

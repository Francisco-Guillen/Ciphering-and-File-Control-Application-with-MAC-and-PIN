import hashlib
import hmac
import random
import os
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
from pathlib import Path
import pathlib
generated_pin = random.randint(999, 9999)
desired_pin = str(generated_pin)
max_tries = 3


def encrypt(key, filename):
    chunksize = 64 * 1024 
    
    # Formato do Output do ficheiro cifrado:
    outputFile = filename + '.aes'
    checkFile = pathlib.Path(filename)
    # Verificar se o ficheiro em questão já está cifrado, caso contrário prossegue com a cifra:
    if checkFile.exists():
        if(("Decifrado" not in filename) and ('Hash' not in filename) and ('.aes' not in filename) ):
            # Tamanho do ficheiro:
            filesize = str(os.path.getsize(filename)).zfill(16)
            # Vetor de Inicialização:
            iv = Random.new().read(16)
            
            # Gerar a cifra de AES:
            encryptor = AES.new(key, AES.MODE_CBC, iv)
            
            with open(filename, 'rb') as infile:
                with open(outputFile, 'wb') as outfile:
                    outfile.write(filesize.encode('utf-8')) # Converter o formato de texto para bytes, permitindo assim a divisão por blocos;
                    outfile.write(iv) # Escrever o vetor de inicialização no ficheiro de saída;
                    
                    while True:
                        chunk = infile.read(chunksize) # Leitura dos 'chunks' do ficheiro de entrada;
                        
                        if len(chunk) == 0: 
                            break
                        
                        elif len(chunk) % 16 != 0:
                            chunk += b' ' * (16 - (len(chunk) % 16))
                            
                        outfile.write(encryptor.encrypt(chunk)) # Escrita, através do 'encrypt' de cada 'chunk', no ficheiro de saída, caso o elif se verifique;
                        print("Cifrado com sucesso!\n")
                hashFile = os.path.join(filename[:-4] + "Hash.txt")
                with open(hashFile, 'w') as file:
                    file.write(getHashValue(filename))
                print("HMAC do ficheiro "+ filename +": "+ getMACValue(filename))
                os.remove(filename)
        
def getHashValue(filename):
    
    h = hashlib.sha256()
    
    chunk=0
    with open(filename,'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read()
            h.update(chunk)
    return h.hexdigest()

def getMACValue(filename):
    h = hashlib.sha256()
    key = str.encode(desired_pin)
    with open(filename, "r") as file:
                message=file.read()
                hmac1 = hmac.new(key, message.encode('UTF-8'), hashlib.sha256)
    digestvalue = hmac1.hexdigest()
    return digestvalue

def verify_pin(the_pin):
    return the_pin == desired_pin 

def decrypt(key, filename):
    chunksize = 64 * 1024 
    save_path = 'FALL-INTO-OBLIVION/'
    completeName = os.path.join(save_path, filename)
    # Formato do Output do ficheiro decifrado:
    preoutputFile = "Decifrado_" + filename[:-4]
    outputFile = os.path.join(save_path, preoutputFile)
    checkFile = pathlib.Path(completeName)
    
    if checkFile.exists():
        if(("Decifrado" not in filename) and ('Hash' not in filename)):
            with open(completeName, 'rb') as infile:
                filesize = int(infile.read(16))    
                iv = infile.read(16) # Leitura do vetor de inicialização; 
                    
                # Gerar a decifra de AES:
                decryptor = AES.new(key, AES.MODE_CBC, iv)
                    
                with open(outputFile, 'wb') as outfile:
                    while True:
                        chunk = infile.read(chunksize) # Leitura dos 'chunks' do ficheiro de entrada (cifrado);
                        
                        if len(chunk) == 0:
                            break
                            
                        outfile.write(decryptor.decrypt(chunk))  # Escrita decifrada no ficheiro de saída, através do 'decrypt' de cada 'chunk' lido; 
                    outfile.truncate(filesize)  # Redefine o tamanho do ficheiro para o número de bytes dado/adequado;
                    print("Decifrado com sucesso!\n")
    else:
        print("O ficheiro não existe!")

def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def help():
    print("-------------------------------------------------------------Help---------------------------------------------------------------------------")
    print("| - 1. Atualizar o programa: atualiza a pasta FALL-INTO-OBLIVION, cifra os novos ficheiros, calcula o Hash e o HMAC de cada um.            |")
    print("| - 2. Verificar a integridade do ficheiro: caso o ficheiro ja se encontre decifrado verifica se este é o mesmo que o original.            |")
    print("| - 3. Adivinhe o PIN e decifre o ficheiro: Caso o utilizador acerta o pin dentro de 3 tentativas poderá decifrar um ficheiro pretendido.  |")
    print("--------------------------------------------------------------------------------------------------------------------------------------------")

def menuPrincipal():
    option = -1
    tries=0
    while True:
        for filename in os.listdir("FALL-INTO-OBLIVION"):
            save_path = 'FALL-INTO-OBLIVION/'
            completeName = os.path.join(save_path, filename)
            encrypt(getKey(desired_pin), completeName)
            
        print("------------------- Menu Principal -----------------------")
        print("| - 1. Atualizar o programa;                             |")
        print("| - 2. Adivinhe o PIN e decifre o ficheiro;              |")
        print("| - 3. Verificar a integridade do ficheiro;              |")
        print("| - 4. Help;                                             |")
        print("| - 5. Sair;                                             |")
        print("----------------------------------------------------------")

        option = input("Seleciona uma opção: ")

        if option == "1":
            print("Atualizado")

        elif option == "2":

            while tries < max_tries:
                print(desired_pin)
                pin = input('Por favor, introduz o código PIN: ')
                if verify_pin(pin):
                    filename = input("Nome do ficheiro a decifrar: ")
                    decrypt(getKey(desired_pin),filename)
                    break
                else:
                    print('Código PIN incorreto, por favor tente outra vez: ')
                tries += 1

            else:   
                print("Bloqueado. Excedeu o número de tentativas")

        elif option == "3":
            save_path = 'FALL-INTO-OBLIVION/'
            filename = input("Nome do ficheiro do qual pretende ver a integridade: ")
            completeName = os.path.join(save_path, filename)
            hashfileoriginal=os.path.join(save_path, filename[:-8] + "Hash.txt")
            DecryptedFile = "FALL-INTO-OBLIVION/Decifrado_"+filename[:- 4]
            checkFile = pathlib.Path(DecryptedFile)
            if checkFile.exists():
                with open(hashfileoriginal, "r") as file1:
                    HashReal=file1.read()
                    DecryptedFile = "FALL-INTO-OBLIVION/Decifrado_"+filename[:- 4]
                    HashDecifrado=getHashValue(DecryptedFile)
                    if(HashReal == HashDecifrado):
                        print("O ficheiro recebido é o mesmo que o original")
                    else:
                        print("O ficheiro não é o mesmo que o original")
            else:
                print("O ficheiro não existe ou não pode ser decifrado!")
        
        elif option == "4":
            help()
            break

        elif option == "5":
            break
        else:
            print("Opção inválida! Tente novamente.")


menuPrincipal()

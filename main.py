import os
import subprocess
import random
from Crypto.PublicKey import RSA

def menu1():
    print("\n*--------------------------*")
    print("*      Menu Principal      *")
    print("*  1 - Agente de Confianca *")
    print("*  2 - Cliente             *")
    print("*  0 - Sair                *")
    print("*--------------------------*")

def menu2():
    print("\n*-----------------------------*")
    print("*   Menu Agente de Confianca  *")
    print("*  1 - Listar Clientes        *")
    print("*  2 - Assinar                *")
    print("*  3 - Criar um Porta-Chaves  *")
    print("*  4 - Enviar Ficheiros       *")
    print("*  0 - Sair                   *")
    print("*-----------------------------*")

def menu3():
    print("\n*----------------*")
    print("*  Menu Cliente  *")
    print("*  1 - Registar  *")
    print("*  2 - Entrar    *")
    print("*  0 - Sair      *")
    print("*----------------*")

def menu4():
    print("\n*-------------------------------*")
    print("*          Menu Entrar          *")
    print("*  1 - Enviar Ficheiro          *")
    print("*  2 - Ver Ficheiros Recebidos  *")
    print("*  3 - Ler Ficheiro Recebido    *")
    print("*  0 - Sair                     *")
    print("*-------------------------------*")

def menu5():
    print("\n*-----------------------------------*")
    print("*     Sub Menu Enviar Ficheiros     *")
    print("*  1 - Cifrar                       *")
    print("*  2 - Assinar                      *")
    print("*  3 - Escolher o Cliente a enviar  *")
    print("*  0 - Sair                         *")
    print("*----------------------------- -----*")

#Variaveis globais
LOGIN_USER = ''
FOLDER_ROOT = os.getcwd()
FOLDER_AGENTE = os.getcwd() + "/.agente/"
FOLDER_CLIENTE = os.getcwd() + "/.cliente/"
FILE_NAME = ''

#Verifica se e numero inteiro
def opcao_input():
    while(True):
        try:
            x = int(input("Introduza a opcao: "))
            break
        except ValueError:
            print("\nIntroduza um inteiro!\n")
    return x

def opcao_inv():
    print("Opcao Invalida!")

#Menu Agente de Confianca
def listClientesRegistados():
    print("\n__Lista de Clientes Registados__\n")
    
    #Abre o ficheiro para leitura
    f1 = open(os.path.join(FOLDER_AGENTE,"login.txt"),"r")
    #A funcao mode verifica se o ficheiro foi aberto
    if(f1.mode == "r"):
        t = f1.readlines()
        for i in t:
            text = i.replace('\n','').split('_',1)
            print("         "+text[0])

def assinarA():
    listClientesLigados()
    cliente = str(input("\nCliente a Enviar: "))
    print()
    flag = False
    flag_aux = False
    lfile = open("ligados.txt", "r")
    t =  lfile.readlines()
    
    #Verifica se o cliente esta ligado ao sistema
    for i in t:
        if(cliente == i.replace('\n','')):
            flag = True
    if(flag):
        #Mostra quais são os ficheiros na pasta do cliente
        cmd = 'ls -a'.split()
        s = ".agente/."+cliente
        cmd.append(s)

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        x = p.communicate()[0]
        p.stdin.close()

        file_a = str(input("Ficheiro a assinar: "))

        cliente_E = file_a.split('_',1)

        #Decifrar com a chave de sessao do cliente que enviou
        output2 = open(os.path.join(FOLDER_AGENTE+"."+cliente,file_a+'-2'),'w+')
        cmd = 'openssl enc -aes128 -d -K'.split()

        f = open(os.path.join(FOLDER_AGENTE,cliente_E[0]+"Sessao.txt"),'r')
        aux = f.read()
        f.close()
        cmd.append(aux)
        cmd.append('-in')
        cmd.append(FOLDER_AGENTE+"."+cliente+'/'+file_a)
        cmd.append('-iv')
        cmd.append('0')

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=output2)
        x = p.communicate()[0]
        p.stdin.close()

        #Cifrar com a chave de sessao do cliente que recebe
        output3 = open(os.path.join(FOLDER_AGENTE+"."+cliente,file_a),'w+')
        cmd = 'openssl enc -aes128 -e -K'.split()

        f = open(FOLDER_AGENTE+cliente+"Sessao.txt",'r')

        cmd.append(f.read())
        cmd.append('-in')
        cmd.append(FOLDER_AGENTE+"."+cliente+'/'+file_a+'-2')
        cmd.append('-iv')
        cmd.append('0')

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=output3)
        x = p.communicate()[0]
        p.stdin.close()
        f.close()

        #Assinar o Ficheiro
        private_key = os.path.join(FOLDER_AGENTE,"key_private.pem")
        f_sign = os.path.join(FOLDER_AGENTE+"."+cliente,file_a+'.sig')
        sigoutput1 = open(f_sign, 'w')
        
        cmd = 'openssl rsautl -sign -in'.split()
        cmd.append(os.path.join(FOLDER_AGENTE+"."+cliente,file_a))
        cmd.append('-inkey')
        cmd.append(private_key)

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=sigoutput1)
        x = p.communicate()[0]
        p.stdin.close()

        cmd = 'cp'.split()
        cmd.append(os.path.join(FOLDER_AGENTE,"key_public.pem"))
        cmd.append(os.path.join(FOLDER_AGENTE+"."+cliente+"/",'pk.pem'))

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        x = p.communicate()[0]
        p.stdin.close()
        print("\nDone\n")
        flag_aux = True
    else:
        print("O Cliente nao existe ou nao esta ligado ao sistema!")
    lfile.close()
    return flag_aux

#Funcao auxiliar para mover ficheiros do agente para o cliente
def moveto_cliente(cliente,file1):
    send_file = os.path.join(FOLDER_AGENTE+"."+cliente,file1)
    dir_cliente = os.path.join(FOLDER_CLIENTE+"."+cliente+"/Recebido/",file1)
    
    cmd = 'mv'.split()
    cmd.append(send_file)
    cmd.append(dir_cliente)

    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    x = p.communicate()[0]
    p.stdin.close()

#Funcao para mover ficheiros do agente para o cliente
def send(flag_assi):
    lfile = open("ligados.txt", "r")
    t =  lfile.readlines()
    if(len(t) > 1):
        listClientesLigados()
        cliente = str(input("\nCliente a Enviar: "))
        print()
        flag = False
        #Verifica se o cliente esta ligado ao sistema
        for i in t:
            if(cliente == i.replace('\n','')):
                flag = True
        if(flag):
            #Mostra quais são os ficheiros na pasta do cliente
            cmd = 'ls -a'.split()
            s = ".agente/."+cliente
            cmd.append(s)

            p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            x = p.communicate()[0]
            p.stdin.close()

            print("Caso o cliente só tenha enviado o ficheiro assinado (.sig)")
            print("Deseja verificar o HMAC (y/n)")

            m = str(input())
            
            aux = False
            if(m == 'y'):
                aux = True

            if(flag_assi == False and aux == True):
                
                print("\n\n----Verificacao de ficheiro corrupto----\n\n")
                
                f_hash = FOLDER_AGENTE+".hash/"
                name = str(input("Introduza o nome do cliente que enviou o ficheiro: "))
                dirlist = os.listdir(FOLDER_AGENTE+".hash/")
                
                for i in range(len(dirlist)):
                    aux =dirlist[i].split('_',1)
                    if(aux[0] == name):
                        f_hash = f_hash + aux[0]+"_hash.sha256"

                with open(f_hash, 'rb') as f:
                    h1 = f.read()

                name_v = str(input("Introduza o nome do ficheiro a verificar: "))

                f_hmac = os.path.join(FOLDER_AGENTE+"."+cliente+"/",'tmp.sha256')
                hmac1 = open(f_hmac, 'w')
                
                cmd = 'openssl dgst -sha256 -hmac'.split()
                cmd.append(h1)
                cmd.append(FOLDER_AGENTE+"."+cliente+"/"+name_v)

                p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=hmac1)
                x = p.communicate()[0]
                p.stdin.close()

                x2 = name_v.split('.',2)
                if(len(x2)>2):
                    x1 = x2[0]+'.'+x2[1]

                with open(os.path.join(FOLDER_AGENTE+"."+cliente+"/",x1+'.sha256'), 'r') as f:
                    f1 = f.read()
                aux_f1 = f1.split("=",2)

                with open(f_hmac, 'r') as f:
                    f2 = f.read()
                aux_f2 = f2.split("=",2)

                if(aux_f1[1] == aux_f2[1]):
                    print("\nFicheiro Inalterado!\n")
                else:
                    print("\nFicheiro Corrupto!\n")

            #Mostra quais são os ficheiros na pasta do cliente
            cmd = 'ls -a'.split()
            s = ".agente/."+cliente
            cmd.append(s)

            p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            x = p.communicate()[0]
            p.stdin.close()

            print("\nIntroduza '0' para sair!")
            while(True):
                f = str(input("Ficheiro a enviar: "))
                if(f == '0'):
                    break
                else:
                    files = f
                    moveto_cliente(cliente,files)
        else:
            print("O Cliente nao existe ou nao esta ligado ao sistema!")
        lfile.close()
    else:
        print("\nSistema so funciona com pelo menos 2 clientes ligados!")

#Menu Login
#Cria a Chave de Sessao (uma nova a cada login efetuado pelo Cliente) e envia para o Agente
def chavesSessao():
    f2 = open(FOLDER_CLIENTE+"."+LOGIN_USER+"/chaveSessao.txt", "w+")
    chaveSess = random.getrandbits(128)
    f2.write(str(chaveSess))
    f2.close()
    
    chave = str(input("Introduza uma chave: "))
    output1 = open(FOLDER_CLIENTE+"."+LOGIN_USER+"/cryptoSessao.pem",'w+')

    cmd = 'openssl enc -aes128 -K'.split()

    cmd.append(chave)
    cmd.append('-in')
    cmd.append(FOLDER_CLIENTE+"."+LOGIN_USER+"/chaveSessao.txt")
    cmd.append('-iv')
    cmd.append('0')

    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=output1)
    x = p.communicate()[0]
    p.stdin.close()

    #Envia para o Agente de Confianca
    send_file = os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/",'cryptoSessao.pem')
    dir_agente = os.path.join(FOLDER_AGENTE,LOGIN_USER+'.pem')

    cmd = 'cp'.split()
    cmd.append(send_file)
    cmd.append(dir_agente)

    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    x = p.communicate()[0]
    p.stdin.close()

    #Decifra a chave de sessao
    output2 = open(os.path.join(FOLDER_AGENTE,LOGIN_USER+"Sessao.txt"),'w+')
    cmd = 'openssl enc -aes128 -d -K'.split()

    cmd.append(chave)
    cmd.append('-in')
    cmd.append(FOLDER_AGENTE+LOGIN_USER+'.pem')
    cmd.append('-iv')
    cmd.append('0')

    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=output2)
    x = p.communicate()[0]
    p.stdin.close()

def listClientesLigados():
    print("\n__Lista de Clientes Ligados__\n")
    
    #Abre o ficheiro para leitura
    f1 = open("ligados.txt","r")
    #A funcao mode verifica se o ficheiro foi aberto
    if(f1.mode == "r"):
        t = f1.readlines()
        for i in t:
            print("         "+i.replace('\n',''))

def registarC():
    usernameC = str(input("Username: "))
    passwordC = str(input("Password: "))
    aux_str = usernameC + "_" + passwordC

    #Abre o ficheiro para leitura (verificacao se user ja existe)
    f1 = open(os.path.join(FOLDER_AGENTE,"login.txt"),"r")
    flag_existe = True

    #Abre o ficheiro para adicionar conteudo
    f2 = open(os.path.join(FOLDER_AGENTE,"login.txt"),"a+")

    #A funcao mode verifica se o ficheiro foi aberto
    if(f1.mode == "r"):
        t = f1.readlines()
        for i in t:
            text = i.replace('\n','').split('_',1)
            if(usernameC == text[0]):
                flag_existe = False
                print("\nEste Username ja existe!")
                break

    if(flag_existe):
        f2.write(aux_str+'\n')
        dir_cliente = FOLDER_CLIENTE+"."+usernameC+"/"
        dir_user = FOLDER_AGENTE+"."+usernameC+"/"

        #Cria as pastas necessarias para o funcionamento do cliente
        os.mkdir(dir_user)
        os.mkdir(dir_cliente)
        os.mkdir(dir_cliente+"Enviado")
        os.mkdir(dir_cliente+"Recebido")

        key = RSA.generate(2048)
        private_key = key.exportKey()

        #Ficheiro da chave privada na pasta do cliente
        f_key_private = open(os.path.join(dir_cliente,"key_private.pem"),"wb")
        f_key_private.write(private_key)
        f_key_private.close()

        #Ficheiros da chave publica na pasta do cliente e do agente
        public_key = key.publickey().exportKey()

        f_key_public1 = open(os.path.join(dir_cliente,"key_public.pem"),"wb")
        f_key_public3 = open(os.path.join(FOLDER_CLIENTE+"key/",usernameC+".pem"),"wb")
        
        f_key_public1.write(public_key)
        f_key_public3.write(public_key)
        
        f_key_public1.close()
        f_key_public3.close()

    f1.close()
    f2.close()

def loginC():
    usernameC = str(input("Username: "))
    passwordC = str(input("Password: "))
    aux_str = usernameC + "_" + passwordC
    
    #Abre o ficheiro para leitura (verificacao se user ja existe)
    f1 = open(os.path.join(FOLDER_AGENTE,"login.txt"),"r")
    flag_existe = False

    #Verifica se o utilizador ja esta ligado ao sistema noutro local
    flag_loginE = False

    f = open("ligados.txt", "r")
    t =  f.readlines()

    for i in t:
        if(usernameC == i.replace('\n','')):
            flag_loginE = True
    
    if(flag_loginE == False):
        f2 = open("ligados.txt", "a+")
        #Permite guardar na variavel global o username do cliente que efetuou login
        global LOGIN_USER

        #A funcao mode verifica se o ficheiro foi aberto
        if(f1.mode == "r"):
            t = f1.readlines()
            for i in t:
                text = i.replace('\n','').replace('[','').replace(']','')
                if(aux_str == text):
                    flag_existe = True
                    LOGIN_USER = usernameC
                    f2.write(usernameC+'\n')
                    #Cria a Chave de Sessao
                    chavesSessao()
                    break

    return flag_existe,flag_loginE

#Menu Cliente
def verFicheirosR():
    #Cria uma lista com o nome dos ficheiros presentes no diretorio do user que efetuou login
    dirlist = os.listdir(FOLDER_CLIENTE+"."+LOGIN_USER+"/Recebido/")
    if(len(dirlist) > 0):
        print("\nFicheiros:\n")
        for i in range(len(dirlist)):
            print(dirlist[i])
    else:
        print("\nNão foi recebido nenhum ficheiro!\n")

def lerFicheiro():
    #Mostra quais são os ficheiros na pasta do cliente
    cmd = 'ls -a'.split()
    s = FOLDER_CLIENTE+'.'+LOGIN_USER+"/Recebido"
    cmd.append(s)

    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    x = p.communicate()[0]
    p.stdin.close()
    if(len(os.listdir(FOLDER_CLIENTE+"."+LOGIN_USER+"/Recebido/"))>0):
        f = str(input("Ficheiro a ler: "))
        aux = f.split('.',4)
        f_dir = FOLDER_CLIENTE+'.'+LOGIN_USER+"/Recebido/"+f

        if(aux[1] == "aes" or aux[2] == "aes"):
            output1 = open(FOLDER_CLIENTE+"."+LOGIN_USER+"/Recebido/file.txt", 'w+')
            #Le o ficheiro assinado
            cmd = 'openssl rsautl -verify -inkey'.split()
            k_pub = FOLDER_CLIENTE+"."+LOGIN_USER+"/Recebido/pk.pem"
            
            cmd.append(k_pub)
            cmd.append('-pubin')
            cmd.append('-in')
            cmd.append(f_dir)

            p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=output1)
            x = p.communicate()[0]
            p.stdin.close()

            #Decifrar com a chave de sessao do cliente que enviou
            output2 = open(os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/Recebido/","file.txt-2"),'w+')
            cmd = 'openssl enc -aes128 -d -K'.split()

            f = open(os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/","chaveSessao.txt"),'r')
            
            cmd.append(f.read())
            cmd.append('-in')
            cmd.append(FOLDER_CLIENTE+"."+LOGIN_USER+"/Recebido/file.txt")
            cmd.append('-iv')
            cmd.append('0')

            p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=output2)
            x = p.communicate()[0]
            p.stdin.close()

            #Imprime o ficheiro no terminal
            print()
            cmd = 'cat'.split()
            cmd.append(FOLDER_CLIENTE+"."+LOGIN_USER+"/Recebido/file.txt-2")

            p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            x = p.communicate()[0]
            p.stdin.close()
        else:
            output1 = open(FOLDER_CLIENTE+"."+LOGIN_USER+"/Recebido/file.txt", 'w+')
            #Le o ficheiro assinado
            cmd = 'openssl rsautl -verify -inkey'.split()
            k_pub = FOLDER_CLIENTE+"."+LOGIN_USER+"/Recebido/pk.pem"
            
            cmd.append(k_pub)
            cmd.append('-pubin')
            cmd.append('-in')
            cmd.append(f_dir)

            p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=output1)
            x = p.communicate()[0]
            p.stdin.close()

            #Imprime o ficheiro no terminal
            print()
            cmd = 'cat'.split()
            cmd.append(FOLDER_CLIENTE+"."+LOGIN_USER+"/Recebido/file.txt")

            p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            x = p.communicate()[0]
            p.stdin.close()
    else:
        print("Não tem ficheiros para ler!")

#Inputs: Ficheiro a retirar o hash; ficheiro a guardar;
def cal_hash(file_t,fhash):
    sigoutput = open(fhash, 'w')

    cmd = 'openssl dgst -sha256'.split()
    cmd.append(file_t)

    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=sigoutput)
    x = p.communicate()[0]
    p.stdin.close()

def cifrarCliente():
    output2 = open(os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/Enviado/",LOGIN_USER+"_"+FILE_NAME+".aes"),'w+')
    cmd = 'openssl enc -aes128 -e -K'.split()

    f = open(FOLDER_CLIENTE+"."+LOGIN_USER+"/chaveSessao.txt",'r')

    cmd.append(f.read())
    cmd.append('-in')
    cmd.append(FOLDER_CLIENTE+"."+LOGIN_USER+"/Enviado/"+FILE_NAME)
    cmd.append('-iv')
    cmd.append('0')

    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=output2)
    x = p.communicate()[0]
    p.stdin.close()
    f.close()

    return True

def assinarC(flag_cifrar):
    if(flag_cifrar == False):
        #Calcular o hash e guardar num ficheiro
        fhash = os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/"+"Enviado/",'hash.sha256')
        cal_hash(os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/"+"Enviado/",FILE_NAME),fhash)

        #Assinar
        private_key = os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/","key_private.pem")
        f_sign = os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/"+"Enviado/",FILE_NAME+'.sig')
        sigoutput1 = open(f_sign, 'w')
        
        cmd = 'openssl rsautl -sign -in'.split()
        cmd.append(os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/"+"Enviado/",FILE_NAME))
        cmd.append('-inkey')
        cmd.append(private_key)

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=sigoutput1)
        x = p.communicate()[0]
        p.stdin.close()

        #Calcular o hash para o HMAC
        fhash_sig = os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/"+"Enviado/",'hash_sig.sha256')
        cal_hash(f_sign,fhash_sig)

        f_hmac = os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/"+"Enviado/",FILE_NAME+'.sha256')
        hmac1 = open(f_hmac, 'w')

        with open(fhash_sig, 'rb') as f:
            h1 = f.read()

        cmd = 'openssl dgst -sha256 -hmac'.split()
        cmd.append(h1)
        cmd.append(f_sign)

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=hmac1)
        x = p.communicate()[0]
        p.stdin.close()

        dir_agente = os.path.join(FOLDER_AGENTE+".hash/",LOGIN_USER+"_hash.sha256")

        cmd = 'cp'.split()
        cmd.append(fhash_sig)
        cmd.append(dir_agente)

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        x = p.communicate()[0]
        p.stdin.close()
    else:
        #Assinar com o Ficheiro Cifrado
        private_key = os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/","key_private.pem")
        f_sign = os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/"+"Enviado/",FILE_NAME+'.sig')
        sigoutput1 = open(f_sign, 'w')
        
        cmd = 'openssl rsautl -sign -in'.split()
        cmd.append(os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/"+"Enviado/",LOGIN_USER+"_"+FILE_NAME+'.aes'))
        cmd.append('-inkey')
        cmd.append(private_key)

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=sigoutput1)
        x = p.communicate()[0]
        p.stdin.close()
        
    print("\nDone\n")
    return True

#Funcao auxiliar envia ficheiros para o agente de confianca, copiando-os
def copyto_agente(cliente,file1):
    send_file = os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/Enviado/",file1)
    dir_agente = os.path.join(FOLDER_AGENTE+"."+cliente+"/",file1)

    cmd = 'cp'.split()
    cmd.append(send_file)
    cmd.append(dir_agente)

    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    x = p.communicate()[0]
    p.stdin.close()

#Funcao envia ficheiros para o Agente
def sendf(flag_cifrar,flag_assinar):
    f = open("ligados.txt", "r")
    t =  f.readlines()

    if(len(t) > 1):
        listClientesLigados()
        cliente = str(input("\nCliente a Enviar: "))
        flag_existe = False

        #Verifica se o cliente esta ligado ao sistema
        for i in t:
            if(cliente == i.replace('\n','')):
                flag_existe = True
        
        if(flag_existe):
            if(flag_cifrar == False and flag_assinar == True):
                file_sig = FILE_NAME+'.sig'
                copyto_agente(cliente,file_sig)

                file_hmac = FILE_NAME+'.sha256'
                copyto_agente(cliente,file_hmac)

                send_file = os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/",'key_public.pem')
                dir_agente = os.path.join(FOLDER_AGENTE+"."+cliente+"/",'pk.pem')

                cmd = 'cp'.split()
                cmd.append(send_file)
                cmd.append(dir_agente)

                p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                x = p.communicate()[0]
                p.stdin.close()
            elif(flag_cifrar == True and flag_assinar == False):
                file_sig = LOGIN_USER+'_'+FILE_NAME+'.aes'
                copyto_agente(cliente,file_sig)
            
            elif(flag_cifrar == True and flag_assinar == True):
                file_sig = LOGIN_USER+"_"+FILE_NAME+'.aes'
                copyto_agente(cliente,file_sig)
                file_sig = FILE_NAME+'.sig'
                copyto_agente(cliente,file_sig)

                send_file = os.path.join(FOLDER_CLIENTE+"."+LOGIN_USER+"/",'key_public.pem')
                dir_agente = os.path.join(FOLDER_AGENTE+"."+cliente+"/",'pk.pem')

                cmd = 'cp'.split()
                cmd.append(send_file)
                cmd.append(dir_agente)

                p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                x = p.communicate()[0]
                p.stdin.close()

            print("\nDone\n")
        else:
            print("\nO cliente nao existe na Lista!")
            print("O Ficheiro nao foi enviado!")
    else:
        print("\nSistema so funciona com pelo menos 2 clientes ligados!")
    f.close()

if __name__ == '__main__':
    while(True):
        #Menu Principal
        menu1()
        n1 = opcao_input()
        if(n1 == 1):
            flag_assi = False
            while(True):
                #Menu Agente de Confianca
                menu2()
                n2 = opcao_input()
                if(n2 == 1):
                    listClientesRegistados()
                elif(n2 == 2):
                    flag_assi = assinarA()
                elif(n2 == 3):
                    key = RSA.generate(2048)
                    private_key = key.exportKey()

                    #Ficheiro da chave privada na pasta do cliente
                    f_key_private = open(os.path.join(FOLDER_AGENTE,"key_private.pem"),"wb")
                    f_key_private.write(private_key)
                    f_key_private.close()

                    #Ficheiros da chave publica na pasta do cliente e do agente
                    public_key = key.publickey().exportKey()

                    f_key_public1 = open(os.path.join(FOLDER_AGENTE,"key_public.pem"),"wb")
                    f_key_public3 = open(os.path.join(FOLDER_CLIENTE+"key/","agente.pem"),"wb")
                    
                    f_key_public1.write(public_key)
                    f_key_public3.write(public_key)
                    
                    f_key_public1.close()
                    f_key_public3.close()
                    print("\nDone\n")
                elif(n2 == 4):
                    send(flag_assi)
                elif(n2 == 0):
                    break
                else:
                    opcao_inv()
        elif(n1 == 2):
            while(True):
                #Menu Cliente (Login, Registo)
                menu3()
                n3 = opcao_input()
                if(n3 == 1):
                    registarC()
                elif(n3 == 2):
                    login, existe = loginC()
                    if(login):
                        while(True):
                            #Menu Cliente
                            menu4()
                            n4 = opcao_input()
                            if(n4 == 1):
                                #Enviar Ficheiro; Imprime os ficheiros na pasta, prontos a serem enviados
                                dirlist = os.listdir(FOLDER_CLIENTE+"."+LOGIN_USER+"/Enviado/")
                                print("\nFicheiros:\n")
                                for i in range(len(dirlist)):
                                    print(dirlist[i])

                                FILE_NAME = str(input("\nIntroduza o nome do ficheiro a Cifrar/Assinar: "))
                                flag_cifrar = False
                                flag_assinar = False
                                while(True):
                                    #Menu Enviar Ficheiro
                                    menu5()
                                    n5 = opcao_input()
                                    if(n5 == 1):
                                        flag_cifrar = cifrarCliente()
                                    elif(n5 == 2):
                                        flag_assinar = assinarC(flag_cifrar)
                                    elif(n5 == 3):
                                        sendf(flag_cifrar,flag_assinar)
                                    elif(n5 == 0):
                                        break
                                    else:
                                        opcao_inv()
                            elif(n4 == 2):
                                verFicheirosR()
                            elif(n4 == 3):
                                lerFicheiro()
                            elif(n4 == 0):
                                f = open("ligados.txt", "r")
                                t =  f.readlines()
                                aux = []

                                for i in t:
                                    if(LOGIN_USER != i.replace('\n','')):
                                        aux.append(i)

                                #Limpa o ficheiro dos ligados
                                f_new = open('ligados.txt',"w")
                                f_new.close()
                                #Abre em 'append' o "novo" ficheiro de ligados
                                f_new = open('ligados.txt',"a")

                                for x in range(len(aux)):
                                    f_new.write(aux[x])

                                f_new.close()
                                f.close()
                                break
                            else:
                                opcao_inv()
                    else:
                        if(existe):
                            print("\nO utilizador tem sessao ligada noutro local!\n")
                        else:
                            print("\nUsername ou Password Errados!")
                elif(n3 == 0):
                    break
                else:
                    opcao_inv()
        elif(n1 == 0):
            break
        else:
            opcao_inv()
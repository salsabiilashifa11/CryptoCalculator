import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QFileDialog
from RSA import RSA
from Paillier import Paillier
from ecc.ecc import *
from elgamal.elgamal import *
from keyUtil import *
from textUtil import *
import cv2

#---------------------------------UTILITIES---------------------------------
def goBack():
    # widget.setCurrentIndex(widget.currentIndex() - 1)
    widget.removeWidget(widget.currentWidget())

#---------------------------------HOME---------------------------------
class HomeScreen(QDialog):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi("UI/main.ui", self)

        self.pushButton.clicked.connect(self.goToRSA)
        self.pushButton_2.clicked.connect(self.goToElGamal)
        self.pushButton_3.clicked.connect(self.goToPaillier)
        self.pushButton_4.clicked.connect(self.goToECC)

    def goToElGamal(self):
        image = ElGamalScreen()
        widget.addWidget(image)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToECC(self):
        ecc = ECCScreen()
        widget.addWidget(ecc)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToPaillier(self):
        paillier = paillierScreen()
        widget.addWidget(paillier)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToRSA(self):
        rsa = rsaScreen()
        widget.addWidget(rsa)
        widget.setCurrentIndex(widget.currentIndex()+1)
    

#---------------------------------RSA---------------------------------
class rsaScreen(QDialog):
    def __init__(self):
        super(rsaScreen, self).__init__()
        loadUi("UI/RSA/RSA-main.ui", self)

        self.pushButton.clicked.connect(self.goToRSAEncrypt)
        self.pushButton_2.clicked.connect(self.goToRSADecrypt)
        self.backButton.clicked.connect(goBack)

    def goToRSAEncrypt(self):
        rsa1 = rsaEncryptScreen()
        widget.addWidget(rsa1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToRSADecrypt(self):
        rsa1 = rsaDecryptScreen()
        widget.addWidget(rsa1)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class rsaEncryptScreen(QDialog):
    def __init__(self):
        super(rsaEncryptScreen, self).__init__()
        loadUi("UI/RSA/RSA-encrypt.ui", self)
        self.mode = "encrypt"
        self.messagePath = ""
        self.P = None
        self.Q = None
        self.E = None
        self.n = None
        self.message = ""
        self.fileInputMethod = ""
        self.keyInputMethod = ''
        self.outputPath = ""
        self.random = False
        self.keyboard = False


        #actions
        self.inputButton_1.toggled.connect(self.toggleInputButton1)
        self.inputButton_2.toggled.connect(self.toggleInputButton2)
        self.inputButton_4.toggled.connect(self.toggleInputButton4)
        self.inputButton_3.toggled.connect(self.toggleInputButton3)
        self.inputButton_5.toggled.connect(self.toggleInputButton5)
        self.messageFileButton.clicked.connect(self.browseMessage)
        self.keyFileButton.clicked.connect(self.browseKey)
        self.goButton.clicked.connect(self.runEncrypt)
        self.backButton.clicked.connect(goBack)

    def browseMessage(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop', '*.txt')
        self.inputFileField.setText(f[0])
        self.messagePath = f[0]
    
    def browseKey(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop', '*.pub')
        self.inputFileField_2.setText(f[0])
        self.messagePath = f[0]

    def toggleInputButton1(self): self.btnInputState(self.inputButton_1)
    def toggleInputButton2(self): self.btnInputState(self.inputButton_2)

    def toggleInputButton5(self) : self.KeyInputState(self.inputButton_5)
    def toggleInputButton4(self) : self.KeyInputState(self.inputButton_4)
    def toggleInputButton3(self) : self.KeyInputState(self.inputButton_3)

    def btnInputState(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.messageFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.messageFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")

    def KeyInputState(self, b):
        if b.text() == "Random":
            if b.isChecked():
                self.Factor1KeyField.setReadOnly(True)
                self.Factor2KeyField.setReadOnly(True)
                self.PublicKeyField.setReadOnly(True)
                self.keyInputMethod = "Random"
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.Factor1KeyField.setReadOnly(False)
                self.Factor2KeyField.setReadOnly(False)
                self.PublicKeyField.setReadOnly(False)
                self.keyInputMethod = "Keyboard"
        elif b.text() == "File":
                self.Factor1KeyField.setReadOnly(True)
                self.Factor2KeyField.setReadOnly(True)
                self.PublicKeyField.setReadOnly(True)
                self.keyInputMethod = "File"

    def getMessage(self):
        if (self.fileInputMethod == "File"):
            msgPath = self.inputFileField.text()
            f = open(msgPath, "rb")
            self.message = (f.read())
            f.close()
        else:
            self.message = self.inputKeyboardField.text()

    def getKey(self):
        if (self.keyInputMethod == "File"):
            keyPath = self.inputFileField_2.text()
            f = open(keyPath, 'r')
            self.key = f.read().split(' ')
            f.close()

    def getOutputPath(self):
        self.outputPathKey = "save/rsa/key/" + self.KeyFileName.text() 
        self.outputPathCipher = "save/rsa/enc/" + self.KeyFileName.text() + '.txt'

    def runEncrypt(self):
        self.getMessage()
        self.getOutputPath()
        self.getKey()

        print(self.message)
        self.rsa = RSA()
        if (self.keyInputMethod == 'Random'):
            self.rsa.generateKeyPair()
        elif (self.keyInputMethod == 'File'):
            self.rsa.e = int(self.key[0])
            self.rsa.n = int(self.key[1])
        else:
            P = int(self.Factor1KeyField.text())
            Q = int(self.Factor2KeyField.text())
            E = int(self.PublicKeyField.text())
            print(P)
            print(Q)
            print(E)
            self.rsa.generateKeyPair(int(P), int(Q), int(E))
        
        if self.fileInputMethod == 'Keyboard':
            self.message = bytes(self.message, 'utf-8')

        ct, cts = self.rsa.encrypt(self.message, self.rsa.e, self.rsa.n)
        
        f = open(self.outputPathCipher, 'w')
        f.write(cts)
        f.close()

        self.messageOutput.setText(cts)
        self.messageOutput.setReadOnly(True)

        saveKeyRSA(self.rsa.e, self.rsa.n, self.rsa.d, self.outputPathKey)



class rsaDecryptScreen(QDialog):
    def __init__(self):
        super(rsaDecryptScreen, self).__init__()
        loadUi("UI/RSA/RSA-decrypt.ui", self)
        self.mode = "decrypt"
        self.outputPath = ""
        self.messagePath = ""
        self.P = None
        self.Q = None
        self.E = None
        self.n = None
        self.cipher = ""
        self.fileInputMethod = ""
        self.keyInputMethod = ''
        self.random = False
        self.keyboard = False

        #actions
        self.goButton.clicked.connect(self.runDecrypt)
        self.backButton.clicked.connect(goBack)
        self.inputButton_1.toggled.connect(self.toggleInputButton1)
        self.inputButton_2.toggled.connect(self.toggleInputButton2)
        self.inputButton_4.toggled.connect(self.toggleInputButton4)
        self.inputButton_3.toggled.connect(self.toggleInputButton3)
        self.keyFileButton.clicked.connect(self.browseKey)
        self.messageFileButton.clicked.connect(self.browseCipher)

    def browseCipher(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop', '*.txt')
        self.inputFileField.setText(f[0])
        self.messagePath = f[0]

    def browseKey(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop', '*.pri')
        self.inputFileField_2.setText(f[0])
        self.messagePath = f[0]
    
    def toggleInputButton1(self): self.btnInputState(self.inputButton_1)
    def toggleInputButton2(self): self.btnInputState(self.inputButton_2)

    def toggleInputButton4(self) : self.KeyInputState(self.inputButton_4)
    def toggleInputButton3(self) : self.KeyInputState(self.inputButton_3)

    def btnInputState(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.messageFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.messageFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")

    def KeyInputState(self, b):
        if b.text() == "Keyboard":
            if b.isChecked():
                self.publicKeyField.setReadOnly(False)
                self.privateKeyField.setReadOnly(False)
                self.keyInputMethod = "Keyboard"
        elif b.text() == "File":
                self.publicKeyField.setReadOnly(True)
                self.privateKeyField.setReadOnly(True)
                self.keyInputMethod = "File"

    def getCipher(self):
        if (self.fileInputMethod == "File"):
            msgPath = self.inputFileField.text()
            f = open(msgPath, "r")
            string = f.read()
            self.cipher = string
            f.close()
        else:
            self.cipher = self.inputKeyboardField.text()

    def getOutputPath(self):
        self.outputPath = "Keys/" + self.KeyFileName.text() 

    def getKey(self):
        if (self.keyInputMethod == "File"):
            keyPath = self.inputFileField_2.text()
            f = open(keyPath, 'r')
            self.key = f.read().split(' ')
            f.close()

    def runDecrypt(self):
        self.getCipher()
        self.getOutputPath()
        self.getKey()

        print(self.cipher)
        self.rsa = RSA()
        if (self.keyInputMethod == 'File'):
            self.rsa.d = self.key[0]
            self.rsa.n = self.key[1]
        else:
            d = self.privateKeyField.text()
            n = self.publicKeyField.text()

            self.rsa.d = int(d)
            self.rsa.n = int(n)

        

        print(self.cipher)
        # Preprocess the cipher
        cipher = cipher2IntArr(str(self.cipher), (len(str(self.rsa.n))))

        pt = self.rsa.decrypt(cipher, int(self.rsa.d), int(self.rsa.n))

        self.messageOutput.setText(str(pt))
        self.messageOutput.setReadOnly(True)





#---------------------------------Paillier---------------------------------
class paillierScreen(QDialog):
    def __init__(self):
        super(paillierScreen, self).__init__()
        loadUi("UI/Paillier/Paillier-main.ui", self)

        self.pushButton.clicked.connect(self.goToPaillierEncrypt)
        self.pushButton_2.clicked.connect(self.goToPaillierDecrypt)
        self.backButton.clicked.connect(goBack)

    def goToPaillierEncrypt(self):
        paillier1 = paillierEncryptScreen()
        widget.addWidget(paillier1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToPaillierDecrypt(self):
        paillier1 = paillierDecryptScreen()
        widget.addWidget(paillier1)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class paillierEncryptScreen(QDialog):
    def __init__(self):
        super(paillierEncryptScreen, self).__init__()
        loadUi("UI/Paillier/Paillier-encrypt.ui", self)
        self.mode = "encrypt"
        self.messagePath = ''
        self.P = None
        self.Q = None
        self.g = None
        self.message = ""
        self.fileInputMethod = ""
        self.outputPath = ""
        self.random = False
        self.seed = 0

        #actions
        self.inputButton_1.toggled.connect(self.toggleInputButton1)
        self.inputButton_2.toggled.connect(self.toggleInputButton2)
        self.messageFileButton.clicked.connect(self.browseMessage)
        self.inputButton_4.toggled.connect(self.toggleInputButton4)
        self.inputButton_3.toggled.connect(self.toggleInputButton3)
        self.inputButton_5.toggled.connect(self.toggleInputButton5)
        self.keyFileButton.clicked.connect(self.browseKey)
        self.goButton.clicked.connect(self.runEncrypt)
        self.backButton.clicked.connect(goBack)

    def browseMessage(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/darubagus/Desktop', '*.txt')
        self.inputFileField.setText(f[0])
        self.messagePath = f[0]

    def browseKey(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop', '*.pub')
        self.inputFileField_2.setText(f[0])
        self.messagePath = f[0]

    def toggleInputButton1(self): self.btnInputState(self.inputButton_1)
    def toggleInputButton2(self): self.btnInputState(self.inputButton_2)

    def toggleInputButton5(self) : self.KeyInputState(self.inputButton_5)
    def toggleInputButton4(self) : self.KeyInputState(self.inputButton_4)
    def toggleInputButton3(self) : self.KeyInputState(self.inputButton_3)

    def btnInputState(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.messageFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.messageFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")
    
    def KeyInputState(self, b):
        if b.text() == "Random":
            if b.isChecked():
                self.Factor1KeyField.setReadOnly(True)
                self.Factor2KeyField.setReadOnly(True)
                self.PublicKeyField.setReadOnly(True)
                self.keyInputMethod = "Random"
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.Factor1KeyField.setReadOnly(False)
                self.Factor2KeyField.setReadOnly(False)
                self.PublicKeyField.setReadOnly(False)
                self.keyInputMethod = "Keyboard"
        elif b.text() == "File":
                self.Factor1KeyField.setReadOnly(True)
                self.Factor2KeyField.setReadOnly(True)
                self.PublicKeyField.setReadOnly(True)
                self.keyInputMethod = "File"

    def getMessage(self):
        if (self.fileInputMethod == "File"):
            msgPath = self.inputFileField.text()
            f = open(msgPath, "rb")
            self.message = (f.read())
            f.close()
        else:
            self.message = self.inputKeyboardField.text()

    def getKey(self):
        if (self.keyInputMethod == "File"):
            keyPath = self.inputFileField_2.text()
            f = open(keyPath, 'rb')
            self.key = f.read().split(' ')
            f.close()

    def getOutputPath(self):
        self.outputPathKey = "save/paillier/key/" + self.KeyFileName.text()
        self.outputPathCipher = "save/paillier/enc/" + self.KeyFileName.text() + '.txt'

    def runEncrypt(self):
        self.getMessage()
        self.getOutputPath()
        self.getKey()

        # print(self.message)
        self.Paillier = Paillier()
        if (self.keyInputMethod == 'Random'):
            self.Paillier.generateKeyPair()
        elif (self.keyInputMethod == 'File'):
            self.Paillier.g = self.key[0]
            self.Paillier.n = self.key[1]
        else:
            P = self.Factor1KeyField.text()
            Q = self.Factor2KeyField.text()
            G = self.PublicKeyField.text()
            print(P)
            print(Q)
            print(G)
            self.Paillier.generateKeyPair(int(P), int(Q), int(G))
        
        ct, cts = self.Paillier.encrypt(self.message, self.Paillier.g)

        f = open(self.outputPathCipher, 'w')
        f.write(cts)
        f.close()

        self.messageOutput.setText(cts)
        self.messageOutput.setReadOnly(True)

        saveKeyPaillier(self.Paillier.n, self.Paillier.g, self.Paillier.miu, self.Paillier.lmd, self.outputPathKey)
    

class paillierDecryptScreen(QDialog):
    def __init__(self):
        super(paillierDecryptScreen, self).__init__()
        loadUi("UI/Paillier/paillier-decrypt.ui", self)
        self.mode = "decrypt"
        self.messagePath = ""
        self.outputPath = ""
        self.cipher = ''
        self.n = None
        self.D = None
        self.random = False


        #actions
        self.goButton.clicked.connect(self.runDecrypt)
        self.backButton.clicked.connect(goBack)
        self.inputButton_1.toggled.connect(self.toggleInputButton1)
        self.inputButton_2.toggled.connect(self.toggleInputButton2)
        self.inputButton_4.toggled.connect(self.toggleInputButton4)
        self.inputButton_3.toggled.connect(self.toggleInputButton3)
        self.keyFileButton.clicked.connect(self.browseKey)
        self.messageFileButton.clicked.connect(self.browseCipher)

    def browseCipher(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop', '*.txt')
        self.inputFileField.setText(f[0])
        self.messagePath = f[0]

    def browseKey(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop', '*.pri')
        self.inputFileField_2.setText(f[0])
        self.messagePath = f[0]

    def toggleInputButton1(self): self.btnInputState(self.inputButton_1)
    def toggleInputButton2(self): self.btnInputState(self.inputButton_2)

    def toggleInputButton4(self) : self.KeyInputState(self.inputButton_4)
    def toggleInputButton3(self) : self.KeyInputState(self.inputButton_3)

    def btnInputState(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.messageFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.messageFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")

    def KeyInputState(self, b):
        if b.text() == "Keyboard":
            if b.isChecked():
                self.nKeyField.setReadOnly(False)
                self.lambdaKeyField.setReadOnly(False)
                self.miuKeyField.setReadOnly(False)
                self.keyInputMethod = "Keyboard"
        elif b.text() == "File":
                self.nKeyField.setReadOnly(True)
                self.lambdaKeyField.setReadOnly(True)
                self.miuKeyField.setReadOnly(True)
                self.keyInputMethod = "File"

    def getCipher(self):
        if (self.fileInputMethod == "File"):
            msgPath = self.inputFileField.text()
            f = open(msgPath, "r")
            self.cipher = f.read()
            f.close()
        else:
            self.message = self.inputKeyboardField.text()

    def getOutputPath(self):
        self.outputPath = "Keys/" + self.KeyFileName.text() 

    def getKey(self):
        if (self.keyInputMethod == "File"):
            keyPath = self.inputFileField_2.text()
            f = open(keyPath, 'r')
            self.key = f.read().split(' ')
            f.close()

    def runDecrypt(self):
        self.getCipher()
        self.getOutputPath()
        self.getKey()

        print(self.cipher)
        self.Paillier = Paillier()
        if (self.keyInputMethod == 'File'):
            self.Paillier.lmd = self.key[0]
            self.Paillier.miu = self.key[1]
            self.Paillier.n = self.key[2]
        else:
            n = self.nKeyField.text()
            l = self.lambdaKeyField.text()
            m = self.miuKeyField.text()

            self.Paillier.n = int(n)
            self.Paillier.lmd = int(l)
            self.Paillier.miu = int(m)
        
        print(self.cipher)

        # Preprocess the cipher
        cipher = cipher2IntArr(self.cipher, len(str(pow(int(self.Paillier.n), 2))))
        print(cipher)
        pt = self.Paillier.decrypt(cipher, int(self.Paillier.lmd), int(self.Paillier.miu), int(self.Paillier.n))

        self.messageOutput.setText(pt)
        self.messageOutput.setReadOnly(True)


#---------------------------------ECC---------------------------------

class ECCScreen(QDialog):
    def __init__(self):
        super(ECCScreen, self).__init__()
        loadUi("UI/ECC/ECC-main.ui", self)

        self.pushButton.clicked.connect(self.goToECCEncrypt)
        self.pushButton_2.clicked.connect(self.goToECCDecrypt)
        self.pushButton_3.clicked.connect(self.goToECCKeyGen)
        self.backButton.clicked.connect(goBack)

    def goToECCEncrypt(self):
        ecc = ECCEncryptScreen()
        widget.addWidget(ecc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToECCDecrypt(self):
        ecc = ECCDecryptScreen()
        widget.addWidget(ecc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToECCKeyGen(self):
        ecc = ECCKeyGenScreen()
        widget.addWidget(ecc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class ECCEncryptScreen(QDialog):
    def __init__(self):
        super(ECCEncryptScreen, self).__init__()
        loadUi("UI/ECC/ECC-encrypt.ui", self)
        self.mode = "encrypt"
        self.message = ""
        self.outputPath = ""
        self.key = ""
        self.curve = ""

        #actions
        self.inputButton_1.toggled.connect(self.toggleInputButton1) #file message
        self.inputButton_2.toggled.connect(self.toggleInputButton2) #keyboard message
        self.messageFileButton.clicked.connect(self.browseInput) #browse message
        self.curveEquationFileButton.clicked.connect(self.browseCurve)
        self.publicKeyFileButton.clicked.connect(self.browseKey)
        self.goButton.clicked.connect(self.runEncryption) #encrypt
        self.backButton.clicked.connect(goBack)

    def browseInput(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop')
        self.inputFileField.setText(f[0])

    def browseCurve(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop')
        self.curveFileField.setText(f[0])

    def browseKey(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop')
        self.keyFileField.setText(f[0])

    def toggleInputButton1(self): self.btnInputState(self.inputButton_1)
    def toggleInputButton2(self): self.btnInputState(self.inputButton_2)

    def btnInputState(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.messageFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.messageFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")

    def btn2InputState(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.curveEquationFileButton.setEnabled(True)
                self.publicKeyFileButton.setEnabled(True)
                self.paramInputMethod = "File"

    def getMessage(self):
        if (self.fileInputMethod == "File"):
            path = self.inputFileField.text()
            f = open(path, "r")
            self.message = f.read()
        else:
            self.message = self.inputKeyboardField.text()
    
    def getKey(self):
        path = self.keyFileField.text()
        self.key = read_key(path)

    def getCurve(self):
        path = self.curveFileField.text()
        self.curve = read_curve(path)

    def getK(self):
        self.k = int(self.encodingKeyField.text())

    def getOutputPath(self):
        self.outputPathKey = "save/ecc/key/" + self.outputFileField.text() + ".pub"
        self.outputPathCurve = "save/ecc/curve/" + self.outputFileField.text() + "-curve.txt" 
        self.outputPathCipher = "save/ecc/enc/" + self.outputFileField.text() + "-cipher.txt" 

    def runEncryption(self):
        self.getMessage()
        self.getCurve()
        self.getKey()
        self.getK()
        self.getOutputPath()

        print(self.curve)
        print(self.key)
        result = encrypt(self.curve[0], self.curve[1], self.curve[2], self.curve[3], self.key, self.k, self.message)
        save_enc(result, self.outputPathCipher)

        printText = "%s" % (result,)
        self.messageOutput.setText(printText)

        
class ECCDecryptScreen(QDialog):
    def __init__(self):
        super(ECCDecryptScreen, self).__init__()
        loadUi("UI/ECC/ECC-decrypt.ui", self)
        self.mode = "decrypt"
        self.message = ""
        self.outputPath = ""
        self.key = ""

        #actions
        self.messageFileButton.clicked.connect(self.browseInput) #browse message
        self.curveEquationFileButton.clicked.connect(self.browseCurve)
        self.privateKeyFileButton.clicked.connect(self.browseKey)
        self.goButton.clicked.connect(self.runDecryption) #decrypt
        self.backButton.clicked.connect(goBack)

    def browseInput(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop')
        self.inputFileField.setText(f[0])

    def browseCurve(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop')
        self.curveFileField.setText(f[0])

    def browseKey(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop')
        self.keyFileField.setText(f[0])

    def getMessage(self):
        self.message = read_enc(self.inputFileField.text())

    def getKey(self):
        path = self.keyFileField.text()
        self.key = read_key(path)

    def getCurve(self):
        path = self.curveFileField.text()
        self.curve = read_curve(path)

    def getK(self):
        self.k = int(self.encodingKeyField.text())

    def runDecryption(self):
        self.getMessage()
        self.getCurve()
        self.getKey()
        self.getK()
        
        result = decrypt(self.curve[0], self.curve[1], self.curve[2], self.curve[3], self.key, self.k, self.message)
        self.messageOutput.setText(result)

class ECCKeyGenScreen(QDialog):
    def __init__(self):
        super(ECCKeyGenScreen, self).__init__()
        loadUi("UI/ECC/ECC-keygen.ui", self)
        self.mode = "encrypt"
        self.message = ""
        self.outputPath = ""
        self.key = ""
        self.curve = ""

        #actions
        self.curveEquationFileButton.clicked.connect(self.browseCurve)
        self.goButton.clicked.connect(self.runGenerateKey) #generate key
        self.goButton_2.clicked.connect(self.runGenerateCurve) #generate curve
        self.backButton.clicked.connect(goBack)

    def browseCurve(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop')
        self.curveFileField.setText(f[0])

    def getCurve(self):
        path = self.curveFileField.text()
        self.curve = read_curve(path)

    def runGenerateCurve(self):
        path = self.outputCurveFileField.text()
        curve_generator(16, path)
    
    def runGenerateKey(self):
        path = self.outputKeyFileField.text()
        self.getCurve()
        key_generator(self.curve[0], self.curve[1], self.curve[2], self.curve[3], 8, path)

#---------------------------------El Gamal---------------------------------

class ElGamalScreen(QDialog):
    def __init__(self):
        super(ElGamalScreen, self).__init__()
        loadUi("UI/ElGamal/ElGamal-main.ui", self)

        self.pushButton.clicked.connect(self.goToElGamalEncrypt)
        self.pushButton_2.clicked.connect(self.goToElGamalDecrypt)
        self.pushButton_3.clicked.connect(self.goToElGamalKeyGen)
        self.backButton.clicked.connect(goBack)

    def goToElGamalEncrypt(self):
        ecc = ElGamalEncryptScreen()
        widget.addWidget(ecc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToElGamalDecrypt(self):
        ecc = ElGamalDecryptScreen()
        widget.addWidget(ecc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToElGamalKeyGen(self):
        ecc = ElGamalKeyGenScreen()
        widget.addWidget(ecc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class ElGamalEncryptScreen(QDialog):
    def __init__(self):
        super(ElGamalEncryptScreen, self).__init__()
        loadUi("UI/ElGamal/ElGamal-encrypt.ui", self)
        self.mode = "encrypt"
        self.message = ""
        self.outputPath = ""
        self.key = ""
        self.curve = ""

        #actions
        self.inputButton_1.toggled.connect(self.toggleInputButton1) #file message
        self.inputButton_2.toggled.connect(self.toggleInputButton2) #keyboard message
        self.messageFileButton.clicked.connect(self.browseInput) #browse message
        self.goButton.clicked.connect(self.runEncryption) #encrypt
        self.backButton.clicked.connect(goBack)

    def browseInput(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop')
        self.inputFileField.setText(f[0])

    def toggleInputButton1(self): self.btnInputState(self.inputButton_1)
    def toggleInputButton2(self): self.btnInputState(self.inputButton_2)

    def btnInputState(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.messageFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.messageFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")

    def getMessage(self):
        if (self.fileInputMethod == "File"):
            path = self.inputFileField.text()
            f = open(path, "r")
            self.message = f.read()
        else:
            self.message = self.inputKeyboardField.text()
    
    def getKey(self):
        self.key = (int(self.yKeyField.text()), int(self.gKeyField.text()), int(self.pKeyField.text()))

    def getOutputPath(self):
        # self.outputPathKey = "save/ecc/key/" + self.outputFileField.text() + ".pub"
        # self.outputPathCurve = "save/ecc/curve/" + self.outputFileField.text() + "-curve.txt" 
        self.outputPathCipher = "save/elGamal/enc/" + self.outputFileField.text() + "-cipher.txt" 

    def runEncryption(self):
        self.getMessage()
        self.getKey()
        self.getOutputPath()

        result = elgamal_encrypt(self.message, self.key[0], self.key[1], self.key[2])
        elgamal_save_enc(result, self.outputPathCipher)

        printText = "%s" % (result,)
        self.messageOutput.setText(printText)
        
class ElGamalDecryptScreen(QDialog):
    def __init__(self):
        super(ElGamalDecryptScreen, self).__init__()
        loadUi("UI/ElGamal/ElGamal-decrypt.ui", self)
        self.mode = "decrypt"
        self.message = ""
        self.outputPath = ""
        self.key = ""

        #actions
        self.messageFileButton.clicked.connect(self.browseInput) #browse message
        self.goButton.clicked.connect(self.runDecryption) #decrypt
        self.backButton.clicked.connect(goBack)

    def browseInput(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop')
        self.inputFileField.setText(f[0])

    def getMessage(self):
        self.message = elgamal_read_enc(self.inputFileField.text())

    def getKey(self):
        self.key = (int(self.privateXField.text()), int(self.privatePField.text()))

    def runDecryption(self):
        self.getMessage()
        self.getKey()
        
        result = elgamal_decrypt(self.message, self.key[0], self.key[1])
        self.messageOutput.setText(result)

class ElGamalKeyGenScreen(QDialog):
    def __init__(self):
        super(ElGamalKeyGenScreen, self).__init__()
        loadUi("UI/ElGamal/ElGamal-keygen.ui", self)
        self.mode = "encrypt"
        self.message = ""
        self.outputPath = ""
        self.key = ""
        self.curve = ""

        #actions
        self.goButton.clicked.connect(self.runGenerateKey) #generate key
        self.backButton.clicked.connect(goBack)
    
    def runGenerateKey(self):
        path = self.outputKeyFileField.text()
        elgamal_generate_key(32, path)

#main
app = QApplication(sys.argv)
widget = QStackedWidget()

home = HomeScreen()

widget.addWidget(home)
widget.setFixedWidth(1201)
widget.setFixedHeight(821)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
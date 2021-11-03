import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QFileDialog
from RSA import RSA
from Paillier import Paillier
from keyUtil import *
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
        self.pushButton_2.clicked.connect(self.goToImage)
        self.pushButton_3.clicked.connect(self.goToPaillier)

    def goToImage(self):
        image = ImageScreen()
        widget.addWidget(image)
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
            f = open(keyPath, 'rb')
            self.key = f.read().split(' ')
            f.close()

    def getOutputPath(self):
        self.outputPath = "Keys/" + self.KeyFileName.text() 

    def runEncrypt(self):
        self.getMessage()
        self.getOutputPath()
        self.getKey()

        print(self.message)
        self.rsa = RSA()
        if (self.keyInputMethod == 'Random'):
            self.rsa.generateKeyPair()
        elif (self.keyInputMethod == 'File'):
            self.rsa.e = self.key[0]
            self.rsa.n = self.key[1]
        else:
            P = self.Factor1KeyField.text()
            Q = self.Factor2KeyField.text()
            E = self.PublicKeyField.text()
            print(P)
            print(Q)
            print(E)
            self.rsa.generateKeyPair(int(P), int(Q), int(E))

        ct, cts = self.rsa.encrypt(self.message, self.rsa.e, self.rsa.n)

        print(cts)
        

        self.messageOutput.setText(cts)
        self.messageOutput.setReadOnly(True)

        saveKeyRSA(self.rsa.e, self.rsa.n, self.rsa.d, self.outputPath)



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
            f = open(msgPath, "rb")
            self.cipher = (f.read())
            f.close()
        else:
            self.message = self.inputKeyboardField.text()

    def getOutputPath(self):
        self.outputPath = "Keys/" + self.KeyFileName.text() 

    def getKey(self):
        if (self.keyInputMethod == "File"):
            keyPath = self.inputFileField_2.text()
            f = open(keyPath, 'rb')
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

        # Preprocess the cipher
        cipher = ''

        pt = self.rsa.decrypt(cipher, self.rsa.d, self.rsa.n)

        self.messageOutput.setText(pt)
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
        self.outputPath = "Keys/" + self.KeyFileName.text()

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

        self.messageOutput.setText(cts)
        self.messageOutput.setReadOnly(True)

        saveKeyPaillier(self.Paillier.n, self.Paillier.g, self.Paillier.miu, self.Paillier.lmd, self.outputPath)
    

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
            f = open(msgPath, "rb")
            self.cipher = (f.read())
            f.close()
        else:
            self.message = self.inputKeyboardField.text()

    def getOutputPath(self):
        self.outputPath = "Keys/" + self.KeyFileName.text() 

    def getKey(self):
        if (self.keyInputMethod == "File"):
            keyPath = self.inputFileField_2.text()
            f = open(keyPath, 'rb')
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
        
        # Preprocess the cipher
        cipher = ''

        pt = self.Paillier.decrypt(cipher, self.Paillier.lmd, self.Paillier.miu, self.Paillier.n)

        self.messageOutput.setText(pt)
        self.messageOutput.setReadOnly(True)


#---------------------------------RC4---------------------------------

class RC4Screen(QDialog):
    def __init__(self):
        super(RC4Screen, self).__init__()
        loadUi("UI/RC4/rc4-main.ui", self)

        self.pushButton.clicked.connect(self.goToRC4Encrypt)
        self.pushButton_2.clicked.connect(self.goToRC4Decrypt)
        self.backButton.clicked.connect(goBack)

    def goToRC4Encrypt(self):
        rc1 = RC4EncryptScreen()
        widget.addWidget(rc1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToRC4Decrypt(self):
        rc1 = RC4DecryptScreen()
        widget.addWidget(rc1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class RC4EncryptScreen(QDialog):
    def __init__(self):
        super(RC4EncryptScreen, self).__init__()
        loadUi("UI/RC4/rc4-encrypt.ui", self)
        self.mode = "encrypt"
        self.message = ""
        self.outputPath = ""
        self.key = ""

        #actions
        self.inputButton_1.toggled.connect(self.toggleInputButton1)
        self.inputButton_2.toggled.connect(self.toggleInputButton2)
        self.inputFileButton.clicked.connect(self.browseInput)
        self.goButton.clicked.connect(self.runEncoding)
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
                self.inputFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.inputFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")

    def getMessage(self):
        if (self.fileInputMethod == "File"):
            path = self.inputFileField.text()
            self.message = readfile_bin(path)
        else:
            self.message = self.inputKeyboardField.text()

    def getOutputPath(self):
        self.outputPath = "output_encode/" + self.outputFileField.text() + "." + self.outputFormatField.text()

    def runEncoding(self):
        self.getMessage()
        self.getOutputPath()
        self.key = self.stegoKeyField.text()
        acquire_key(self.key)
        result = encrypt_text(self.message)
        writefile_bin(self.outputPath, result)

        self.gotToResult()

    def gotToResult(self):
        filename = self.outputFileField.text() + "." + self.outputFormatField.text()
        result = RC4ResultScreen(self.mode, filename, "")
        widget.addWidget(result)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class RC4DecryptScreen(QDialog):
    def __init__(self):
        super(RC4DecryptScreen, self).__init__()
        loadUi("UI/RC4/rc4-decrypt.ui", self)
        self.mode = "decrypt"
        self.message = ""
        self.outputPath = ""
        self.key = ""

        #actions
        self.inputButton_1.toggled.connect(self.toggleInputButton1)
        self.inputButton_2.toggled.connect(self.toggleInputButton2)
        self.inputFileButton.clicked.connect(self.browseInput)
        self.goButton.clicked.connect(self.runDecoding)
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
                self.inputFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.inputFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")

    def getMessage(self):
        if (self.fileInputMethod == "File"):
            path = self.inputFileField.text()
            self.message = readfile_bin(path)
        else:
            self.message = self.inputKeyboardField.text()

    def getOutputPath(self):
        self.outputPath = "output_decode/" + self.outputFileField.text() + "." + self.outputFormatField.text()

    def runDecoding(self):
        self.getMessage()
        self.getOutputPath()
        self.key = self.stegoKeyField.text()
        acquire_key(self.key)
        result = decrypt_text(self.message)
        writefile_bin(self.outputPath, result)

        self.gotToResult()

    def gotToResult(self):
        filename = self.outputFileField.text() + "." + self.outputFormatField.text()
        result = RC4ResultScreen(self.mode, filename, "")
        widget.addWidget(result)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class RC4ResultScreen(QDialog):
    def __init__(self, _mode, _resultFileName, _psnr):
        super(RC4ResultScreen, self).__init__()
        loadUi("UI/RC4/rc4-result.ui", self)
        self.label.setText((_mode+"ed").capitalize())
        self.fileNameLabel.setText(_resultFileName)
        self.psnrLabel.setText(_psnr)

        #actions
        self.goButton.clicked.connect(self.goToHome)

    def goToHome(self):
        for i in range(3):
            goBack()

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
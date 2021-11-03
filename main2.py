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
        self.pushButton_3.clicked.connect(self.goToAudio)

    def goToImage(self):
        image = ImageScreen()
        widget.addWidget(image)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToAudio(self):
        audio = AudioScreen()
        widget.addWidget(audio)
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
        rsa1 = ImageDecodeScreen()
        widget.addWidget(rsa1)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class rsaEncryptScreen(QDialog):
    def __init__(self):
        super(rsaEncryptScreen, self).__init__()
        loadUi("UI/RSA/RSA-encrypt.ui", self)
        self.mode = "encrypt"
        self.messagePath = ""
        self.message = ""
        self.fileInputMethod = ""
        self.keyInputMethod = ''
        self.outputPath = ""
        self.random = False
        self.keyboard = False
        # self.outputMessage.setReadOnly(True)

        #actions
        # self.vesselButton.clicked.connect(self.browseVessel)
        self.inputButton_1.toggled.connect(self.toggleInputButton1)
        self.inputButton_2.toggled.connect(self.toggleInputButton2)
        self.inputButton_4.toggled.connect(self.toggleInputButton4)
        self.inputButton_3.toggled.connect(self.toggleInputButton3)
        self.messageFileButton.clicked.connect(self.browseMessage)
        self.goButton.clicked.connect(self.runEncrypt)
        self.backButton.clicked.connect(goBack)

    def browseMessage(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop', '*.txt')
        self.inputFileField.setText(f[0])
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
        if b.text() == "Random":
            if b.isChecked():
                self.Factor1KeyField.setReadOnly(True)
                self.Factor2KeyField.setReadOnly(True)
                self.PublicKeyField.setReadOnly(True)
                self.keyInputMethod = "Random"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.Factor1KeyField.setReadOnly(False)
                self.Factor2KeyField.setReadOnly(False)
                self.PublicKeyField.setReadOnly(False)
                self.keyInputMethod = "Keyboard"
                self.inputFileField.setText("")    

    def getMessage(self):
        if (self.fileInputMethod == "File"):
            msgPath = self.inputFileField.text()
            f = open(msgPath, "rb")
            self.message = (f.read())
            f.close()
        else:
            self.message = self.inputKeyboardField.text()

    def getOutputPath(self):
        self.outputPath = "Keys/" + self.KeyFileName.text() 

    def runEncrypt(self):
        self.getMessage()
        self.getOutputPath()
        self.getMessage()
        print(self.message)
        self.rsa = RSA()
        if (self.keyInputMethod == 'Random'):
            self.rsa.generateKeyPair()
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



class rsaDecryptScreen(QDialog):
    def __init__(self):
        super(rsaDecryptScreen, self).__init__()
        loadUi("UI/RSA/RSA-decrypt.ui", self)
        self.mode = "decrypt"
        self.vesselPath = ""
        self.outputPath = ""
        self.random = False
        self.decrypt = False
        self.seed = 0

        #actions
        self.vesselButton.clicked.connect(self.browseVessel)
        self.goButton.clicked.connect(self.runDecoding)
        self.backButton.clicked.connect(goBack)
        self.encButton_1.clicked.connect(self.toggleEncButton1)
        self.encButton_2.clicked.connect(self.toggleEncButton2)

    def browseVessel(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop', '*.png *.bmp')
        self.vesselField.setText(f[0])
        self.vesselPath = f[0]
    
    def toggleEncButton1(self): self.btnEncryptionState(self.encButton_1)
    def toggleEncButton2(self): self.btnEncryptionState(self.encButton_2)

    def btnEncryptionState(self, b):
        if b.text() == "Yes":
            if b.isChecked():
                self.decrypt = True
    
    def decryptMessage(self):
        if self.decrypt:
            acquire_key(self.stegoKeyField.text())
            # Decrypt output file
            cr4_decrypt_file(self.outputFileField.text(), self.outputFormatField.text())

    def btnInsertionState(self, b):
        if b.text() == "Sequential":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(True)
                self.stegoKeyField.setText("")
        elif b.text() == "Random":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(False)

    def getRandom(self):
        if self.stegoKeyField.text() != "":
            self.random = True
            self.seed = (int(''.join(map(str, map(ord, self.stegoKeyField.text()))))) % (2**32 - 1)

    def runDecoding(self):
        self.getRandom()

        decode(self.vesselPath, self.outputFileField.text(), self.outputFormatField.text(), self.random, self.seed)
        self.decryptMessage()
        print("All decoded")
        self.gotToResult()

    def gotToResult(self):
        filename = self.outputFileField.text() + "." + self.outputFormatField.text()
        pnsr = ""
        result = ImageResultScreen(self.mode, filename, pnsr)
        widget.addWidget(result)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class ImageResultScreen(QDialog):
    def __init__(self, _mode, _resultFileName, _psnr):
        super(ImageResultScreen, self).__init__()
        loadUi("UI/image/image-result.ui", self)
        self.label.setText((_mode+"d").capitalize())
        self.fileNameLabel.setText(_resultFileName)
        self.psnrLabel.setText(_psnr)

        #actions
        self.goButton.clicked.connect(self.goToHome)

    def goToHome(self):
        for i in range(3):
            goBack()

#---------------------------------AUDIO---------------------------------
class AudioScreen(QDialog):
    def __init__(self):
        super(AudioScreen, self).__init__()
        loadUi("UI/audio/audio-main.ui", self)

        self.pushButton.clicked.connect(self.goToAudioEncode)
        self.pushButton_2.clicked.connect(self.goToAudioDecode)
        self.backButton.clicked.connect(goBack)

    def goToAudioEncode(self):
        audioEncode = AudioEncodeScreen()
        widget.addWidget(audioEncode)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToAudioDecode(self):
        audioDecode = AudioDecodeScreen()
        widget.addWidget(audioDecode)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class AudioEncodeScreen(QDialog):
    def __init__(self):
        super(AudioEncodeScreen, self).__init__()
        loadUi("UI/audio/audio-encode.ui", self)
        self.mode = "encode"
        self.vesselPath = ""
        self.message = ""
        self.fileInputMethod = ""
        self.outputPath = ""
        self.random = False
        self.seed = 0
        self.audioEncode = ""
        self.modifiedFrame = ""

        #actions
        self.vesselButton.clicked.connect(self.browseVessel)
        self.inputButton_1.toggled.connect(self.toggleInputButton1)
        self.inputButton_2.toggled.connect(self.toggleInputButton2)
        self.inputFileButton.clicked.connect(self.browseInput)
        self.insButton_1.clicked.connect(self.toggleInsButton1)
        self.insButton_2.clicked.connect(self.toggleInsButton2)
        self.goButton.clicked.connect(self.runEncoding)
        self.backButton.clicked.connect(goBack)

    def browseVessel(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/darubagus/Desktop', '*.wav')
        self.vesselField.setText(f[0])
        self.vesselPath = f[0]

    def browseInput(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/darubagus/Desktop')
        self.inputFileField.setText(f[0])

    def toggleInputButton1(self): self.btnInputState(self.inputButton_1)
    def toggleInputButton2(self): self.btnInputState(self.inputButton_2)
    def toggleInsButton1(self): self.btnInsertionState(self.insButton_1)
    def toggleInsButton2(self): self.btnInsertionState(self.insButton_2)

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

    def btnInsertionState(self, b):
        if b.text() == "Sequential":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(True)
                self.stegoKeyField.setText("")
        elif b.text() == "Random":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(False)

    def getBinaryMessage(self):
        if (self.fileInputMethod == "File"):
            self.msgPath = self.inputFileField.text()
            # msg = File(path)
            # self.message = msg.readFile()
            # self.message = file2bin(path)
        else:
            plaintext = self.inputKeyboardField.text()
            self.msgPath = 'message/message.txt'
            msg = File(self.msgPath)
            msg.writeTextFile(plaintext)
            # self.message = str2bin(plaintext)

    def getOutputPath(self):
        self.outputPath = "output_encode/" + self.outputFileField.text() + ".wav" 

    def getRandom(self):
        if self.insButton_2.isChecked():
            self.random = True
            self.seed = self.stegoKeyField.text()
        else:
            self.random = False
            self.seed = ''

    def runEncoding(self):
        self.getBinaryMessage()
        self.getOutputPath()
        self.getRandom()
        # get encrypt

        # encode(self.message, self.vesselPath, self.outputPath, self.random, self.seed)
        self.audioEncode = EncodeAudio(self.vesselPath, self.msgPath, self.seed)
        self.modifiedFrame = self.audioEncode.encodeAudio(self.random, False)
        # print(self.modifiedFrame)
        

        self.gotToResult()

    def gotToResult(self):
        filename = self.outputFileField.text() + ".wav"
        path = 'output_encode/' + filename
        output = File(path)
        output.writeAudioFile(self.modifiedFrame, self.audioEncode.metadata)
        pnsr = str(psnr(self.vesselPath, self.outputPath)) + ' dB'
        result = AudioResultScreen(self.mode, filename, pnsr)
        widget.addWidget(result)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class AudioDecodeScreen(QDialog):
    def __init__(self):
        super(AudioDecodeScreen, self).__init__()
        loadUi("UI/audio/audio-decode.ui", self)
        self.mode = "decode"
        self.vesselPath = ""
        self.outputPath = ""
        self.random = False
        self.seed = 0
        self.decodeAudio = ""

        #actions
        self.vesselButton.clicked.connect(self.browseVessel)
        self.goButton.clicked.connect(self.runDecoding)
        self.backButton.clicked.connect(goBack)

    def browseVessel(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/darubagus/Desktop', '*.wav')
        self.vesselField.setText(f[0])
        self.vesselPath = f[0]

    def btnInsertionState(self, b):
        if b.text() == "Sequential":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(True)
                self.stegoKeyField.setText("")
        elif b.text() == "Random":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(False)

    def getRandom(self):
        if self.stegoKeyField.text() != "":
            self.random = True
            self.seed = self.stegoKeyField.text()
        else :
            self.random = False
            self.seed = ''

    def runDecoding(self):
        self.getRandom()

        # decode(self.vesselPath, self.outputFileField.text(), self.outputFormatField.text(), self.random, self.seed)
        self.decodeAudio = DecodeAudio(self.vesselPath, self.seed)
        # self.decodeAudio.decode()
        # self.decodeAudio.parseMsg()
        print("All decoded")
        self.gotToResult()

    def gotToResult(self):
        self.decodeAudio.decode()
        self.decodeAudio.parseMsg()
        filename = self.outputFileField.text() + "." + self.decodeAudio.extension
        path = 'output_decode/' + filename
        
        byte = self.decodeAudio.getDecodedMsg()
        output = File(path)
        output.writeFile(byte)

        pnsr = ""
        result = AudioResultScreen(self.mode, filename, pnsr)
        widget.addWidget(result)
        widget.setCurrentIndex(widget.currentIndex() + 1)
class AudioResultScreen(QDialog):
    def __init__(self, _mode, _resultFileName, _psnr):
        super(AudioResultScreen, self).__init__()
        loadUi("UI/audio/audio-result.ui", self)
        self.label.setText((_mode+"d").capitalize())
        self.fileNameLabel.setText(_resultFileName)
        self.psnrLabel.setText(_psnr)

        #actions
        self.goButton.clicked.connect(self.goToHome)

    def goToHome(self):
        for i in range(3):
            goBack()

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
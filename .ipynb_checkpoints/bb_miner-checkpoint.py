#!/usr/bin/env python
# coding: utf-8

# In[8]:


from pdf2image import convert_from_path
import PyPDF2 
import textract
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pdftotext
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import re


# In[10]:


root = Tk()
root.title("Minerador - Boletos BB")
root.minsize(500,500)
root.filename = filedialog.askopenfilename(initialdir = "../data/samples", title = "Escolha o arquivo:", filetypes=(("Arquivos PDF", "*.pdf"),))


# In[118]:


# filename = "../data/NF_BOLETOS_SETEMBRO_2019/25_SETEMBRO_2019/POLICONT_REC.TRIBUTOS.pdf"
# Load your PDF
with open(root.filename, "rb") as f:
    pdf = pdftotext.PDF(f)
text = ("".join(pdf))
lines = text.splitlines()


# In[119]:


#The word_tokenize() function will break our text phrases into #individual words
tokens = word_tokenize(text)
#we'll create a new list which contains punctuation we wish to clean
punctuations = ['(',')',';','[',']',':',',','.','-','--']
#We initialize the stopwords variable which is a list of words like #"The", "I", "and", etc. that don't hold much value as keywords
stop_words = stopwords.words('portuguese')
#We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
keywords = [word for word in tokens if not word.lower() in stop_words and not word in punctuations]


# In[122]:


for i in range(3, len(keywords)):
    if (keywords[i-1].lower() == 'pagamento' and keywords[i-2].lower() == 'data'):
        data = keywords[i]
    if (keywords[i-1].lower() == "convenio"):
        cliente = ''
        j = 0
        while(1):
            cliente = cliente + " " + (keywords[i+j])
            j+=1
            if (keywords[i+j].lower() == 'codigo' or j > 5):
                break
    if (keywords[i-1].lower() == "fantasia" and keywords[i-2].lower() == 'nome'):
        cliente = ''
        j = 0
        while(1):
            cliente = cliente + " " + (keywords[i+j])
            j+=1
            if (keywords[i+j].lower() == 'cnpj' or j > 5):
                break
    if (keywords[i-1].lower() == 'agencia'):
        agencia = keywords[i]
    if (keywords[i-1].lower() == 'conta'):
        conta = keywords[i]
    if (keywords[i-2].lower() == 'valor'):
        valor = keywords[i]

fileLastName = root.filename.split("/")[-1]
notaFiscal = re.findall(r"NF\d+|nf\d+|\d+", fileLastName)

# In[123]:

result = "Extrato bancario;"+data+";"+valor+";2059;1174;VR PAGO REF FORNECEDOR"+cliente+" NF "+notaFiscal[-1]
images  = convert_from_path(root.filename)
img     = images[0]
myImage = ImageTk.PhotoImage(img.resize((1000,1000)))
label0  = Label(root, text = result).pack()
label1  = Label(root, image = myImage).pack()
root.mainloop()


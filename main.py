import os
from pdfminer.high_level import extract_text
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
import re

# constant
PATH_DIR = 'input'
PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')



def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)


def extract_names(txt):
    person_names = []
    for sent in nltk.sent_tokenize(txt):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(' '.join(chunk_leave[0] for chunk_leave in chunk.leaves()))

    return person_names

def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)
    if phone:
        number = ''.join(phone[0])
        return number
        # if resume_text.find(number) >= 0 and len(number) < 16:
        #     return number
    return None


def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)
 

onlyfiles = [os.path.join(PATH_DIR, f) for f in os.listdir(PATH_DIR) if os.path.isfile(os.path.join(PATH_DIR, f))]
for x in onlyfiles:
    dataCV = extract_text_from_pdf(x)
    names = extract_names(dataCV)
    phone = extract_phone_number(dataCV)
    emails = extract_emails(dataCV)
    print(names)
    print(phone)
    print(emails)

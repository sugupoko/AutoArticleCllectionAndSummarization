# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from googletrans import Translator

# ======================== Parameters ============================

# folder path
folderPath = './computational_imaging/'

# select algorithm
# LSA or KL
ALGORITHM = 'LSA'

# For summarizer
LANGUAGE = "english"
SENTENCES_COUNT = 10


# ======================== Summarizer ============================

# Summarize Strategy pattern
class Summarize:
    def __init__(self, formatter, inputText):
        self.inputText = inputText
        self.SummarizedText = ''
        self.formatter = formatter

    def SummarizeText(self):
        self.SummarizedText = self.formatter.SummarizeText(self)


# 抽象化したクラス(抽象戦略)
class SummarizerFormatterStrategy:
    def SummarizeText(self, input):
        raise Exception('Called abstract method !!')


# LsaSummarizer(具体戦略)
class LsaSummarizer(SummarizerFormatterStrategy):
    def SummarizeText(self, input):
        text = input.inputText
        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        from sumy.summarizers.lsa import LsaSummarizer
        summarizer = LsaSummarizer(stemmer)

        summarizer.stop_words = get_stop_words(LANGUAGE)
        summrizedText = ''
        # summarize =============================================
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            summrizedText = summrizedText + str(sentence) + '\n'

        return summrizedText


# KlSummarizer(具体戦略)
class KlSummarizer(SummarizerFormatterStrategy):
    def SummarizeText(self, input):
        text = input.inputText
        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)

        from sumy.summarizers.kl import KLSummarizer
        summarizer = KLSummarizer(stemmer)

        summarizer.stop_words = get_stop_words(LANGUAGE)
        summrizedText = ''
        # summarize =============================================
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            summrizedText = summrizedText + str(sentence) + '\n'

        return summrizedText


# ======================== Converter ============================


def convert_pdf_to_txt(path_name):
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
    from io import StringIO
    #
    rsrcmgr = PDFResourceManager()

    # setting
    outfp = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    laparams.detect_vertical = True
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)

    # open
    fp = open(path_name + '.pdf', 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # transform
    for page in PDFPage.get_pages(fp, pagenos=None, maxpages=0, password=None, caching=True,
                                  check_extractable=True):
        interpreter.process_page(page)

    fp.close()
    device.close()

    # save as text file
    convertedText = outfp.getvalue()
    outfp.close()

    # transform specific character
    convertedText = convertedText.replace("ﬁ", "fi")
    convertedText = convertedText.replace("ﬂ", "fl")
    convertedText = convertedText.replace("“", '"')
    convertedText = convertedText.replace("”", '"')

    return convertedText


# ======================== in/out ============================


def openTextFile(path_name):
    # input file
    f = open(path_name + '.txt', 'r', encoding="utf-8")
    data = f.read()
    f.close()
    return data


def saveStringAsTextFile(path, strings):
    make_new_text_file = open(path + '.txt', 'w', encoding="utf-8")
    make_new_text_file.write(strings)
    make_new_text_file.close()
    return


# ======================== Main ============================

if __name__ == "__main__":
    import os

    # make directory
    fileList = os.listdir(folderPath)
    output = folderPath + 'Output/'
    if not os.path.exists(output):
        os.mkdir(output)

    # create path
    outputText = output + 'textfile/'
    OutputSentence = output + 'SentencesCount_' + str(SENTENCES_COUNT) + '/'
    OutputFolder = OutputSentence + str(ALGORITHM) + '/'
    savePathEng = OutputFolder + 'summarizedTextByEng/'
    savePathJap = OutputFolder + 'summarizedTextByJap/'

    # make subDirectory
    if not os.path.exists(OutputSentence):
        os.mkdir(OutputSentence)
    if not os.path.exists(OutputFolder):
        os.mkdir(OutputFolder)
    if not os.path.exists(outputText):
        os.mkdir(outputText)
    if not os.path.exists(savePathEng):
        os.mkdir(savePathEng)
    if not os.path.exists(savePathJap):
        os.mkdir(savePathJap)

    # start
    for file in fileList:
        print('\n\n')
        base, ext = os.path.splitext(file)
        print(base)
        if ext == '.pdf':
            Input_path = folderPath + base

            # Pdf to Text =======================
            if not os.path.exists(outputText + base + '.txt'):
                print('Pdf to Text start')
                text = convert_pdf_to_txt(Input_path)
            else:
                # openTextFile
                text = openTextFile(outputText + base)

            # Summarization =======================
            if not os.path.exists(savePathEng + base + '.txt'):
                print('Summarization start')
                # アルゴリズム選択 KL or LSA
                if ALGORITHM == 'LSA':
                    Summarizer = Summarize(LsaSummarizer(), text)
                elif ALGORITHM == 'KL':
                    Summarizer = Summarize(KlSummarizer(), text)

                Summarizer.SummarizeText()
                summarizedText = Summarizer.SummarizedText
            else:
                summarizedText = openTextFile(savePathEng + base)

            # Translate =======================
            if not os.path.exists(savePathJap + base + '.txt'):
                translator = Translator()
                translations = translator.translate(summarizedText, dest='ja')
                print(translations.text)

            # Save files =======================
            if not os.path.exists(outputText + base + '.txt'):
                saveStringAsTextFile(outputText + base, text)
            if not os.path.exists(savePathEng + base + '.txt'):
                saveStringAsTextFile(savePathEng + base, summarizedText)
            if not os.path.exists(savePathJap + base + '.txt'):
                saveStringAsTextFile(savePathJap + base, translations.text)

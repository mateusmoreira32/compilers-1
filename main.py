import unittest
from main import toInt

class TesteVerificarToInt(unittest.TestCase):
    def teste_correto(self):
        self.assertEqual(toInt('1243') + 1,1244)
        self.assertEqual(toInt('311') + 5 ,316)
        self.assertEqual(toInt('10') -1, 9)
 class TesteVerificarData(unittest.TestCase):
    def test_invalid_dates(self):
        DatasInvalidas = [
            'qwcascasc'
            '11/ca/1999']
        for DatasInvalidas in DatasInvalidas:
            self.assertFalse(verificar_data(DatasInvalidas))
    def teste_validar(self):
        validarDatas = [
            '12/11/10'
            '11/10/21'
            '12/06/13']
        for validarDatas in validarDatas:
            self.assertTrue(verificar_data(DatasInvalidas))
  class test_invalid_emails(self):
    def test_invalid_emails(self):
        invalidarEmails = [
            'mat-@mail.com',
            'mat..@mail.com',
            '.mat@mail.com',
            'mat#@mail.com',
            'mat.def@mail.com',
            'mat.def@mail.c',
            'mat.def@mail#archive.com'
        ]
        for invalidarEmail in invalidarEmails:
            self.assertFalse(verificar_email(invalidarEmail))
    def test_validar_emails(self):
        validarEmails = [
            'mat-d@mail.com',
            'mat.def@mail.com',
            'mat@mail.com',
            'mat_def@mail.com',
            'mat.def@mail.com',
        ]
        for validarEmail in validarEmails:
            self.asserttrue(verificar_email(validarEmail))
            

import csv
from operator import attrgetter

class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = int(anno_acquisto)
        self.valore = float(valore)

    def __str__(self):
        return f'[{self.codice}], {self.tipo} - {self.marca} ({self.anno_acquisto}) - {self.valore:.2f} euro'


class Prestito:
    def __init__(self, codice_prestito, data, id_strumento, cognome_allievo):
        self.codice_prestito = codice_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

        def __str__(self):
            return f'[{self.codice_prestito}] Data: {self.data}, Strumento: {self.id_strumento}, Allievo: {self.cognome_allievo}'


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.__responsabile = responsabile
        self.strumenti = {} # DIZIONARIO: {codice: oggetto strumento}
        self.prestiti = {} # DIZIONARIO: {codice_prestito: oggetto prestito}
        self.contatore_prestiti = 1

    @property
    def responsabile(self):
        return self.__responsabile

    @responsabile.setter
    def responsabile(self, nuovo_responsabile):
        self.__responsabile = nuovo_responsabile


    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, "r", encoding='utf-8') as file:
                reader = csv.DictReader(file, fieldnames=['C1', 'C2', 'C3', 'C4', 'C5'])
                for record in reader:
                    codice = record['C1']
                    tipo = record['C2']
                    marca = record['C3']
                    anno_acquisto = record['C4']
                    valore = record['C5']

                    # salvo strumento nel dizionario
                    self.strumenti[codice] = Strumento(codice, tipo, marca, anno_acquisto, valore)

        except FileNotFoundError:
            return None


    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        max_num = 0
        for codice in self.strumenti.keys(): # calcolo nuovo codice
            if codice.startswith('S'):
                num = int(codice[1:])
                if num > max_num:
                    max_num = num

        nuovo_codice = f'S{max_num + 1}'
        nuovoS = Strumento(nuovo_codice, tipo, marca, anno_acquisto, valore)
        self.strumenti[nuovo_codice] = nuovoS

        return nuovoS


    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        lista_strumenti = list(self.strumenti.values())
        # ordinamento mediante l'uso di attregetter sulla proprietà 'marca'
        return sorted(lista_strumenti, key=attrgetter('marca'))


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        # verifico se lo strumento esiste nel sistema
        if id_strumento not in self.strumenti:
            return None
        # verifico se lo strumento è già in prestito
        for prestito in self.prestiti.values():
            if prestito.id_strumento == id_strumento:
                return None

        codiceP = f'P{self.contatore_prestiti}'
        self.contatore_prestiti += 1

        nuovoP = Prestito(codiceP, data, id_strumento, cognome_allievo)
        self.prestiti[codiceP] = nuovoP
        return nuovoP


    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        if id_prestito in self.prestiti:
            del self.prestiti[id_prestito]
        else:
            return None
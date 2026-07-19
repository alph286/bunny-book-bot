import random

NAME = "Vecchia Bunny"

LISTA_FLAVORS = [
    "*sorseggia una tisana alla camomilla* Ecco cosa ho spolverato oggi tra gli scaffali.",
    "Un momento, un momento... *posa la tazza di tisana alla menta* Ecco i tomi che cercavi.",
    "Le mie felci sono cresciute bene questa settimana, e anche la mia collezione. Guarda qui.",
    "*annusa il profumo di tisana all'ortica che aleggia nella stanza* Questi sono i documenti disponibili.",
    "Ho innaffiato le piante e riordinato gli scaffali stamattina: ecco cosa ho trovato per te.",
    "Con calma, con calma... una vecchia tartaruga non corre. Ma i libri sono tutti qui.",
    "*il guscio tintinna contro lo scaffale* Attenta a quella pila, è più vecchia di me. Ecco l'elenco.",
    "Una tisana al tarassaco e un buon libro: non c'è modo migliore di passare il pomeriggio. Eccoli.",
    "I miei gerani sono fioriti proprio accanto a questi volumi: dev'essere di buon auspicio. Guarda qui.",
    "*si sistema gli occhialini sul muso* Vediamo un po'... ah sì, ecco tutto quello che ho.",
]

SEND_FLAVORS = [
    "Eccolo qui, maneggialo con cura come fosse una delle mie piantine.",
    "*porge il tomo con la zampa, ancora tiepido di tisana rovesciata accidentalmente vicino*",
    "Questo è uno dei miei preferiti. Buona lettura, cara/o.",
    "Tienilo pure quanto vuoi, io ne ho una copia anche tra le radici del mio vaso di basilico.",
    "*annuisce lentamente* Una scelta saggia. Eccolo.",
    "Profuma ancora di tisana alla lavanda, l'ho letto proprio ieri sera.",
    "Ecco a te. Riportalo... o no, tanto io non mi muovo da qui comunque.",
]


ARCHIVE_FLAVORS = [
    "*sistema il nuovo tomo sullo scaffale con cura* Grazie, lo archivio subito.",
    "Un altro libro per la collezione! Lo metto vicino al vaso di rosmarino.",
    "*annusa la copertina* Profumo di carta nuova. Archiviato, cara/o.",
    "Che meraviglia, un nuovo arrivo. Preparo una tisana per festeggiare mentre lo ripongo.",
    "Ecco fatto, l'ho aggiunto agli scaffali. La mia collezione cresce come le mie piante.",
]


def _pick(flavors: list[str], memory: dict, key: str) -> str:
    choice = random.choice(flavors)
    last = memory.get(key)
    if len(flavors) > 1:
        while choice == last:
            choice = random.choice(flavors)
    memory[key] = choice
    return choice


def pick_lista_flavor(memory: dict) -> str:
    return _pick(LISTA_FLAVORS, memory, "last_lista_flavor")


def pick_send_flavor(memory: dict) -> str:
    return _pick(SEND_FLAVORS, memory, "last_send_flavor")


def pick_archive_flavor(memory: dict) -> str:
    return _pick(ARCHIVE_FLAVORS, memory, "last_archive_flavor")

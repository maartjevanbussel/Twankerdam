import code

zelfstemmers = ['Ingrid', 'Ruby']  #De mensen die 1e keer niet stemmen
permanentestemmen = []  #De mensen die twee keer niet gestemd hebben
ravenveer = []  #Speler met veer tussen ' ' of laat het leeg als ''
zwartestem = []  #Speler met zwarte stem tussen ' ' of laat het leeg als ''

#Alisassen
aliaslijst = [['Tom s', 'toms', 'tomschouten', 'tom schouten', 'tomss'],
              [
                'Tom l', 'toml', 'tomvl', 'tom vl', 'tom van lamoen',
                'Tomvanlamoen', 'tom lamoen'
              ], ['Loes', 'loes schouten', 'loess', 'loes s'],
              ['Sjors', 'sjorsje', 'sjorsjeee', 'sjorsjeee333'],
              ['Wesley', 'wesleyy', 'wesley'],
              ['Isabelle', 'isabelle v w', 'isabellevw', 'isabelle-v-w'],
              ['Vincent', 'vincentv'],
              ['Eliane', 'Elaine'],
              ['Kim', 'kim verhoeven', 'kimverhoeven'],
              ['Jurriaan', 'jurruaan', 'jurriaan', 'juriaan'],
              ['Niels', 'niels van laarhoven'], ['Maud', 'maud :heart: mes'],
              ['Koffie Kan', 'koffiekan'], ['Do', 'Dootje', 'do'],
              ['Daniël', 'Daniel', 'daniel'], ['Tess', 'Tessa']]

#karakters die achter een stem verwijderd moeten worden.
stopkarakters = [
  '.', ':', ',', '?', ' met', '\n', '!', ' omdat', ' want', ' vanwege',
  ' maar', ' al', ' als', ' vanwege', ' voornamelijk', ' (', '('
]

staafbreedte = 0.9  #Hoe breed de staven zijn
hoog = 10  #hoogte afbeelding
titel = ''  # laat dit als '' tenzij je handmatig de titel with aanpassen
code.doehet(zelfstemmers, permanentestemmen, aliaslijst, stopkarakters,
            staafbreedte, ravenveer, titel, hoog, zwartestem)

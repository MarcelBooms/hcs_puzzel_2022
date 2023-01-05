veldgrootte=30
maxaantalgetallen=15

vulblokje="X"
kruisje="."
leegveld="_"
  
tabel=[[leegveld for n in range(veldgrootte)] for n in range(veldgrootte)]
tabel2_x=[[] for n in range(veldgrootte)]
tabel2_y=[[] for n in range(veldgrootte)]

gx=[[] for n in range(veldgrootte)]
gy=[[] for n in range(veldgrootte)]



def lees_rij():
  # Makkelijke manier om alle rijen uit te lezen
  # In de list gx[kolom] komen alle ingelezen rij-getallen te staan
  f = open('input_kerstpuzzel2022_rij.txt','r')
  regels = f.readlines()
  m=0
  for regel in regels:
    getallen = regel.strip().split('\t')
    totaal = 0
    # Bereken het aantal gevulde vakjes
    for n in range(len(getallen)):
      totaal += int(getallen[n])
    #Bij ieder blok van gevulde vakjes hoort een kruisje
    totaal += len(getallen)-1 if totaal else 0
    # Ruimte is de speelruimte tussen veldgrootte en gevulde vakjes
    # Ruimte wordt later gebruikt om het aantal mogelijke combinaties te berekenen
    ruimte = veldgrootte-totaal
    for n in range(len(getallen)):
      gx[m].append({'ruimte': ruimte ,'getal':int(getallen[n])})
    m+=1

def lees_kolom():
  # Makkelijke manier om alle kolommen uit te lezen. Zie lees_rij() voor commentaar
  # In de list gy[rij] komen alle ingelezen kolom-getallen te staan
  f = open('input_kerstpuzzel2022_kolom.txt','r')
  regels = f.readlines()
  m=0
  for regel in regels:
    getallen = regel.strip().split('\t')
    totaal = 0
    for n in range(len(getallen)):
      totaal += int(getallen[n])
    totaal += len(getallen)-1 if totaal else 0
    ruimte = veldgrootte-totaal
    begin = 0
    for n in range(len(getallen)):
      gy[m].append({'ruimte': ruimte,'getal':int(getallen[n])})
      begin += int(getallen[n]) + 1
    m+=1

def print_tabel():
  # print header met kolomnummers
  tekst=' ' * 5
  for n in range(veldgrootte):
    tekst+=str(int(n/10)).strip()+' '
  print(tekst)
  tekst=' ' * 5
  for n in range(veldgrootte):
    tekst+=str(int(n % 10)).strip()+' '
  print(tekst)
  print()
  # print de tabel
  n=0
  for regel in tabel:
    cijfers=''
    for cijfer in gx[n]:
      if cijfer['getal']:
        cijfers += str(cijfer['getal']) + ' '
      elif not cijfers:
        cijfers='0'    
    print(str(n).zfill(2),' ', ' '.join(regel)," ",cijfers)
    n+=1
  
  # print de cijfers onder de tabel
  print()
  rij1=True
  rij=0
  for kolom in range(maxaantalgetallen-1):
    cijfers=' ' * 5
    for cijfer in gy:
      if rij1 or (len(cijfer)>kolom and cijfer[kolom]['getal']):
        cijfers += (str(cijfer[kolom]['getal']) + ' ')[:2]
      else:
        cijfers += '  '
    print(cijfers)
    rij += 1
    rij1=False

def check_alle_mogelijkheden(m, kolom, speling_totaal, speling_max):
  # Een recursieve functie die alle mogelijke combinaties uitrekent van een setje getallen uitrekent
  # Stel een veld is 5 breed en de getallen zijn 1 1 dan zijn de volgende combinaties mogelijk
  # X.X.. X..X. X...X .X.X. ..X.X (Speling is 2 posities)
  # m is een list van getallen
  # kolom is positie(index) vanaf waar de mogelijkheden berekend worden
  # speling_totaal is de reeds gebruikte speling vanaf kolom 0.
  # speling_max is het aantal posities speling dat voor deze set getallen geldt.
  blok = []
  # print("speling_max (",speling_max,") - speling_totaal(",speling_totaal,") =", speling_max - speling_totaal)
  # Bereken voor ieder blokje alle mogelijkheden. Wanneer het eerste blokje niet alle speling heeft gebruikt dan
  # kan de resterende speling voor het 2e,3e, enz. blokje gebruikt worden. Hier zit het recursieve gedeelte in.
  # De functie geeft een lijst van mogelijkheden terug. 
  for spel in range(speling_max - speling_totaal + 1):
    tekst = kruisje * spel + vulblokje * m[kolom]['getal'] 
    if kolom == len(m)-1:
      tekst += kruisje * (speling_max - speling_totaal - spel )
      antwoord = []
    else:
      antwoord = check_alle_mogelijkheden(m, kolom + 1, speling_totaal + spel, speling_max )
    for antw in antwoord:
      blok.append( tekst + kruisje + antw )
    if kolom == len(m) -1:
      blok.append(tekst)
  # print("Returning ",blok)
  return blok


def bouw_alle_rijen():
  # In lijst tabel2_x komt per rij alle mogelijke combinaties van de rij getallen te staan.
  # In lijst tabel2_y komt per rij alle mogelijke combinaties van de kolom getallen te staan.
  # Het startpunt van check_alle_mogelijkheden is:
  # - de lijst van getallen voor rij n, kolom 0, gebruikte speling 0, maximale speling voor die rij 
  # Het resultaat is een list die naar een dictionary en weer terug naar een list wordt omgezet om 
  # alle duplicates eruit te filteren. (Alles ombouwen naar dictionaries zou de solver nog sneller maken)
  for n in range(veldgrootte):
    tabel2_x[n]=list(dict.fromkeys(check_alle_mogelijkheden(gx[n],0,0,gx[n][0]['ruimte'])))
    tabel2_y[n]=list(dict.fromkeys(check_alle_mogelijkheden(gy[n],0,0,gy[n][0]['ruimte'])))
      

def verwijder_kolommen(rij_nr):
  # Op rij X staat in tabel2_X alle mogelijke combinaties voor die rij
  # Deze functie maakt een filter op basis van die combinaties
  # Alle kolomcobinaties in de tabel2_Y die niet aan het filter voldoen worden verwijderd.

  # Startpunt is de eerste combinatie
  tekst=list(tabel2_x[rij_nr][0])
  # print("Originele tekst: ",''.join(tekst))
  # Controleer nu de overige combinaties. Een leegveld vakje wordt straks als wildcard gebruikt
  for n in range(len(tabel2_x[rij_nr])):
    for m in range(veldgrootte):
      if tekst[m] != leegveld and tekst[m] != tabel2_x[rij_nr][n][m]:
        tekst[m]=leegveld
  # print("Nieuwe tekst   : ",''.join(tekst))
  # Roep de verwijder_kolom functie aan om te gaan filteren
  return verwijder_kolom(tekst, rij_nr)

def verwijder_kolom(filter, rij_nr):
  # Als het filter alleen wildcards bevat is geen vergelijking nodig
  if ''.join(filter) == leegveld*veldgrootte:
    return False
  # Boolean verwijderd wordt voor het iteratieproces gebruikt om te bepalen of er nog wijzigingen hebben plaatsgevonden
  verwijderd=False
  # Controleer character voor character of een item niet aan het filter voldoet.
  # Vanwege de grootte van sommige lists wordt 2e list nieuwe_tabel aangemaakt en de oude verwijderd. Dit is vele malen sneller dan een item uit een lijst verwijderen
  for n in range(veldgrootte):
    # print("Processing rij",rij_nr,"kolom",n)
    c=filter[n]
    nieuwe_tabel=[]
    for optie in range(len(tabel2_y[n])):
      if tabel2_y[n][optie][rij_nr] == c or c == leegveld:
        nieuwe_tabel.append(tabel2_y[n][optie])
      else:
        # print("Optie ",m," wordt verwijderd")
        verwijderd=True
    tabel2_y[n].clear
    if len(nieuwe_tabel) == 0:
      print("Er bestaat geen oplossing. Wat gaat hier fout?")
      print(''.join(filter) + "  <-- Filter")
      for n in tabel2_y[n]:
        print(''.join(n))
      raise Exception('Verwijder_kolommen: Wat gaat hier fout?')
    tabel2_y[n]=nieuwe_tabel
  return verwijderd

def verwijder_rijen(kolom_nr):
  # Zie verwijder_kolommen voor commentaar
  tekst=list(tabel2_y[kolom_nr][0])
  for n in range(len(tabel2_y[kolom_nr])):
    for m in range(veldgrootte):
      if tekst[m] != leegveld and tekst[m] != tabel2_y[kolom_nr][n][m]:
        tekst[m]=leegveld
  return verwijder_rij(tekst, kolom_nr)

def verwijder_rij(filter, kolom_nr):
  # Zie verwijder_kolom voor commentaar
  if ''.join(filter) == leegveld*veldgrootte:
    return False
  verwijderd=False
  for n in range(veldgrootte):
    c=filter[n]
    nieuwe_tabel=[]
    for m in range(len(tabel2_x[n])):
      if c == leegveld or tabel2_x[n][m][kolom_nr] == c or c == leegveld:
        nieuwe_tabel.append(tabel2_x[n][m])
      else:
        # print("Optie ",m," wordt verwijderd")
        verwijderd=True
    tabel2_x[n].clear    
    if len(nieuwe_tabel) == 0:
      print("Er bestaat geen oplossing. Wat gaat hier fout?")
      print(''.join(filter) + "  <-- Filter")
      for n in tabel2_x[n]:
        print(''.join(n))
      raise Exception('Wat gaat hier fout?')
    tabel2_x[n]=nieuwe_tabel
  return verwijderd

def controleren():
  # Deze functie ruimt net zo lang alle rijen/kolommen op totdat
  # de oplossing gevonden is, er geen oplossing mogelijk is of
  # het aantal iteraties > 100 (debug/runaway functie)
  verwijderd=True
  run=0
  while verwijderd:
    verwijderd=False
    run+=1
    if run>100:
      break
    print("\nRun ",run)
    for n in range(veldgrootte):
      print("Rij " , n , " heeft ",len(tabel2_x[n]),"mogelijkheden")
      verwijderd = verwijder_kolommen(n)
  
    for n in range(veldgrootte):
      print("Kolom " , n , " heeft ",len(tabel2_y[n]),"mogelijkheden")    
      if verwijder_rijen(n):
        verwijderd = True

def vul_tabel():
  # Vul de tabel om te kunnen printen
  for rij_nr in range(veldgrootte):
    tekst=list(tabel2_x[rij_nr][0])
    for n in range(len(tabel2_x[rij_nr])):
      for m in range(veldgrootte):
        if tekst[m] != leegveld and tekst[m] != tabel2_x[rij_nr][n][m]:
          tekst[m]=leegveld
    for kolom_nr in range(veldgrootte):
      tabel[rij_nr][kolom_nr]=tekst[kolom_nr]    
        
def main():
  lees_rij()
  lees_kolom()
  bouw_alle_rijen()
  controleren()
  vul_tabel()
  print_tabel()
    
if __name__ == "__main__":
  main()

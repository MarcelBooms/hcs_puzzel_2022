veldgrootte=30
maxaantalgetallen=15

vulblokje='Y'
kruisje="."
leegveld="_"
  
tabel=[[leegveld for n in range(veldgrootte)] for n in range(veldgrootte)]
gx=[[] for n in range(veldgrootte)]
gy=[[] for n in range(veldgrootte)]



def lees_rij():
  # Makkelijke manier om alle rijen uit te lezen
  global gx
  global veldgrootte
  f = open('input_kerstpuzzel2022_rij.txt','r')
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
      gx[m].append({'begin':begin,'eind':begin + int(getallen[n]) + ruimte -1,'getal':int(getallen[n])})
      # print({'begin':begin,'eind':begin + int(getallen[n]) + ruimte - 1,'getal':int(getallen[n])})
      begin += int(getallen[n]) + 1
    m+=1

def lees_kolom():
  # Makkelijke manier om alle kolommen uit te lezen
  global gy
  global veldgrootte
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
      gy[m].append({'begin':begin,'eind':begin + int(getallen[n]) + ruimte - 1,'getal':int(getallen[n])})
      begin += int(getallen[n]) + 1
    m+=1

def print_tabel():
  # print de tabel
  n=0
  for regel in tabel:
    cijfers=''
    for cijfer in gx[n]:
      if cijfer['getal']:
        cijfers += str(cijfer['getal']) + ' '
      elif not cijfers:
        cijfers='0'    
    print(' '.join(regel)," ",cijfers)
    n+=1
    
  print()
  rij1=True
  rij=0
  for kolom in range(maxaantalgetallen-1):
    cijfers=''
    for cijfer in gy:
      if rij1 or (len(cijfer)>kolom and cijfer[kolom]['getal']):
        cijfers += (str(cijfer[kolom]['getal']) + ' ')[:2]
      else:
        cijfers += '  '
    print(cijfers)
    rij += 1
    rij1=False

def print_tabel2():
  # print de tabel
  n=0
  for regel in tabel:
    cijfers=''
    for cijfer in gx[n]:
      if cijfer['getal']:
        cijfers += str(cijfer['getal']) + ' '
      elif not cijfers:
        cijfers='0'    
    print(' '.join(regel)," ",cijfers)
    print(gx[n])
    n+=1

def check_volledige_rij_kolom():
  # Check elke rij & kolom waarvan de vrijheid van de te plaatsen
  # blokjes/kruisjes 0 is. 
  global tabel,gx,gy
  aangepast=False
  print("== check_volledige_rij_kolom ==")
  print_tabel()
  for y in range(veldgrootte):
    kruizen=0
    for x in range(veldgrootte):
      kruizen+=1 if tabel[y][x]==kruisje else 0
    totaal=0
    for n in gx[y]:
      totaal+=n['getal']
    totaal+=len(gx[y])-1 # Voeg verplichte lege vakjes toe.
    if kruizen + totaal == veldgrootte or totaal == 0:
      # print("Rij " + str(y) + " kan volledig gevuld worden")
      if vul_rij_kolom('r',y):
        aangepast=True
    # else:
      # print("Rij " + str(y) + " heeft " + str(kruizen) + " kruizen en " + str(totaal) + " blokjes. veldgrootte = " + str(veldgrootte))
      
  for x in range(veldgrootte):
    kruizen=0
    for y in range(veldgrootte):
      kruizen+=1 if tabel[y][x]==kruisje else 0
    totaal=0
    for n in gy[x]:
      totaal+=n['getal']
    totaal+=len(gy[x])-1   # Voeg verplichte lege vakjes toe.
    if kruizen + totaal == veldgrootte or totaal == 0:
      print("Kolom " + str(x) + " kan volledig gevuld worden")
      if vul_rij_kolom('k',x):
        aangepast = True
    # else:
      # print("Kolom " + str(x) + " heeft " + str(kruizen) + " kruizen en " + str(totaal) + " blokjes. veldgrootte = " + str(veldgrootte))
  print_tabel()
  return aangepast

def vul_rij_kolom(richting,pos):
  # Vul de rij/kolom in tabel waarvan de vrijheid te plaatsen blokjes 0 is.
  aangepast=False
  o=0
  totaal=0
  print(gx[pos])
  print_tabel()
  if richting == 'r':
    for n in gx[pos]:
      totaal+=n['getal']
    for n in range(veldgrootte):
      if tabel[pos][n] == leegveld:
        if o<len(gx[pos]):
          for m in range(gx[pos][o]['getal']-1):
            print(tabel[pos])
            print(gx[pos])
            print(pos,n,m,n+m)
            tabel[pos][n+m]=vulblokje
            aangepast=True
          n += gx[pos][o]['getal']
          o += 1
        if n < veldgrootte and tabel[pos][n]==leegveld:
          tabel[pos][n]=kruisje
          aangepast=True
  else:
    for n in gy[pos]:
      totaal+=n['getal']
    for n in range(veldgrootte):
      if tabel[n][pos] == leegveld:
        if o < len(gy[pos]):
          for m in range(gy[pos][o]['getal']-1):
            tabel[n+m][pos]=vulblokje
            aangepast=True
          n += gy[pos][o]['getal']
          o += 1
        if n < veldgrootte and tabel[n][pos]==leegveld:
          tabel[n][pos]=kruisje
          aangepast=True
  return aangepast

def vul_blokjes_in():
  # Check iedere rij/kolom op velden die zowieso een blokje zijn.
  # Een rij blokjes van 7 en een vrijheid van 1 heeft zowieso 5 blokjes
  print("== vul blokjes ==")
  print_tabel()
  aangepast=False
  for n in range(veldgrootte):
    for m in gx[n]:
      speling=m['eind']-m['begin']-m['getal'] +1
      # print("begin",m['begin'],"eind",m['eind'],"getal",m['getal'],"speling",speling,"b+s",m['begin'] + speling)
      # print(n,"begin + speling < eind ", m['begin'] + speling,m['eind'],m)
      if m['getal'] > 0 and m['begin'] + m['getal'] >= m['eind'] - m['getal'] + 1:
        print(n,m)
        for o in range(m['begin'] +speling, m['eind']-m['getal'],-1):          
          # print("begin",m['begin'],"eind",m['eind'],"getal",m['getal'],"speling",speling)
          if tabel[n][o] == leegveld:            
            tabel[n][o]=vulblokje
            aangepast=True
    for m in gy[n]:
      speling=m['eind']-m['begin']-m['getal'] +1
      if m['getal'] > 0 and m['begin'] + m['getal'] >= m['eind'] - m['getal'] + 1:
        for o in range(m['begin'] +speling, m['eind']-m['getal'],-1):
          # print("begin",m['begin'],"eind",m['eind'],"getal",m['getal'],"speling",speling)
          if tabel[n][o] == leegveld:
            tabel[o][n]=vulblokje
            aangepast=True
  print_tabel()
  return aangepast

def aanvullen():
  print("== aanvullen ==")
  aangepast=False
  for n in range(veldgrootte):
    # print("aanvullen1",n)
    # print_tabel()
    for m in gx[n]:
      #Als het eerste veld bekend gevuld is dan kan de rest aangevuld worden
      print("horizontaal begin->eind ",n,m,' '.join(tabel[n]))
      if tabel[n][m['begin']] == kruisje and m['begin'] < m['eind']:
         m['begin'] += 1
      if tabel[n][m['eind']] == kruisje and m['eind'] > m['begin']:
         m['eind'] -= 1
      if tabel[n][m['begin']] == vulblokje and (m['begin'] == 0  or tabel[n][m['begin']-1] == kruisje):
        for o in range(m['begin'], m['begin'] + m['getal']-1):
          # print(n,o,tabel[n][o])
          if tabel[n][o]==leegveld:
            tabel[n][o]=vulblokje
            aangepast=True
        m['eind']=m['begin'] + m['getal'] - 1
        if m['begin'] + m['getal'] < veldgrootte:
          tabel[n][m['begin'] + m['getal']]=kruisje
      #Als het laatste veld bekend is en geen onderdeel is van het volgende getal
      # print("horizontaal eind->begin ",n,m,' '.join(tabel[n]))
      if tabel[n][m['eind']] == vulblokje and (m['eind'] == veldgrootte-1 or tabel[n][m['eind'] +1] == kruisje):
        # print("o gaat van ",m['eind'] - m['getal']+1,"naar",m['eind'])
        for o in range(m['eind'] - m['getal']+1, m['eind']):
          # print(n,o,tabel[n][o])
          if tabel[n][o]==leegveld:
            tabel[n][o]=vulblokje
            aangepast=True
          m['begin']=m['eind'] - m['getal'] + 1
        if m['eind'] - m['getal'] > 0:
          tabel[n][m['eind'] - m['getal']]=kruisje
    # print("aanvullen2",n)
    # print_tabel()
    for m in gy[n]:
      #Als het eerste veld bekend gevuld is dan kan de rest aangevuld worden
      if n == 3:
        print(n,m,"VERTIKAAL")
        print_tabel()       
      if tabel[m['begin']][n] == kruisje and m['begin'] < m['eind']:
         m['begin'] += 1
      if tabel[m['eind']][n] == kruisje and m['eind'] > m['begin']:
         m['eind'] -= 1
      if tabel[m['begin']][n] == vulblokje and (m['begin'] == 0  or tabel[m['begin']-1][n] == kruisje):
        for o in range(m['begin'], m['begin'] + m['getal']-1):
          if n == 3:
            print(n,o,tabel[n][o])
          if tabel[o][n]==leegveld:
            tabel[o][n]=vulblokje
            aangepast=True
          m['eind']=m['begin'] + m['getal'] 
        if m['begin'] + m['getal'] < veldgrootte:
          tabel[m['begin'] + m['getal']][n]=kruisje
      if n == 3:
        print('na eerste stap',gy[n])
        print_tabel()
      #Als het laatste veld bekend is en geen onderdeel is van het volgende getal
      if tabel[n][m['eind']] == vulblokje and (m['eind'] == veldgrootte-1 or (tabel[n][m['eind'] +1] == kruisje and sss):
        for o in range(m['eind'] - m['getal'] + 1, m['eind']):
          print(n,o,tabel[n][o])
          if tabel[o][n]==leegveld:
            tabel[o][n]=vulblokje
            aangepast=True
          # print("!!! m['begin']=m['eind'] - m['getal']+1 =>",m['eind'] , m['getal'],1, m['eind'] - m['getal']+1 )
          m['begin']=m['eind'] - m['getal'] + 1
        if m['eind'] - m['getal'] > 0:
          tabel[m['eind'] - m['getal']][n]=kruisje
      print("einde aanvullen2",n)
      print_tabel()
  # print_tabel()
  return aangepast

# def controle_vrijheden():
#   for n in range(veldgrootte):
#     for m in gx[n]:
      

        
def los_puzzel_op():
  aangepast=check_volledige_rij_kolom()
  while aangepast:
    aangepast = check_volledige_rij_kolom()
    print('Nog een keer')
    vul_blokjes_in()
    aanvullen()
  aangepast = check_volledige_rij_kolom()
  print('Nog een keer')
  vul_blokjes_in()
  aanvullen()

def main():
  lees_rij()
  lees_kolom()
  los_puzzel_op()
  print_tabel()
  print_tabel2()
  
  
if __name__ == "__main__":
  main()

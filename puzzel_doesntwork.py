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
      if tabel[y][x]==kruisje:
        kruizen+=1
        print("Kruizen = ",kruizen,"y=",y,"x=",x)
    totaal=0
    for n in gx[y]:
      totaal+=n['getal']
    totaal+=len(gx[y])-1 # Voeg verplichte lege vakjes toe.
    if kruizen + totaal == veldgrootte or totaal == 0:
      print("Rij " + str(y) + " heeft " + str(kruizen) + " kruizen en " + str(totaal) + " blokjes. veldgrootte = " + str(veldgrootte))
      print(tabel[y])
      print("Rij " + str(y) + " kan volledig gevuld worden")
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
  print('== vul_rij_kolom(',richting,pos,')==')
  # print(gx[pos])
  # print_tabel()
  if richting == 'r':
    for n in gx[pos]:
      totaal+=n['getal']
    n = 0
    while n < veldgrootte:
      # print("Checking rij",pos," kolom",n)
      if totaal == 0:
        # print("totaal is 0")
        tabel[pos][n]=kruisje
      else:
        # print("if geen er kruisje staat..")
        if o<len(gx[pos]) and tabel[pos][n] != kruisje:
          # print("Geen kruisje op kolom ",n)
          for m in range(gx[pos][o]['getal']):
            # print("kolom ",n+m,"wordt gevuld")  
            tabel[pos][n+m]=vulblokje
            aangepast=True
          gx[pos][o]['begin'] = n
          n += gx[pos][o]['getal']
          # print("kolom eind is ",n )
          gx[pos][o]['eind'] = n
          o += 1
          if n < veldgrootte-1:
            # print("Kruisje op n ",n,"geplaatst")
            tabel[pos][n]=kruisje
        else:
          # print("geen levens meer dus kruisje")
          tabel[pos][n]=kruisje
      n += 1
  else:
    for n in gy[pos]:
      totaal+=n['getal']
    n = 0
    while n < veldgrootte:
      # print("Checking kolom",n)
      if totaal == 0:
        tabel[n][pos]=kruisje
      else:
        # print("if geen er kruisje staat..")
        if o<len(gy[pos]) and tabel[n][pos] != kruisje:
          # print("Geen kruisje op rij ",n)
          for m in range(gy[pos][o]['getal']):
            # print("rij ",n+m,"wordt gevuld")  
            tabel[n+m][pos]=vulblokje
            aangepast=True
          gy[pos][o]['begin'] = n
          n += gy[pos][o]['getal']
          # print("rij eind is ",n )
          gy[pos][o]['eind'] = n
          o += 1
          if n < veldgrootte-1:
            # print("Kruisje op n ",n,"geplaatst")
            tabel[n][pos]=kruisje
        else:
          # print("geen levens meer dus kruisje")
          tabel[n][pos]=kruisje
      n += 1
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
      # if n == 20:
      #   print("begin",m['begin'],"eind",m['eind'],"getal",m['getal'],"speling",speling,"b+s",m['begin'] + speling)
      #   print(n,"begin + speling < eind ", m['begin'] + speling,m['eind'],m)
      if m['getal'] > 0 and m['begin'] + m['getal'] >= m['eind'] - m['getal'] + 1:
        # print(n,m)
        for o in range(m['begin'] +speling, m['begin'] + m['getal'] - 1):          
          # if n == 20:
            # print("begin",m['begin'],"eind",m['eind'],"getal",m['getal'],"speling",speling)
          if tabel[n][o] == leegveld:            
            tabel[n][o]=vulblokje
            aangepast=True
    for m in gy[n]:
      speling=m['eind']-m['begin']-m['getal'] +1
      if m['getal'] > 0 and m['begin'] + m['getal'] >= m['eind'] - m['getal'] + 1:
        for o in range(m['begin'] +speling, m['begin'] + m['getal'] - 1):
          # print("begin",m['begin'],"eind",m['eind'],"getal",m['getal'],"speling",speling)
          if tabel[n][o] == leegveld:
            tabel[o][n]=vulblokje
            aangepast=True
  print_tabel()
  return aangepast

# Het eerste cijfer (of vorig cijfer heeft eind kleiner dan begin) heeft een blokje op de eerste positie
# - invullen
# - kruisje plaatsen
# - begin, eind invullen
# - indien volgend getal een begin < eind+1 heeft dan aanpassen
# Het laatste (of volgend cijfer heeft een begin groter dan eind) cijfer heeft een blokje op de laatste positie
# - invullen
# - kruisje plaatsen
# - begin, eind invullen
# - indien vorig getal een eind > begin-1 heeft dan aanpassen

def aanvullen():
  print("== aanvullen ==")
  aangepast=False
  for n in range(veldgrootte):
    # print("aanvullen1",n)
    # print_tabel()
    for b in range(len(gx[n])):
      m=gx[n][b]
      if b>0:
        mp=gx[n][b-1]
      else:
        mp={'begin':-1,'eind':-1,'getal':0}
      if b<len(gx[n])-1:
        mn=gx[n][b+1]
      else:
        mn={'begin':veldgrootte,'eind':veldgrootte,'getal':0}
      #Als het eerste veld bekend gevuld is dan kan de rest aangevuld worden
      # print("horizontaal begin->eind ",n,m,' '.join(tabel[n]))
      if tabel[n][m['begin']] == kruisje and m['begin'] < m['eind']:
         m['begin'] += 1
      if tabel[n][m['eind']] == kruisje and m['eind'] > m['begin']:
         m['eind'] -= 1
      if tabel[n][m['begin']] == vulblokje and (m['begin'] == 0  or (tabel[n][m['begin']-1] == kruisje and mp['eind']<=m['begin'])):
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
      if tabel[n][m['eind']] == vulblokje and (m['eind'] == veldgrootte-1 or (tabel[n][m['eind'] +1] == kruisje and m['eind']<=mn['begin'])):
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
    for b in range(len(gy[n])):
      m=gy[n][b]
      if b>0:
        mp=gy[n][b-1]
      else:
        mp=gy[n][b]
      if b<len(gy[n])-1:
        mn=gy[n][b+1]
      else:
        mn=gy[n][b]
      #Als het eerste veld bekend gevuld is dan kan de rest aangevuld worden
      # if n == 3:
        # print(n,m,"VERTIKAAL")
        # print_tabel()       
      if tabel[m['begin']][n] == kruisje and m['begin'] < m['eind']:
         m['begin'] += 1
      if tabel[m['eind']][n] == kruisje and m['eind'] > m['begin']:
         m['eind'] -= 1
      if tabel[m['begin']][n] == vulblokje and (m['begin'] == 0  or (tabel[n][m['begin']-1] == kruisje and mp['eind']<=m['begin'])):
        for o in range(m['begin'], m['begin'] + m['getal']-1):
          # if n == 3:
            # print(n,o,tabel[n][o])
          if tabel[o][n]==leegveld:
            tabel[o][n]=vulblokje
            aangepast=True
          m['eind']=m['begin'] + m['getal'] 
        if m['begin'] + m['getal'] < veldgrootte:
          tabel[m['begin'] + m['getal']][n]=kruisje
      # if n == 3:
        # print('na eerste stap',gy[n])
        # print_tabel()
      #Als het laatste veld bekend is en geen onderdeel is van het volgende getal
      if tabel[n][m['eind']] == vulblokje and (m['eind'] == veldgrootte-1 or (tabel[n][m['eind'] +1] == kruisje and m['eind']<=mn['begin'])):
        for o in range(m['eind'] - m['getal'] + 1, m['eind']):
          print(n,o,tabel[n][o])
          if tabel[o][n]==leegveld:
            tabel[o][n]=vulblokje
            aangepast=True
          # print("!!! m['begin']=m['eind'] - m['getal']+1 =>",m['eind'] , m['getal'],1, m['eind'] - m['getal']+1 )
          m['begin']=m['eind'] - m['getal'] + 1
        if m['eind'] - m['getal'] > 0:
          tabel[m['eind'] - m['getal']][n]=kruisje
      # print("einde aanvullen2",n)
      # print_tabel()
  # print_tabel()
  return aangepast

def controle_vrijheden():
  for n in range(veldgrootte):
    teller=0
    for m in gx[n]:
      speling=m['eind']-m['begin']-m['getal'] +1
      if m['getal']:
        p=speling/m['getal']
      if [m['begin'] != m['eind']]:
        print(m,tabel[n][m['begin']:m['eind']+1])
      else:
        print(m,tabel[n][m['begin']])
    print()
    for m in gy[n]:
      speling=m['eind']-m['begin']-m['getal'] +1
      if m['getal']:
        p=speling/m['getal']
      if [m['begin'] != m['eind']]:
        print(m,tabel[n][m['begin']:m['eind']+1])
      else:
        print(m,tabel[n][m['begin']])
    print()

        
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

def vooraf():
  tabel[0]  = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '.', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', '.']
  tabel[1]  = ['Y', '.', '.', '.', '.', '.', 'Y', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '.', 'Y', '_', '_', '_', '_', '_', 'Y', '.']
  tabel[2]  = ['Y', '_', 'Y', 'Y', 'Y', '_', 'Y', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '.', 'Y', '_', 'Y', 'Y', 'Y', '_', 'Y', '.']
  tabel[3]  = ['Y', '.', 'Y', 'Y', 'Y', '.', 'Y', '.', 'Y', 'Y', '.', 'Y', 'Y', 'Y', 'Y', '.', 'Y', 'Y', '.', 'Y', '.', '.', 'Y', '_', 'Y', 'Y', 'Y', '_', 'Y', '.']
  tabel[4]  = ['Y', '.', 'Y', 'Y', 'Y', '_', 'Y', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '.', 'Y', '_', 'Y', 'Y', 'Y', '_', 'Y', '.']
  tabel[5]  = ['Y', '.', '.', '.', '.', '.', 'Y', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '.', 'Y', '_', '_', '_', '_', '_', 'Y', '.']
  tabel[6]  = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', '.', 'Y', '.', 'Y', '.', 'Y', '.', 'Y', '.', 'Y', '.', 'Y', '.', 'Y', '.', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', '.']
  tabel[7]  = ['.', '.', '.', '.', '.', '.', '.', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '.', '.', '.', '.', '.', '.', '.', '.']

  tabel[21] = ['.', '.', '.', '.', '.', '.', '.', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '.']
  tabel[22] = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '.']
  tabel[23] = ['Y', '.', '_', '_', '_', '_', 'Y', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '.']
  tabel[24] = ['Y', '.', 'Y', 'Y', 'Y', '_', 'Y', '_', 'Y', '_', '_', '_', 'Y', 'Y', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '.']
  tabel[25] = ['Y', '.', 'Y', 'Y', 'Y', '_', 'Y', '_', 'Y', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '.']
  tabel[26] = ['Y', '_', 'Y', 'Y', 'Y', '_', 'Y', '_', '_', '_', '_', '_', '_', '_', '_', 'Y', '_', '_', '_', '_', '_', '_', '_', 'Y', 'Y', '_', '_', '_', '_', '.']
  tabel[27] = ['Y', '_', '_', '_', '_', '_', 'Y', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '.']
  tabel[28] = ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '.']
  tabel[29] = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']


def main():
  lees_rij()
  lees_kolom()
  vooraf()
  los_puzzel_op()
  print_tabel()
  # print_tabel2()
  controle_vrijheden()
  print(tabel[0])
  print(tabel[1])
  print(tabel[2])
  print(tabel[3])
  print(tabel[4])
  print(tabel[5])
  print(tabel[6])
  print()
  print(tabel[22])
  print(tabel[23])
  print(tabel[24])
  print(tabel[25])
  print(tabel[26])
  print(tabel[27])
  print(tabel[28])
  print(tabel[29])
  
  
if __name__ == "__main__":
  main()

'''
Ryan Muncy 04/07/2023

Last Edited 04/07/2023

StagedWombo
The purpose of this is to expand upon the capabilities of WomboCombo3 so that it can calculate fuel needed for each engine for a given payloadf weight and deltaV, and then take that weight and continue onto the next stage anbd do those calculations again.
'''

from math import *
from decimal import *
from pickle import FALSE

getcontext().prec = 6

def deltaV_Calculator(MI, MF, Isp):
    deltaV = Isp * Decimal(log(MI/MF))
    return(deltaV)



def convert_Ton_To_KG(MT):
    #quick function to convert Tons into Pounds
    MassKG = MT * Decimal(1000.0) 
    return(MassKG)
 
def convert_KG_To_Ton(WK):
    MassTons = WK * Decimal(0.0010)
    return(MassTons)

def twrCalculator(T, W):
    twr = Decimal(T/(W * Decimal(9.81)))
    return(twr)

def boolCheck(string):
    checkList = ['true', 't', 'y', 'yes', 'yeah', 'yea', 'yup', 'certainly', 'uh-huh', 'affirmative', 'confirm']
    if string in checkList:
        return(True)
    else:
        return(False)
'''
engineLibrary = {'LV-909': {'Mass': Decimal(0.5), 'Thrust': Decimal(14.783), 'Isp': Decimal(834.70)},
                          'LV-30': {'Mass': Decimal(1.25), 'Thrust':Decimal(205.161) , 'Isp': Decimal(2602.30)},
                           'LV-45': {'Mass': Decimal(1.5), 'Thrust': Decimal(167.969), 'Isp': Decimal(2455.0)}}
'''
engineLibrary = {'LV-909': {'Mass': Decimal(0.5), 'Thrust': Decimal(14.7), 'Isp': Decimal(835.0), 'VacThrust': Decimal(60.0), 'VacIsp': Decimal(3384.45)},
                 'LV-30': {'Mass': Decimal(1.25), 'Thrust':Decimal(205) , 'Isp': Decimal(2602.0), 'VacThrust': Decimal(240.0), 'VacIsp': Decimal(3041.1)},
                 'LV-45': {'Mass': Decimal(1.5), 'Thrust': Decimal(168), 'Isp': Decimal(2455.0), 'VacThrust': Decimal(215.0), 'VacIsp': Decimal(3139.2)}}
#
#variable creation
payloadMassKG = 0
payloadMassTons = 0
payloadMass = 0
fuelCanMassKG = 0
fuelCanMassTons = 0
fuelCanMass = 0
engineMass = 0
nonFuelMass = 0
fuelTotalMassKG = 0
fuelTotalMassTons = 0
fuelTotalMass = 0
finalMass = 0
eningeMassKG = 0
engineMassTons = 0
engineMass = 0
initialMass = 0
engineIsp = 0
engineModel = ' '
desiredDeltaV = 0
twrMin = 1.3
twr = 1.3
thrust = 'Thrust'
Isp = 'Isp'

#getting input
numStages = int(input("How many stages would you like? "))
payloadMassTons = Decimal(input("Please enter your payload Mass in Tons: "))
engineModel = 'LV-909'
#fuelcans are dictionaries so i can keep track of multiple pieces of info at once
'''
FuelCan1 = {'TotalMass': Decimal(0.5625), 'NonFuelMass': Decimal(0.0625), 'Count': 0}
FuelCan2 = {'TotalMass': Decimal(1.125), 'NonFuelMass': Decimal(0.125), 'Count': 0}
FuelCan3 = {'TotalMass': Decimal(2.25), 'NonFuelMass': Decimal(0.25), 'Count': 0}
fuelCans = [FuelCan1]
'''

FuelCan1 = {'TotalMass': Decimal(0.6), 'NonFuelMass': Decimal(0.06), 'Count': 0, 'RadialSize': 1}
FuelCan2 = {'TotalMass': Decimal(1.13), 'NonFuelMass': Decimal(0.13), 'Count': 0, 'RadialSize': 1}
FuelCan3 = {'TotalMass': Decimal(2.25), 'NonFuelMass': Decimal(0.25), 'Count': 0, 'RadialSize': 1}
largeFuelCan1 = {'TotalMass': Decimal(1.2375), 'NonFuelMass': Decimal(0.1), 'Count': 0, 'RadialSize': 2}
largeFuelCan2 = {'TotalMass': Decimal(2.475), 'NonFuelMass': Decimal(0.3), 'Count': 0, 'RadialSize': 2}
largeFuelCan3 = {'TotalMass': Decimal(5.06), 'NonFuelMass': Decimal(0.56), 'Count': 0, 'RadialSize': 2}
adapterSmallLarge = {'TotalMass': Decimal(4.57), 'NonFuelMass': Decimal(0.57), 'Count': 0, 'RadialSize': 1}
fuelCans = [FuelCan1]

def reset_Var():
    global fuelCans
    global fuelCanMassKG
    global fuelCanMassTons
    global fuelCanMass
    global engineMass
    global nonFuelMass
    global fuelTotalMassKG
    global fuelTotalMassTons
    global fuelTotalMass
    global finalMass
    global eningeMassKG
    global engineMassTons
    global engineMass
    global initialMass
    global engineIsp
    global dV
    dV = 0
    initialMass = 0
    engineIsp = 0
    engineMassTons = 0
    engineMassKG = 0
    finalMass = 0
    fuelTotalMass = 0
    fuelTotalMassTons = 0
    fuelTotalMassKG = 0
    nonFuelMass = 0
    engineMass = 0
    fuelCanMass = 0
    fuelCanMassTons = 0
    fuelCanMassKG = 0
    for i in fuelCans:
        i['Count'] = 0
    fuelCans = []

    
def sumOfDictionaries(dictionaries, key1, key2):
    totalSum = 0
    uniqueFuelCans = set()
    for dictionary in dictionaries:
        dictTuple = tuple(dictionary.items())
        if dictTuple not in uniqueFuelCans:
            ##print(dictionary[key1], dictionary[key2])
            totalSum += dictionary[key1] * dictionary[key2]
            uniqueFuelCans.add(dictTuple)
    return(totalSum)


def part_Counter():
    #this iterates through fuelCans to count how many there are so i can keep track of it later
    global fuelCanMassTons
    global fuelTotalMassTons
    global fuelCans
    
    fuelCanMassTons = sumOfDictionaries(fuelCans, 'Count', 'NonFuelMass')
    fuelTotalMassTons = sumOfDictionaries(fuelCans, 'Count', 'TotalMass')

    
part_Counter()
#print(FuelCan1)
##print(fuelCans)
##print(fuelCanMassTons)
##print(fuelTotalMassTons)

#setting variables and conversions
def variableCalculatorWorking():
    global fuelCanMassKG
    global fuelTotalMassKG
    global payloadMassKG
    global engineIsp
    global engineMassTons
    global engineMassKG
    fuelCanMassKG = convert_Ton_To_KG(fuelCanMassTons)
    ##print(fuelCanMassKG)
    fuelTotalMassKG = convert_Ton_To_KG(fuelTotalMassTons)
    ##print(fuelTotalMassKG)
    payloadMassKG = convert_Ton_To_KG(payloadMassTons)
    ##print(payloadMassKG)
    engineIsp = engineLibrary[engineModel][Isp]
    ##print(engineIsp)
    engineMassTons = engineLibrary[engineModel]['Mass']
    ##print(engineMassTons)
    engineMassKG = convert_Ton_To_KG(engineMassTons)
    ##print(engineMassKG)

variableCalculatorWorking()

#setting usable variables put in a funtion so they can be recalculated easily
def variableCalculatorUsable():
    global engineMass
    global payloadMass
    global fuelCanMass
    global nonFuelMass
    global finalMass
    global fuelTotalMass
    global initialMass
    global dV
    ##print(' ')
    engineMass = engineMassKG
    ##print(engineMass)
    payloadMass = payloadMassKG
    ##print(payloadMass)
    fuelCanMass = fuelCanMassKG
    ##print(fuelCanMass)
    nonFuelMass =  payloadMass + fuelCanMass + engineMass
    ##print(nonFuelMass)
    finalMass = nonFuelMass
    ##print(finalMass)
    fuelTotalMass = fuelTotalMassKG
    ##print(fuelTotalMass)
    initialMass = finalMass + fuelTotalMass - fuelCanMass
    ##print(initialMass)
    
    dV = Decimal(deltaV_Calculator(initialMass,  finalMass, engineIsp))

variableCalculatorUsable()
for i in  range(numStages):
    desiredDeltaV = int(input("Please enter your desired deltaV for this stage: "))
    vacOrNah = input("Is this stage going to be operating in a vacuum? ")
    if boolCheck(vacOrNah):
        thrust = 'VacThrust'
        Isp = 'VacIsp'
        twrMin = 0
    else:
        thrust = 'Thrust'
        Isp = 'Isp'
        twrMin = 1.3
    for x in engineLibrary.keys():
        ##print(payloadMass)
        reset_Var()
        ##print(dV)
        engineModel = x
        print(engineModel)
        twr = 1.3
        while dV < desiredDeltaV and twr >= twrMin:
            part_Counter()
            ##print('partcounter ran')
            ##print(fuelCans)
            variableCalculatorWorking()
            variableCalculatorUsable()
            ##print(' ')
            ##print(fuelCans)
            ##print(dV)
            ##print('small')
            if FuelCan1['Count'] >= 1 and FuelCan2['Count']< 3:
                fuelCans.pop()
                fuelCans.append(FuelCan2)
                FuelCan1['Count'] = 0
                FuelCan2['Count'] += 1
                ##print(fuelCans)
                ##print("tank2 added")

            elif FuelCan2['Count'] >= 1 and FuelCan3['Count']< 3:
                fuelCans.pop()
                fuelCans.append(FuelCan3)
                FuelCan2['Count'] = 0
                FuelCan3['Count'] += 1
                ##print(fuelCans)
                ##print("tank3 added")
            elif FuelCan1['Count']< 3:
                fuelCans.append(FuelCan1)
                FuelCan1['Count'] += 1
                ##print(fuelCans)
                ##print("tank1 added")
            elif  FuelCan1['Count']> 1  or FuelCan2['Count']>1 or FuelCan3['Count']>=3:
                break
            

            part_Counter()
            variableCalculatorWorking()
            variableCalculatorUsable()
            twr = twrCalculator(engineLibrary[engineModel][thrust], convert_KG_To_Ton(initialMass))
            ##print('TWR is:', twr)
            print(dV)
        if dV < desiredDeltaV:
            ##print('big start')
            reset_Var()
            twr = 1.3
            fuelCans = []
            ##fuelCans.append(adapterSmallLarge)
            ##adapterSmallLarge['Count'] +=1
            ##print('\nbig has started')
            while dV < desiredDeltaV and twr >= twrMin:
                ##print(fuelCans)
                part_Counter()
                variableCalculatorWorking()
                variableCalculatorUsable()
                if largeFuelCan1['Count'] >= 1 and largeFuelCan2['Count']< 1:
                    fuelCans.pop()
                    fuelCans.append(largeFuelCan2)
                    largeFuelCan1['Count'] = 0
                    largeFuelCan2['Count'] += 1
                    ##print(fuelCans)
                    ##print("tank2 added")

                elif largeFuelCan2['Count'] >= 1 and largeFuelCan3['Count']< 3:
                    fuelCans.pop()
                    fuelCans.append(largeFuelCan3)
                    largeFuelCan2['Count'] = 0
                    largeFuelCan3['Count'] += 1
                    ##print(fuelCans)
                    ##print("tank3 added")
                elif largeFuelCan1['Count'] < 1:
                    fuelCans.append(largeFuelCan1)
                    largeFuelCan1['Count'] += 1
                    ##print(fuelCans)
                    ##print("tank1 added")
                elif  largeFuelCan1['Count']> 1  or largeFuelCan2['Count']>1 or largeFuelCan3['Count']>=3:
                    break
                
                ##print(dV)
                
                part_Counter()
                variableCalculatorWorking()
                variableCalculatorUsable()
                twr = twrCalculator(engineLibrary[engineModel][thrust], convert_KG_To_Ton(initialMass))
                ##print('TWR is', twr)
                ##print(dV)
                ##print(FuelCan1['Count'], ' small fuel cans.', FuelCan2['Count'], ' medium fuel cans.', FuelCan3['Count'], ' large fuel cans.')
                ##print(initialMass, finalMass)
                ##print('dv:', dV, 'fuelcan1s:', FuelCan1['Count'], 'fuelcan2s:', FuelCan2['Count'], 'fuelcan3s:', FuelCan3['Count'], 'initialmass:', initialMass, 'finalMass:', finalMass, 'fuelTotalMass:', fuelTotalMass, 'fuelcanmass', fuelCanMass)

        formattedDV = '{0:.2f}'.format(dV)
        ##print(formattedDV)
        print('DeltaV is:', formattedDV, FuelCan1['Count'], ' small fuel cans.', FuelCan2['Count'], ' medium fuel cans.', FuelCan3['Count'], ' large fuel cans.', largeFuelCan1['Count'], ' big small fuel cans.', largeFuelCan2['Count'], ' big medium fuel cans.', largeFuelCan3['Count'], ' big large fuel cans.', 'With a thrust to weight ratio of', twr)
        ##print(fuelCanMass)
        ##print(engineModel)
        print("Start: ", str(convert_KG_To_Ton(initialMass)), "End: ", str(convert_KG_To_Ton(finalMass)))
        
    payloadMassTons = convert_KG_To_Ton(initialMass)
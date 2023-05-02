'''
Ryan Muncy 04/07/2023

Last Edited 04/07/2023

StagedWombo
The purpose of this is to expand upon the capabilities of WomboCombo3 so that it can calculate fuel needed for each engine for a given payloadf weight and deltaV, and then take that weight and continue onto the next stage anbd do those calculations again.
'''

from math import *
from decimal import *

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
    twr = Decimal(T/W)
    return(twr)

'''
engineLibrary = {'LV-909': {'Mass': Decimal(0.5), 'Thrust': Decimal(14.783), 'Isp': Decimal(834.70)},
                          'LV-30': {'Mass': Decimal(1.25), 'Thrust':Decimal(205.161) , 'Isp': Decimal(2602.30)},
                           'LV-45': {'Mass': Decimal(1.5), 'Thrust': Decimal(167.969), 'Isp': Decimal(2455.0)}}
'''
engineLibrary = {'LV-909': {'Mass': Decimal(0.5), 'Thrust': Decimal(14.7), 'Isp': Decimal(835.0)},
                          'LV-30': {'Mass': Decimal(1.25), 'Thrust':Decimal(205.1) , 'Isp': Decimal(2602.0)},
                           'LV-45': {'Mass': Decimal(1.5), 'Thrust': Decimal(167.9), 'Isp': Decimal(2455.0)}}

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

#getting input
numStages = int(input("How many stages would you like? "))
desiredDeltaV = int(input("Please enter your deisred deltaV: "))
payloadMassTons = Decimal(input("Please enter your payload Mass in Tons: "))
engineModel = 'LV-909'
#fuelcans are dicitonaries so i can keep track of multiple pieces of info at once
'''
FuelCan1 = {'TotalMass': Decimal(0.5625), 'NonFuelMass': Decimal(0.0625), 'Count': 0}
FuelCan2 = {'TotalMass': Decimal(1.125), 'NonFuelMass': Decimal(0.125), 'Count': 0}
FuelCan3 = {'TotalMass': Decimal(2.25), 'NonFuelMass': Decimal(0.25), 'Count': 0}
fuelCans = [FuelCan1]
'''

FuelCan1 = {'TotalMass': Decimal(0.6), 'NonFuelMass': Decimal(0.06), 'Count': 0}
FuelCan2 = {'TotalMass': Decimal(1.13), 'NonFuelMass': Decimal(0.13), 'Count': 0}
FuelCan3 = {'TotalMass': Decimal(2.25), 'NonFuelMass': Decimal(0.25), 'Count': 0}
fuelCans = [FuelCan1]

def reset_Var():
    global FuelCan1
    global FuelCan2
    global FuelCan3
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
    FuelCan1['Count'] = 0
    FuelCan2['Count'] = 0
    FuelCan3['Count'] = 0
    fuelCans = [FuelCan1]
    

def part_Counter():
    #this iterates through fuelCans to count how many there are so i can keep track of it later
    global FuelCan1
    global FuelCan2
    global FuelCan3
    global fuelCanMassTons
    global fuelTotalMassTons
    global totalDryMass
    global fuelCans
    ##for i in fuelCans:
        ##i['Count'] +=1
    fuelCanMassTons = (FuelCan1['Count'] * FuelCan1['NonFuelMass']) + (FuelCan2['Count'] * FuelCan2['NonFuelMass']) + (FuelCan3['Count'] * FuelCan3['NonFuelMass'])
    fuelTotalMassTons = (FuelCan1['Count'] * FuelCan1['TotalMass']) + (FuelCan2['Count'] * FuelCan2['TotalMass']) + (FuelCan3['Count'] * FuelCan3['TotalMass'])
    
part_Counter()
##print(FuelCan1)
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
    engineIsp = engineLibrary[engineModel]['Isp']
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

    for x in engineLibrary.keys():
        print(payloadMass)
        reset_Var()
        ##print(dV)
        engineModel = x
        print(engineModel)
        while dV < desiredDeltaV:
            part_Counter()
            ##print(fuelCans)
            variableCalculatorWorking()
            variableCalculatorUsable()
            ##print(' ')
            ##print(fuelCans)
            if FuelCan1['Count'] >= 1:
                fuelCans.pop()
                fuelCans.append(FuelCan2)
                FuelCan1['Count'] = 0
                FuelCan2['Count'] += 1
                ##print(fuelCans)
                ##print("tank2 added")

            elif FuelCan2['Count'] >= 1:
                fuelCans.pop()
                fuelCans.append(FuelCan3)
                FuelCan2['Count'] = 0
                FuelCan3['Count'] += 1
                ##print(fuelCans)
                ##print("tank3 added")
            else:
                fuelCans.append(FuelCan1)
                FuelCan1['Count'] += 1
                ##print(fuelCans)
                ##print("tank1 added")
            part_Counter()
            variableCalculatorWorking()
            variableCalculatorUsable()
            ##print(dV)
            ##print(FuelCan1['Count'], ' small fuel cans.', FuelCan2['Count'], ' medium fuel cans.', FuelCan3['Count'], ' large fuel cans.')

        formattedDV = '{0:.2f}'.format(dV)
        print(formattedDV)
        print(FuelCan1['Count'], ' small fuel cans.', FuelCan2['Count'], ' medium fuel cans.', FuelCan3['Count'], ' large fuel cans.')
        ##print(fuelCanMass)
        ##print(engineModel)
        print("Start: ", str(convert_KG_To_Ton(initialMass)), "End: ", str(convert_KG_To_Ton(finalMass)))
        
    payloadMassTons = convert_KG_To_Ton(initialMass)
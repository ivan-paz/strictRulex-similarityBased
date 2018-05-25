import json
from ruleExtraction import ruleExtraction
# reads a json file containing sets of presets
with open('presets.json') as json_data:
    setOfPresets = json.load(json_data)

def convertPresetSetINTORules(Presets):
    rules = [ ]
    for preset in Presets:
        temporal = []
        for i in range( 0, len(preset) - 1 ):
            entrance = preset[i]
            temporal.append(set([entrance]))
        temporal.append(preset[-1])
        rules.append(temporal)
    return rules

#    rule Extraction
bunch_of_rules = []
for Presets in setOfPresets:
    Rules = convertPresetSetINTORules(Presets)
    rules = ruleExtraction(Rules,1)
    bunch_of_rules.append(rules)

thefile = open("Output.txt", "w")
for item in bunch_of_rules:
    for rule in item:
        thefile.write("%s\n" % rule)
    thefile.write("%s\n" % '------------------------------------------')
thefile.close()



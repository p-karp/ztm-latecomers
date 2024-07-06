import pandas as pd
import findBusStopNames as fBSN

'''
INPUT
sfp - schedule file path
dfp - data file path

OUTPUT
D - data dict
S - schedule dict
'''
def processing (sfp: str, dfp: str) -> dict:
    df = pd.read_csv(dfp)
    D = {}

    for _, row in df.iterrows():
        values = row.values.tolist()
        if values[2] in D.keys():
            if values[0] in D[values[2]].keys():
                if values[1] in D[values[2]][values[0]].keys():
                    if values[4] in D[values[2]][values[0]][values[1]].keys():
                        D[values[2]][values[0]][values[1]][values[4]].append(values[5])
                    else: 
                        D[values[2]][values[0]][values[1]][values[4]] = [values[5]]
                else:
                    D[values[2]][values[0]][values[1]] = {values[4]: [values[5]]}
            else:
                D[values[2]][values[0]] = {values[1]: {values[4]: [values[5]]}}
        else: 
            D[values[2]] = {values[0]: {values[1]:{values[4]: [values[5]]}}}

    Pairs = fBSN.findPairs()
    df = pd.read_csv(sfp, encoding='windows-1250', delimiter=";")
    df = df.drop_duplicates()
    S = {}

    for _, row in df.iterrows():
        values = row.values.tolist()
        for p in Pairs:
            if int(p[0]) == values[0]: values[0] = p[1]

        if values[2] in S.keys():
            if values[0] in S[values[2]].keys():
                if values[1] in S[values[2]][values[0]].keys():
                    if values[3] in S[values[2]][values[0]][values[1]].keys():
                        S[values[2]][values[0]][values[1]][values[3]].append(values[4])
                    else: 
                        S[values[2]][values[0]][values[1]][values[3]] = [values[4]]
                else:
                    S[values[2]][values[0]][values[1]] = {values[3]: [values[4]]}
            else:
                S[values[2]][values[0]] = {values[1]: {values[3]: [values[4]]}}
        else: 
            S[values[2]] = {values[0]: {values[1]:{values[3]: [values[4]]}}}
    
    return D, S
    


# '''Pokaz jak to wygląda w środku'''
# D, S = processing('./zebraneDane/rj_30-06.csv', './zebraneDane/dane_30-06.csv')
# print(D[6]['KS Polonia'])
# print(S[6]['KS Polonia'])

# Problem z:    7053;02;6;2024-06-30;08:28:00
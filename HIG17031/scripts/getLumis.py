#!/usr/bin/env python

if __name__ == "__main__":
    import sys
    model = sys.argv[1]
    scen = sys.argv[2]
    variant = ''
    if len(sys.argv) >= 4:
        variant = sys.argv[3]

    if model != 'A1_5PD':
        if 'phase2' in variant:
            lumis = ['1000', '3000']
            if 'S2NF' in scen:
                lumis = ['3000']
        else:
            lumis = ['35.9', '100', '300', '3000']
            if 'S2NF' in scen:
                lumis = ['300']
    else:
        if 'phase2' in variant and not 'S2NF' in scen:
            lumis = ['3000']
        else:
            lumis = []
    print ' '.join(lumis)

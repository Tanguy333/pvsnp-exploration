# tools/

## cryptominisat5.exe (non versionne -- voir .gitignore)

CryptoMiniSat v5.14.5, binaire officiel Windows x86_64 (clauses XOR
natives + elimination gaussienne), utilise par F-011 etape 21c.

Provenance :
    gh release download "release/v5.14.5" -R msoos/cryptominisat -p "*windows*"
    unzip cryptominisat5-v5.14.5-windows-x86_64.zip

Usage type : cryptominisat5.exe --maxtime 1200 instance.cnf
(format DIMACS etendu : lignes "x l1 l2 ... 0" = clauses XOR).

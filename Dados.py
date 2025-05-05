
from Codigos import Ranged, Melee, Protecao, Item, Consumivel, Explosivo, Municao, Melhoria, Kit, Proficiencia

Munições = {
    "9x19mm HP": lambda: Municao("9x19mm HP", 0, "9x19mm", 1, 4),
    "9x19mm FMJ": lambda: Municao("9x19mm FMJ", 0, "9x19mm", 2, 2),
    "9x19mm +P HP": lambda: Municao("9x19mm +P HP", 0, "9x19mm", 1, 6),
    "9x19mm +P FMJ": lambda: Municao("9x19mm +P FMJ", 0, "9x19mm", 2, 4),

    "9x18mm HP": lambda: Municao("9x18mm HP", 0, "9x18mm", 1, 2),
    "9x18mm FMJ": lambda: Municao("9x18mm FMJ", 0, "9x18mm", 2, 1),
    ".380ACP FMJ": lambda: Municao(".380ACP FMJ", 0, ".380 ACP", 2, 1),
    ".380ACP HP": lambda: Municao(".380ACP HP", 0, ".380 ACP", 1, 2),

    ".40 S&W HP": lambda: Municao(".40 S&W HP", 0, ".40S&W", 1, 2),
    ".40 S&W FMJ": lambda: Municao(".40 S&W FMJ", 0, ".40S&W", 2, 1),
    "5.7x28mm FMJ": lambda: Municao("5.7x28mm FMJ", 0, "5.7x28mm", 1, 2),
    "5.7x28mm AP": lambda: Municao("5.7x28mm FMJ", 0, "5.7x28mm", 3, 0),
    "4.6x30mm FMJ": lambda: Municao("4.6x30mm FMJ", 0, "4.6x30mm", 2, 2),
    "4.6x30mm AP": lambda: Municao("4.6x30mm AP", 0, "4.6x30mm", 3, 0),

    ".45ACP HP": lambda: Municao(".45ACP HP", 0, ".45ACP", 1, 5),
    ".45ACP FMJ": lambda: Municao(".45ACP FMJ", 0, ".45ACP", 2, 3),
    ".45ACP +P HP": lambda: Municao(".45ACP +P HP", 0, ".45ACP", 1, 7),
    ".45ACP +P FMJ": lambda: Municao(".45ACP +P FMJ", 0, ".45ACP", 2, 5),

    "10mm Auto FMJ": lambda: Municao("10mm Auto FMJ", 0, "10mm Auto", 2, 4),
    "10mm Auto HP": lambda: Municao("10mm Auto HP", 0, "10mm Auto", 2, 6),
    ".50AE FMJ": lambda: Municao(".50AE FMJ", 0, ".50AE", 3, 6),

    ".357Mag FMJ": lambda: Municao(".357Mag FMJ", 0, ".357Mag", 3, 4),
    ".357Mag HP": lambda: Municao(".357Mag HP", 0, ".357Mag", 2, 6),
    ".44Mag FMJ": lambda: Municao(".44Mag FMJ", 0, ".44Mag", 3, 6),
    ".44Mag HP": lambda: Municao(".44Mag HP", 0, ".44Mag", 2, 8),
    ".454Casull FMJ": lambda: Municao(".454Casull FMJ", 0, ".454Casull", 4, 6),
    ".454Casull HP": lambda: Municao(".454Casull HP", 0, ".454Casull", 4, 8),
    ".500Mag FMJ": lambda: Municao(".500Mag FMJ", 0, ".500Mag", 5, 6),
    ".500Mag HP": lambda: Municao(".500Mag HP", 0, ".500Mag", 4, 10),

    ".410Bore #9 Buck": lambda: Municao(".410Bore #6 Buck", 0, ".410Bore", 1, 8),
    ".410Bore #00 Buck": lambda: Municao(".410Bore #00 Buck", 0, ".410Bore", 2, 4),
    ".410Bore #00) Slug": lambda: Municao(".410Bore #00) Slug", 0, ".410Bore", 3, 2),
    "12ga #4 Buck": lambda: Municao("12 gauge #4 Buckshot", 0, "12ga", 1, 8),
    "12ga #00 Buck": lambda: Municao("12 gauge #00 Buckshot", 0, "12ga", 2, 8),
    "12ga Slug": lambda: Municao("12ga Slug", 0, "12ga", 2, 4),
    "12ga Sabot Slug": lambda: Municao("12ga Sabot Slug", 0, "12ga", 3, 2),
    "12ga Dragons Breath": lambda: Municao("12ga Dragons Breath", 0, "12ga", 0, -20),
    "23x75mmr Barrikada": lambda: Municao("23x75mmr Barrikada", 0, "23x75mmr", 6, 5),
    "23x75mmr Volna-R": lambda: Municao("23x75mmr Volna-R", 0, "23x75mmr", 4, 6),
    "23x75mmr Shrapnel-10": lambda: Municao("23x75mmr Shrapnel-10", 0, "23x75mmr", 4, 8),
    "23x75mmr Shrapnel-25": lambda: Municao("23x75mmr Shrapnel-25", 0, "23x75mmr", 4, 8),
    "23x75mmr Zvezda": lambda: Municao("23x75mmr Zvezda", 0, "23x75mmr", 0, -10),
    "23x75mmr Siren-7": lambda: Municao("23x75mmr Siren-7", 0, "23x75mmr", 0, -15),
    "23x75mmr Cheremukha-7": lambda: Municao("23x75mmr Cheremukha-7", 0, "23x75mmr", 0, -15),

    ".300Blk SuperS": lambda: Municao(".300Blk SuperS", 0, ".300Blk", 4, 6),
    ".300Blk SubS": lambda: Municao(".300Blk SubS", 0, ".300Blk", 4, 2),
    "9x39mm SuperS": lambda: Municao("9x39mm SuperS", 0, "9x39mm", 4, 6),
    "9x39mm SubS": lambda: Municao("9x39mm SubS", 0, "9x39mm", 4, 2),

    "7.62x39mm FMJ": lambda: Municao("7.62x39mm FMJ", 0, "7.62x39mm", 4, 2),
    "7.62x39mm SP": lambda: Municao("7.62x39mm SP", 0, "7.62x39mm", 4, 4),
    "7.62x39mm HP": lambda: Municao("7.62x39mm HP", 0, "7.62x39mm", 3, 6),
    "5.56x45mm FMJ": lambda: Municao("5.56x45mm FMJ", 0, "5.56x45mm", 4, 4),
    "5.56x45mm HP": lambda: Municao("5.56x45mm FMJ", 0, "5.56x45mm", 3, 6),
    "5.45x39mm FMJ": lambda: Municao("5.45x39mm FMJ", 0, "5.45x39mm", 4, 3),
    "5.45x39mm SubS": lambda: Municao("5.45x39mm FMJ", 0, "5.45x39mm", 3, 3),
    "5.45x39mm SP": lambda: Municao("5.45x39mm FMJ", 0, "5.45x39mm", 3, 5),
    "7.92Mauser FMJ": lambda: Municao("7.92 Mauser FMJ", 0, "7.92x57mm", 3, 6),
    ".223Remington FMJ": lambda: Municao(".223 Remington FMJ", 0, ".223 Remington", 4, 3),
    ".223Remington HP": lambda: Municao(".223 Remington FMJ", 0, ".223 Remington", 3, 5),

    ".30-06 FMJ": lambda: Municao(".30-06 FMJ", 0, ".30-06", 5, 4),
    ".30-06 SP": lambda: Municao(".30-06 SP", 0, ".30-06", 4, 6),
    "7.62x54mmr FMJ": lambda: Municao("7.62x54mmr FMJ", 0, "7.62x54mmr", 5, 4),
    "7.62x54mmr SP": lambda: Municao("7.62x54mmr SP", 0, "7.62x54mmr", 4, 6),
    "7.62x51mm FMJ": lambda: Municao("7.62x51mm FMJ", 0, "7.62x51mm", 5, 3),
    "7.62x51mm SP": lambda: Municao("7.62x51mm SP", 0, "7.62x51mm", 4, 5),
    ".308Remington FMJ": lambda: Municao(".308Remington FMJ", 0, ".308Remington", 5, 4),
    ".308Remington SP": lambda: Municao(".308Remington SP", 0, ".308Remington", 4, 6),
    ".408Cheytac FMJ": lambda: Municao(".408Cheytac FMJ", 0, ".408Cheytac", 6, 10),
    ".375Cheytac FMJ": lambda: Municao(".357Cheytac FMJ", 0, ".408Cheytac", 7, 6),
    ".50BMG FMJ": lambda: Municao(".50BMG FMJ", 0, ".50BMG", 8, 12),
    ".50BMG AP": lambda: Municao(".50BMG AP", 0, ".50BMG", 9, 8),

    ".45-70Gov FMJ": lambda: Municao(".45-70Gov FMJ", 0, ".45-70Gov", 3, 5),
    ".45-70Gov HP": lambda: Municao(".45-70Gov FMJ", 0, ".45-70Gov", 2, 7),
    ".30 Carbine FMJ": lambda: Municao(".30 Carbine FMJ", 0, ".30 Carbine", 3, 3),
    ".30 Carbine HP": lambda: Municao(".30 Carbine HP", 0, ".30 Carbine", 2, 6),
}

Rangeds = {
    "Glock 17": lambda: Ranged("Glock 17", 1.2, "Pistola", "Semi", "Comum", "9x19mm", 17),
    "Glock 18": lambda: Ranged("Glock 18", 1.2, "Pistola", "Auto", "Comum", "9x19mm", 17),
    "Glock 19": lambda: Ranged("Glock 19", 1.2, "Pistola", "Semi", "Incomum", "9x19mm", 17),
    "Glock 21": lambda: Ranged("Glock 21", 1.3, "Pistola", "Semi", "Incomum", ".45ACP", 13),
    "Glock 23": lambda: Ranged("Glock 21", 1.3, "Pistola", "Semi", "Incomum", ".40S&W", 13),
    "M17": lambda: Ranged("M17", 1.3, "Pistola", "Semi", "Comum", "9x19mm", 15),
    "M1911": lambda: Ranged("M1911", 1.5, "Pistola", "Semi", "Comum", ".45ACP", 7),
    "MP1911": lambda: Ranged("M1911", 1.8, "Pistola", "Auto", "Incomum", ".45ACP", 15),
    "M45A1": lambda: Ranged("M45A1", 1.4, "Pistola", "Semi", "Incomum", ".45ACP", 7),
    "P226": lambda: Ranged("P226", 1.3, "Pistola", "Semi", "Incomum", "9x19mm", 16),
    "Makarov": lambda: Ranged("Makarov", 0.9, "Pistola", "Semi", "Comum", "9x18mm", 10),
    "Micro Uzi": lambda: Ranged("Micro Uzi", 1.2, "Pistola", "Auto", "Incomum", "9x19mm", 25),
    "Tec-9": lambda: Ranged("Tec-9", 1.6, "Pistola", "Auto", "Incomum", "9x19mm", 20),
    "Izhezsk PB": lambda: Ranged("Izhezsk PB", 1.2, "Pistola", "Semi", "Incomum", "9x18mm", 10),
    "Skorpion Vz": lambda: Ranged("Skorpion Vz", 0.9, "Pistola", "Auto", "Comum", "9x18mm", 20),
    "Browning HP": lambda: Ranged("Browning HP", 1.3, "Pistola", "Semi", "Comum", "9x19mm", 13),
    "Beretta M9": lambda: Ranged("Beretta M9", 1.4, "Pistola", "Semi", "Incomum", "9x19mm", 15),
    "Beretta M93r": lambda: Ranged("Beretta M93r", 1.4, "Pistola", "Rajada", "Rara", "9x19mm", 15),
    "Gsh-18": lambda: Ranged("Gsh-18", 1.8, "Pistola", "Semi", "Incomum", "9x19mm", 18),
    "USP-9": lambda: Ranged("USP-9", 1.7, "Pistola", "Semi", "Rara", "9x19mm", 15),
    "USP-45": lambda: Ranged("USP-45", 1.7, "Pistola", "Semi", "Rara", ".45ACP", 12),
    "Five Seven": lambda: Ranged("Five Seven", 1.6, "Pistola", "Semi", "Exótica", "5.7x28mm", 21),

    "MP412 Rex": lambda: Ranged("MP412 Rex", 2.5, "Revolver", "Dupla", "Comum", ".357Mag", 6),
    "SW357": lambda: Ranged("SW357", 2.6, "Revolver", "Dupla", "Comum", ".357Mag", 6),
    "Magnum 44": lambda: Ranged("Magnum 44", 2.7, "Revolver", "Dupla", "Incomum", ".44Mag", 6),
    "Mateba 6": lambda: Ranged("Mateba 6", 2.9, "Revolver", "Semi", "Rara", ".44Mag", 6),
    "500 S&W": lambda: Ranged("500 S&W", 2.2, "Revolver", "Dupla", "Rara", ".500Mag", 6),
    "Taurus Judge": lambda: Ranged("Taurus Judge", 2.4, "Revolver", "Dupla", "Rara", ".410Bore", 5),
    "Raging Bull": lambda: Ranged("Raging Bull", 2.7, "Revolver", "Dupla", "Rara", ".454Casull", 5),
    "Raging Judge": lambda: Ranged("Raging Judge", 3.1, "Revolver", "Dupla", "Exótica", ".454Casull", 6),

    "M1014": lambda: Ranged("M1014", 2.3, "Escopeta", "Semi", "Comum", "12ga", 7),
    "Ithaca 37": lambda: Ranged("Ithaca 37", 2.1, "Escopeta", "Pump", "Comum", "12ga", 5),
    "VEPR 12": lambda: Ranged("VEPR 12", 2.5, "Escopeta", "Semi", "Incomum", "12ga", 8),
    "Saiga 12": lambda: Ranged("Saiga 12", 2.4, "Escopeta", "Auto", "Incomum", "12ga", 8),
    "SPAS 12": lambda: Ranged("SPAS 12", 2.7, "Escopeta", "Semi", "Rara", "12ga", 7),
    "AA-12": lambda: Ranged("AA-12", 3.4, "Escopeta", "Auto", "Exótica", "12ga", 8),
    "USAS-12": lambda: Ranged("USAS-12", 3.2, "Escopeta", "Auto", "Exótica", "12ga", 9),
    "KS-23": lambda: Ranged("KS-23", 3.1, "Escopeta", "Semi", "Exótica", "23x75mmR", 4),

    "MP5": lambda: Ranged("MP5", 2.2, "Submetralhadora", "Auto", "Comum", "9x19mm", 30),
    "Uzi": lambda: Ranged("Uzi", 2.4, "Submetralhadora", "Auto", "Incomum", "9x19mm", 30),
    "MP5K": lambda: Ranged("MP5K", 2.0, "Submetralhadora", "Auto", "Incomum", "9x19mm", 30),
    "Thompson": lambda: Ranged("Thompson", 2.8, "Submetralhadora", "Auto", "Comum", ".45Acp", 30),
    "MP40": lambda: Ranged("MP40", 2.5, "Submetralhadora", "Auto", "Comum", "9x19mm", 32),
    "PPSH-41": lambda: Ranged("PPSH-41", 3.2, "Submetralhadora", "Auto", "Incomum", "7.62x25mm", 71),
    "Mac-10": lambda: Ranged("Mac-10", 2.0, "Submetralhadora", "Auto", "Incomum", ".45Acp", 30),
    "AKS-74U": lambda: Ranged("AKS-74U", 2.4, "Submetralhadora", "Auto", "Comum", "5.45x39mm", 30),
    "PP19 Bizon": lambda: Ranged("PP19 Bizon", 2.7, "Submetralhadora", "Auto", "Comum", "9x18mm", 64),
    "PP19 Vityaz": lambda: Ranged("PP19 Vityaz", 2.3, "Submetralhadora", "Auto", "Comum", "9x19mm", 30),
    "PP2000": lambda: Ranged("PP2000", 2.1, "Submetralhadora", "Auto", "Incomum", "9x19mm", 30),
    "MP40": lambda: Ranged("MP40", 2.6, "Submetralhadora", "Auto", "Comum", "9x19mm", 32),
    "MP7": lambda: Ranged("MP7", 2.2, "Submetralhadora", "Auto", "Incomum", "4.6x30mm", 40),
    "P90": lambda: Ranged("P90", 2.2, "Submetralhadora", "Auto", "Incomum", "5.7x28mm", 50),
    "MP9": lambda: Ranged("MP9", 2.0, "Submetralhadora", "Auto", "Rara", "9x19mm", 30),
    "Kriss Vector 45": lambda: Ranged("Kriss Vector 45", 2.2, "Submetralhadora", "Auto", "Exótica", ".45ACP", 25),
    "UMP 45": lambda: Ranged("UMP 45", 2.2, "Submetralhadora", "Auto", "Rara", ".45ACP", 25),

    "Winchester 1886": lambda: Ranged("Winchester 1886", 2.5, "Espingarda", "Alavanca", "Comum", ".45-70Gov", 5),
    "Taurus Rossi Judge": lambda: Ranged("Taurus Rossi Judge", 2.8, "Espingarda", "Dupla", "Rara", ".410Bore", 5),
    
    "M4A1": lambda: Ranged("M4A1", 3.5, "Carabina", "Auto", "Comum", "5.56x45mm", 30),
    "M4": lambda: Ranged("M4", 3.5, "Carabina", "Rajada", "Comum", "5.56x45mm", 30),
    "Honey Badger": lambda: Ranged("Honey Badger", 3.3, "Carabina", "Auto", "Rara", ".300Blk", 30),
    "AKS-74": lambda: Ranged("AKS-74", 3.6, "Carabina", "Auto", "Comum", "5.45x39mm", 30),
    "AK-105": lambda: Ranged("AK-105", 3.4, "Carabina", "Auto", "Incomum", "5.45x39mm", 30),
    "G36K": lambda: Ranged("G36C", 3.4, "Carabina", "Auto", "Rara", "5.56x45mm", 30),
    "AK-105": lambda: Ranged("AK-105", 3.3, "Carabina", "Auto", "Incomum", "5.45x39mm", 30),
    "SR-3M": lambda: Ranged("SR-3M", 3.1, "Carabina", "Auto", "Rara", "9x39mm", 20),
    "Groza-1": lambda: Ranged("Groza-1", 3.4, "Carabina", "Auto", "Rara", "7.62x39mm", 30),
    "Groza-4": lambda: Ranged("Groza-4", 3.4, "Carabina", "Auto", "Rara", "9x39mm", 20),

    "M16A4": lambda: Ranged("M16A4", 3.7, "Fuzil De Assalto", "Rajada", "Comum", "5.56x45mm", 30),
    "M16A3": lambda: Ranged("M16A3", 3.7, "Fuzil De Assalto", "Auto", "Comum", "5.56x45mm", 30),
    "G36": lambda: Ranged("G36", 3.6, "Fuzil De Assalto", "Auto", "Comum", "5.56x45mm", 30),
    "L85A2": lambda: Ranged("L85A2", 3.7, "Fuzil De Assalto", "Auto", "Comum", "5.56x45mm", 30),
    "HK416": lambda: Ranged("HK416", 3.6, "Fuzil De Assalto", "Auto", "Incomum", "5.56x45mm", 30),
    "AK-47": lambda: Ranged("AK-47", 3.8, "Fuzil De Assalto", "Auto", "Comum", "7.62x39mm", 30),
    "AK-74": lambda: Ranged("AK-74", 3.4, "Fuzil De Assalto", "Auto", "Incomum", "5.45x39mm", 30),
    "AK-103": lambda: Ranged("AK-103", 3.6, "Fuzil De Assalto", "Auto", "Incomum", "7.62x39mm", 30),
    "AK-12M": lambda: Ranged("AK-12M", 3.3, "Fuzil De Assalto", "Auto", "Incomum", "5.45x39mm", 30),
    "AK-15": lambda: Ranged("AK-15", 3.4, "Fuzil De Assalto", "Auto", "Incomum", "7.62x39mm", 30),
    "AN-94 Abakan": lambda: Ranged("AN-94 Abakan", 3.4, "Fuzil De Assalto", "Rajada", "Exótica", "5.45x39mm", 30),
    

    "M1-Garand": lambda: Ranged("M1-Garand", 3.2, "Fuzil De Batalha", "Auto", "Comum", ".30-06", 20),
    "FAL": lambda: Ranged("FAL", 4.0, "Fuzil De Batalha", "Auto", "Comum", "7.62x51mm", 20),
    "M14": lambda: Ranged("M14", 4.4, "Fuzil De Batalha", "Semi", "Comum", "7.62x51mm", 10),
    "HK417": lambda: Ranged("HK417", 4.0, "Fuzil De Batalha", "Auto", "Incomum", "7.62x51mm", 20),
    "AK-308": lambda: Ranged("AK-308", 3.6, "Fuzil De Assalto", "Auto", "Rara", "7.62x51mm", 20),
    "Beowulf ECR": lambda: Ranged("Beowulf ECR", 4.0, "Fuzil De Batalha", "Auto", "Rara", ".50Beowulf", 10),
    "G3": lambda: Ranged("G3", 4.4, "Fuzil De Batalha", "Auto", "Comum", "7.62x51mm", 20),
    "SCAR-H": lambda: Ranged("SCAR-H", 4.5, "Fuzil De Batalha", "Auto", "Rara", "7.62x51mm", 20),
    "Dragunov SVU-A": lambda: Ranged("Dragunov SVU-A", 3.8, "DMR", "Auto", "Rara", "7.62x54mmr", 10),

    "SKS": lambda: Ranged("SKS", 2.8, "DMR", "Semi", "Comum", "7.62x39mm", 10),
    "M21": lambda: Ranged("M21", 2.5, "DMR", "Semi", "Comum", "7.62x51mm", 10),
    "SA58 SPR": lambda: Ranged("SA58 SPR", 3.0, "DMR", "Semi", "Comum", "7.62x51mm", 20),
    "MK11": lambda: Ranged("MK11", 2.5, "DMR", "Semi", "Incomum", "7.62x51mm", 20),
    "M110RSASS": lambda: Ranged("M110RSASS", 2.5, "DMR", "Semi", "Rara", "7.62x51mm", 10),
    "SCAR SSR": lambda: Ranged("SCAR SSR", 3.8, "DMR", "Semi", "Rara", "7.62x51mm", 20),
    "Beowulf TCR": lambda: Ranged("Beowulf TCR", 3.0, "DMR", "Semi", "Rara", ".50Beowulf", 10),
    "SVK-12": lambda: Ranged("SVK-12", 2.5, "DMR", "Auto", "Incomum", "7.62x54mmr", 20),
    "Dragunov SVU": lambda: Ranged("Dragunov SVU", 2.8, "DMR", "Semi", "Rara", "7.62x54mmr", 10),
    "VSS Vintorez": lambda: Ranged("VSS Vintorez", 2.4, "DMR", "Semi", "Rara", "9x39mm", 10),

    "Mosin Nagant": lambda: Ranged("Mosin Nagant", 3.6, "Fuzil De Precisão", "Bolt", "Comum", "7.62x54mmr", 5),
    "Kar-98k": lambda: Ranged("Kar-98k", 3.6, "Fuzil De Precisão", "Bolt", "Comum", "7.92x57mm", 5),
    "M40A1": lambda: Ranged("M40A1", 2.7, "Fuzil De Precisão", "Bolt", "Comum", "7.62x51mm", 3),
    "Model 700": lambda: Ranged("Model 700", 3.0, "Fuzil De Precisão", "Bolt", "Comum", ".306Remington", 6),
    "Dragunov SVD": lambda: Ranged("Dragunov SVD", 4.2, "Fuzil De Precisão", "Semi", "Comum", "7.62x54mmr", 10),
    "AWP": lambda: Ranged("AWP", 3.1, "Fuzil De Precisão", "Bolt", "Incomum", ".308Remington", 10),
    "AWS": lambda: Ranged("AWS", 3.3, "Fuzil De Precisão", "Bolt", "Rara", ".308Remington", 10),
    "AWM": lambda: Ranged("AWM", 3.8, "Fuzil De Precisão", "Bolt", "Rara", ".338LapuaMag", 5),
    "TRG-42": lambda: Ranged("TRG-42", 4.1, "Fuzil De Precisão", "Bolt", "Rara", ".338LapuaMag", 5),
    "WA2000": lambda: Ranged("WA2000", 3.8, "Fuzil De Precisão", "Semi", "Exótica", ".308Remington", 5),
    "Dragunov SVDs": lambda: Ranged("Dragunov SVDs", 3.4, "Fuzil De Precisão", "Semi", "Incomum", "7.62x54mmr", 10),
    "SV-98": lambda: Ranged("SV-98", 3.6, "Fuzil De Precisão", "Bolt", "Incomum", "7.62x54mmr", 5),
    "M200 Intervention": lambda: Ranged("M200 Intervention", 5.8, "Fuzil De Precisão", "Bolt", "Exótica", ".408Cheytac", 10),
    "M107": lambda: Ranged("M107", 6.5, "Fuzil De Precisão", "Semi", "Incomum", ".50BMG", 10),
    "M82A1": lambda: Ranged("M82A1", 6.5, "Fuzil De Precisão", "Semi", "Rara", ".50BMG", 10),
    "GMC-6 Lynx": lambda: Ranged("GMC-6 Lynx", 6.0, "Fuzil De Precisão", "Semi", "Exótica", ".50BMG", 10),
    "Hecate II": lambda: Ranged("Hecate II", 6.0, "Fuzil De Precisão", "Bolt", "Rara", ".50BMG", 5),

    "MG36": lambda: Ranged("MG36", 3.6, "Metralhadora leve", "Auto", "Incomum", "5.56x45mm", 100),
    "M249": lambda: Ranged("M249", 3.8, "Metralhadora leve", "Auto", "Comum", "5.56x45mm", 100),
    "RPK": lambda: Ranged("RPK", 3.6, "Metralhadora leve", "Auto", "Comum", "7.62x39mm", 45),
    "RPK-74": lambda: Ranged("RPK-74", 3.5, "Metralhadora leve", "Auto", "Comum", "5.45x39mm", 45),
    "RPK-12": lambda: Ranged("RPK-12", 3.5, "Metralhadora leve", "Auto", "Incomum", "5.45x39mm", 45),
    "AK-12Br": lambda: Ranged("AK-12Br", 3.8, "Metralhadora leve", "Auto", "Rara", "5.45x39mm", 95),
    "HK21": lambda: Ranged("HK21", 4.2, "Metralhadora leve", "Auto", "Comum", "7.62x51mm", 100),
    "RPK-16": lambda: Ranged("RPK-16", 3.6, "Metralhadora leve", "Auto", "Rara", "5.45x39mm", 95),
    "MG3Kws": lambda: Ranged("MG3Kws", 3.8, "Metralhadora leve", "Auto", "Rara", "7.62x51mm", 50),
    "MG42": lambda: Ranged("MG42", 4.4, "Metralhadora leve", "Auto", "Rara", "7.92x57mm", 50),
}

Melees = {
    "Faca de Cozinha": lambda: Melee("Faca de Cozinha", 1, "Cortante", "Faca", "Comum"),
    "Faca M9": lambda: Melee("Faca Bowie", 2, "Cortante", "Faca", "Incomum"),
    "Faca Bowie": lambda: Melee("Faca Bowie", 1.5, "Cortante", "Faca", "Rara"),
    "Karambit": lambda: Melee("Karambit", 1.5, "Cortante", "Faca", "Exótica"),
    "Adaga": lambda: Melee("Adaga", 2.5, "Cortante", "Adaga", "Incomum"),
    "Tanto": lambda: Melee("Tanto", 2.5, "Cortante", "Adaga", "Rara"),

    "Machadinha": lambda: Melee("Machadinha", 3, "Cortante", "Machadinha", "Comum"),
    "Tomahawk": lambda: Melee("Tomahawk", 3, "Cortante", "Machadinha", "Incomum"),
    "Pá tatica": lambda: Melee("Pá tatica", 4.5, "Cortante", "Machadinha", "Rara"),

    "Facão": lambda: Melee("Facão", 2.5, "Cortante", "Espada curta", "Comum"),
    "Facão spetnaz": lambda: Melee("Facão spetnaz", 2.5, "Cortante", "Espada curta", "Incomum"),
    "Kukri": lambda: Melee("Kukri", 2.5, "Cortante", "Espada curta", "Rara"),

    "Espada Curta": lambda: Melee("Espada Curta", 4.5, "Cortante", "Espada longa", "Comum"),
    "Espada Longa": lambda: Melee("Espada Longa", 6.5, "Cortante", "Espada longa", "Incomum"),
    "Katana": lambda: Melee("Katana", 6.0, "Cortante", "Espada longa", "Rara"),
    "Zweihander": lambda: Melee("Zweihander", 9.5, "Cortante", "Espada longa", "Lendária"),
    "Wakisashi": lambda: Melee("Wakisashi", 5.0, "Cortante", "Sabre", "Rara"),
    "Odachi": lambda: Melee("Odachi", 7.5, "Cortante", "Sabre", "Exótica"),

    "Machado": lambda: Melee("Machado", 8.5, "Cortante", "Machado", "Comum"),
    "Machado de Bombeiro": lambda: Melee("Machado de Bombeiro", 8.5, "Cortante", "Machado", "Incomum"),

    "Martelo": lambda: Melee("Martelo", 3, "Concussivas", "Martelo", "Comum"),
    "Crowbar": lambda: Melee("Crowbar", 4, "Concussivas", "Martelo", "Incomum"),
    "Chave Inglesa": lambda: Melee("Chave Inglesa", 3, "Concussivas", "Martelo", "Comum"),

    "Pedaço de Pau": lambda: Melee("Pedaço de Pau", 3, "Concussivas", "Porrete", "Comum"),
    "Cassetete": lambda: Melee("Cassetete", 3.5, "Concussivas", "Porrete", "Comum"),
    "Kanabo": lambda: Melee("Kanabo", 8, "Concussivas", "Porrete", "Rara"),

    "Maça": lambda: Melee("Maça", 8, "Concussivas", "Maça", "Rara"),

    "Taco de Cricket": lambda: Melee("Taco de Cricket", 2.5, "Concussivas", "Taco", "Comum"),
    "Taco de Golf": lambda: Melee("Taco de Golf", 2.5, "Concussivas", "Taco", "Comum"),
    "Taco de Baseball": lambda: Melee("Taco de Baseball", 3, "Concussivas", "Taco", "Incomum"),
    "Taco de Baseball de Metal": lambda: Melee("Taco de Baseball de Metal", 4, "Concussivas", "Taco", "Rara"),

    "Marreta": lambda: Melee("Marreta", 15, "Concussivas", "Marreta", "Comum"),
    "Marreta de Demolição": lambda: Melee("Marreta de Demolição", 15, "Concussivas", "Marreta", "Rara"),
}

Protecoes = {    
    "Capacete leve": lambda: Protecao("Capacete leve", 2.5, 3, 4, 4, "Cabeça"),
    "Capacete médio": lambda: Protecao("Capacete médio", 5, 6, 8, 8, "Cabeça"),
    "Capacete pesado": lambda: Protecao("Capacete pesado", 8, 8, 10, 10, "Cabeça"),
    "Altlyn": lambda: Protecao("Altlyn", 8, 8, 12, 10, "Cabeça"),
    "Maska 1-SCH": lambda: Protecao("Maska 1-SCH", 8, 8, 12, 10, "Cabeça"),

    "Protetor facial leve": lambda: Protecao("Protetor facial leve", 1.5, 3, 4, 4, "Rosto"),
    "Protetor facial médio": lambda: Protecao("Protetor facial médio", 3, 6, 8, 8, "Rosto"),
    "Protetor facial pesado": lambda: Protecao("Protetor facial pesado", 4, 7, 10, 10, "Rosto"),
    "Visor Altlyn": lambda: Protecao("Visor Altlyn", 4, 8, 10, 10, "Rosto"),
    "Visor Maska 1-SCH": lambda: Protecao("Visor Maska 1-SCH", 4, 8, 14, 14, "Rosto"),

    "Colete leve": lambda: Protecao("Colete leve", 2, 2, 8, 4, "Torso"),
    "Colete médio": lambda: Protecao("Colete médio", 3, 3, 8, 6, "Torso"),
    "Colete pesado": lambda: Protecao("Colete pesado", 5, 4, 10, 8, "Torso"),

    "Proteção de pernas leve": lambda: Protecao("Proteção de pernas leve", 2.5, 3, 4, 4, "Pernas"),
    "Proteção de pernas média": lambda: Protecao("Proteção de pernas média", 5, 6, 8, 8, "Pernas"),
    "Proteção de pernas pesada": lambda: Protecao("Proteção de pernas pesada", 8, 7, 10, 10, "Pernas"),


    "Proteção de braços leve": lambda: Protecao("Proteção de braços leve", 2.5, 3, 4, 4, "Braços"),
    "Proteção de braços média": lambda: Protecao("Proteção de braços média", 5, 6, 8, 8, "Braços"),
    "Proteção de braços pesada": lambda: Protecao("Proteção de braços pesada", 8, 7, 10, 10, "Braços")
}

Items = {
    "Comunicador": lambda: Item("Comunicador", 0.2),
    "Walkie-Talkie": lambda: Item("Walkie-Talkie", 0.2),
    "Bandoleira": lambda: Item("Bandoleira", 0.5),
    "Coldre": lambda: Item("Coldre", 1.5),
    "Sling": lambda: Item("Sling", 1.5),
    "Coldre melee": lambda: Item("Coldre melee", 1.5),
    "Sling melee": lambda: Item("Sling melee", 1.5),
    "Cinto tático": lambda: Item("Cinto tático", 0.5),

    "Chaves de carro": lambda: Item("Chaves de carro", 0),
    "Chaves": lambda: Item("Chaves", 0),
    "Cartão de acesso": lambda: Item("Cartão de acesso", 0),
    "Documentos pessoais": lambda: Item("Documentos pessoais", 0),

    "Zip tie": lambda: Item("Zip tie", 0),
    "Algema": lambda: Item("Algema", 2),
    "Corda": lambda: Item("Corda", 2),
    "Paracord": lambda: Item("Paracord", 0),
    "Pederneira": lambda: Item("Pederneira", 0),
    "Lockpicker": lambda: Item("Lockpicker", 0),
    "Maçarico": lambda: Item("Maçarico", 1),

    "Bastão de luz": lambda: Item("Bastão de luz", .5),
    "Sinalizador": lambda: Item("Sinalizador", 1.5),
    
    "Zip tie militar": lambda: Item("Zip tie militar", 0),
    "Maçarico Torch-9": lambda: Item("Maçarico Torch-9", 2.5),
    "Broca Sônica Mole": lambda: Item("Broca Sônica Mole", 10),
    "Decodificador Óptico KeyCrack-4": lambda: Item("Decodificador Óptico KeyCrack-4", 2),
    "Espuma de Contenção Rápida FoamLock": lambda: Item("Espuma de Contenção Rápida FoamLock", 4),
    "Escudo Portátil Dobrável TitanFold": lambda: Item("Escudo Portátil Dobrável TitanFold", 10),
}

Consumiveis = {
    "Comida": lambda: Consumivel("Comida", 0.1, 2, 1),
    "Bebida": lambda: Consumivel("Bebida", 0.2, 2, 1),
    "MRE Leve": lambda: Consumivel("MRE Leve", 0.8, 5, 2),
    "MRE Médio": lambda: Consumivel("MRE Médio", 1.4, 10, 4),
    "MRE 12h": lambda: Consumivel("MRE 12h", 3, 15, 6),
    "MRE 24h": lambda: Consumivel("MRE 24h", 6, 30, 12),

    "Bandagem": lambda: Consumivel("Bandagem", 0.2, 2, 0),
    "Gaze": lambda: Consumivel("Gaze", 0.1, 2, 0),
    "Kit Médico Leve": lambda: Consumivel("Kit Médico Leve", 0.5, 2, 0),
    "Kit Médico Médio": lambda: Consumivel("Kit Médico Médio", 1.5, 2, 0),
    "Kit Médico Pesado": lambda: Consumivel("Kit Médico Pesado", 3.5, 2, 0),
}

Explosivos = {
    "Granada Flashbang": lambda: Explosivo("Granada Flashbang", 3, 8, 5, "Concussão"),
    "Granada de fumaça": lambda: Explosivo("Granada de fumaça", 3, 15, 0, "Nenhum"),
    "Granada de fragmentação": lambda: Explosivo("Granada de fragmentação", 3, 15, 50, "Fragmentação"),
    "Granada HE": lambda: Explosivo("Granada HE", 3, 15, 50, "Explosivo"),
    "Granada incendiária": lambda: Explosivo("Granada incendiária", 3, 5, 25, "Incendiário"),
    "Mina antipessoal": lambda: Explosivo("Mina antipessoal", 6, 5, 80, "Explosivo"),
    "Claymore": lambda: Explosivo("Claymore", 6, 5, 80, "Fragmentação"),
    "Breaching charge": lambda: Explosivo("Breaching charge", 3, 2, 15, "Concussão"),
    "C4": lambda: Explosivo("C4", 8, 5, 100, "Explosivo"),
}

Melhorias = {
    "Cabo reforcado": lambda: Melhoria("Cabo reforcado", 0.4, "melee", {"Dano Simples": 2, "Valor Crítico Simples": -1, "Peso": 0.4}),
    "Cabo leve": lambda: Melhoria("Cabo leve", 0.4, "melee", {"Dano Simples": 1, "Valor Crítico Simples": 1, "Peso": -0.2}),
    "Peso extra": lambda: Melhoria("Peso extra", 0.4, "melee", {"Dano Forte": 4, "Valor Crítico Forte": 2, "Peso": 1.2}),
    "Lâmina serrilhada": lambda: Melhoria("Laminâ serrilhada", 0.4, "melee", {"Dano Simples": 2}),

    "MiraHolografica": lambda: Melhoria("MiraHolografica", 0.1, "ranged", {"ShortCrit":-1, "MediumCrit":-1, "Peso": 0.1}),
    "MiraReflex": lambda: Melhoria("MiraReflex", 0.05, "ranged", {"ShortCrit":-1}),
    "MiraAcog4x": lambda: Melhoria("MiraAcog4x", 0.2, "ranged", {"ShortCrit":1, "MediumCrit":-1, "LongCrit": -1}),
    "MiraAcog6x": lambda: Melhoria("MiraAcog6x", 0.25, "ranged", {"ShortCrit":1, "LongCrit": -2}),
    "Luneta8x": lambda: Melhoria("Luneta8x", 0.35, "ranged", {"ShortCrit":3, "MediumCrit": -1, "LongCrit": -2}),

    "Compensador": lambda: Melhoria("Compensador", 0.1, "ranged", {"Recuo": -1}),
    "Quebra-Chamas": lambda: Melhoria("Quebra-Chamas", 0.1, "ranged", {"Recuo": -1}),
    "Supressor .45ACP": lambda: Melhoria("Supressor .45ACP", 0.2, "ranged", {"Alcance Mínimo": 1,"Alcance Máximo": 5, "Dano": -2}),
    "Supressor 9mm": lambda: Melhoria("Supressor 9mm", 0.2, "ranged", {"Alcance Mínimo": 1,"Alcance Máximo": 2, "Dano": -1}),

    "Empunhadura Vertical": lambda: Melhoria("Empunhadura Vertical", 0.15, "ranged", {"Recuo": -1, "Alcance Máximo": 2}),
    "Empunhadura Angulada": lambda: Melhoria("Empunhadura Angulada", 0.2, "ranged", {"Recuo": -1, "Alcance Máximo": 5}),

    "PMAG 60rds": lambda: Melhoria("PMAG 60rds", 1.8, "ranged", {"Capacidade Total": 60}),
    "CMAG 100rds": lambda: Melhoria("CMAG 100rds", 3.4, "ranged", {"Capacidade Total": 100}),


    "Placa Nivel II": lambda: Melhoria("Placa Ceramica Nivel II", 1.2, "protecao", {"Nível Balístico": 2, "Absorção Física": 1, "Absorção Balística": 2}),
    "Placa Nivel III": lambda: Melhoria("Placa Nivel III", 1.4, "protecao", {"Nível Balístico": 3, "Absorção Física": 4, "Absorção Balística": 4}),
    "Placa Nivel IIIA": lambda: Melhoria("Placa Nivel IIIA", 1.6, "protecao", {"Nível Balístico": 4, "Absorção Física": 4, "Absorção Balística": 4}),
    "Placa Nivel IV": lambda: Melhoria("Placa Nivel IV", 2.2, "protecao", {"Nível Balístico": 5, "Absorção Física": 6, "Absorção Balística": 6}),
    "Liga de aço": lambda: Melhoria("Liga de aço", 2.4, "protecao", {"Nível Balístico": 4, "Absorção Física": 2, "Absorção Balística": 4}),
    "Liga de Titânio": lambda: Melhoria("Liga de Titânio", 2.0, "protecao", {"Nível Balístico": 5, "Absorção Física": 4, "Absorção Balística": 6}),
    "Fibra de kevlar": lambda: Melhoria("Fibra de kevlar", 1.6, "protecao", {"Nível Balístico": 3, "Absorção Física": 6, "Absorção Balística": 6}),
    "Amortecimento": lambda: Melhoria("Amortecimento", 2, "protecao", {"Absorção Física": 8, "Absorção Balística": 2})
}

Pools = {}
Pools.update(Items)
Pools.update(Rangeds)
Pools.update(Melees)
Pools.update(Protecoes)
Pools.update(Melhorias)
Pools.update(Munições)
Pools.update(Consumiveis)
Pools.update(Explosivos)

kits_por_nome = {}

kits_por_nome["Agent"] = Kit("Pistola", {"MP5", "Glock 19", "Cassetete",("9x19mm FMJ", 180), "Colete leve", "Proteção de pernas leve", "Proteção de braços leve", ("Comunicador", 1), ("Gaze", 5), ("Bandagem", 5)}, Pools)

kits_por_nome["ATP_Soldat"] = Kit("ATP_Soldat", {"HK416","P226","Faca Bowie",("9x19mm +P FMJ", 76), ("5.56x45mm FMJ", 120), "Colete médio", "Proteção de pernas média", "Proteção de braços média", ("Comunicador", 1), ("Gaze", 5), ("Bandagem", 5)}, Pools)

kits_por_nome["ATP_Engineer"] = Kit("ATP_Engineer", {"AAC Honey Badger","USP-9","Faca Bowie", (".300Blk SuperS", 120), ("9x19mm FMJ", 60), "Colete médio", "Proteção de pernas média", "Proteção de braços média", ("Comunicador", 1), ("Gaze", 5), ("Bandagem", 5)}, Pools)

kits_por_nome["Agent2"] = Kit("Melee", {"Glock 18","Tomahawk", "Cassetete", ("Comunicador", 1), "Colete médio", "Proteção de pernas média", "Proteção de braços média", ("Bebidas", 3),("9x19mm FMJ", 80)}, Pools)

kits_por_nome["ATP_Soldat2"] = Kit("ATP_Soldat_melee", {"MP9", "Wakisashi", "Karambit","Colete Medio",("9x19mm FMJ", 90), ("Comunicador", 1), ("Kit Médico Leve", 1)}, Pools)

kits_por_nome["ATP_Engineer2"] = Kit("ATP_Engineer_SMG", {"UMP-45", "USP-45", "Odachi", "Colete Medio",(".45ACP +P FMJ", 90),(".45ACP HP", 60), ("Comunicador", 1), ("Kit Médico Leve", 1)}, Pools)

Força = {
    "Luta": lambda: Proficiencia("Luta", 0),
    "Carga": lambda: Proficiencia("Carga", 0),
    "Arremesso": lambda: Proficiencia("Arremesso", 0),
    "Pericia em Cortantes": lambda: Proficiencia("Pericia em Cortantes", 0),
    "Pericia em Concussivas": lambda: Proficiencia("Pericia em Concussivas", 0)
    }

Agilidade = {
    "Acrobacia": lambda: Proficiencia("Acrobacia", 0),
    "Furtividade": lambda: Proficiencia("Furtividade", 0),
    "Reflexo": lambda: Proficiencia("Reflexo", 0),
    #"Pilotagem": lambda: Proficiencia("Pilotagem", 0),
    #"Iniciativa": lambda: Proficiencia("Iniciativa", 0),
}

Vigor = {
    "Atletismo": lambda: Proficiencia("Atletismo", 0),
    "Fortitude": lambda: Proficiencia("Fortitude", 0),
    #"Resiliencia": lambda: Proficiencia("Resiliencia", 0),
    "Vitalidade": lambda: Proficiencia("Vitalidade", 0),
    #"Folego": lambda: Proficiencia("Folego", 0),
}

Inteligencia = {
    "Investigação": lambda: Proficiencia("Investigação", 0),
    "Medicina": lambda: Proficiencia("Medicina", 0),
    #"Ciencia": lambda: Proficiencia("Ciencia", 0),
    #"Tecnologia": lambda: Proficiencia("Tecnologia", 0),
    "Sobrevivencia": lambda: Proficiencia("Sobrevivencia", 0),
}

Presença = {
    "Diplomacia": lambda: Proficiencia("Diplomacia", 0),
    "Intimidação": lambda: Proficiencia("Intimidação", 0),
    #"Intuição": lambda: Proficiencia("Intuição", 0),
    "Enganação": lambda: Proficiencia("Enganação", 0),
    "Percepção": lambda: Proficiencia("Percepção", 0),
}

Tática = {
    "Combate": lambda: Proficiencia("Combate", 0),
    "Pontaria": lambda: Proficiencia("Pontaria", 0),
    "Armamento": lambda: Proficiencia("Armamento", 0),
    "Equipamento": lambda: Proficiencia("Equipamento", 0),
    "Balistica": lambda: Proficiencia("Balistica", 0),
}

Proficiencias = {}
Proficiencias.update(Força), Proficiencias.update(Agilidade), Proficiencias.update(Vigor), Proficiencias.update(Inteligencia), Proficiencias.update(Presença), Proficiencias.update(Tática)

NPCs_predefinidos = {
    "Comum": [
        ("Civil", 1, 1, 1, 1, 1, 1),
        ("Segurança", 2, 2, 2, 2, 2, 2),
        ("Policial", 2, 3, 2, 2, 2, 2),
        ("Sheriff", 2, 3, 2, 2, 3, 3),
        ("SWAT", 3, 3, 3, 5, 4, 4)       
    ],

    "NRDN": [
        ("Cientista", 1, 1, 1, 7, 4, 1),
        ("Segurança NRDN", 3, 3, 3, 2, 3, 2),
        ("Segurança GOL.em", 6, 3, 6, 2, 3, 3),
    ],

    "Aberrações": [
        ("Zumbi", 2, 1, 4, 1, 1, 1),
        ("Crazie", 2, 3, 3, 1, 1, 1),
        ("Experiment", 3, 1, 3, 1, 1, 1),
        ("SleepWalker", 3, 2, 5, 1, 1, 2)
    ],

    "Nexus Core Agency": [
        ("Agent", 3, 3, 3, 3, 2, 3),
        ("G0L.Em", 5, 3, 6, 3, 5, 4),
        ("ATP Soldat", 3, 3, 4, 2, 4, 2),
        ("ATP Engineer", 4, 4, 4, 4, 4, 6),
        ("MAG Agent", 8, 3, 9, 2, 4, 3),
    ],

    "Militar": [
        ("Assault", 4, 3, 4, 2, 3, 4),
        ("Engenheiro", 4, 3, 3, 4, 3, 4),
        ("Médico", 1, 2, 3, 4, 5, 4),
        ("Franco Atirador", 4, 4, 4, 5, 3, 5),
        ("Comandante", 5, 5, 5, 5, 5, 5)
    ]
}

GruposDePersonagens = {
    "Players": [],
    "NPCs": []
}

Regras_de_Combate = """
Regras Integradas de Combate (In-Combat)
    O sistema de combate segue uma estrutura baseada em turnos, onde os personagens agem conforme a ordem de Iniciativa. A entrada em combate ocorre quando há a presença de hostilidade direta (geralmente envolvendo um grupo de NPCs inimigos), exigindo decisões rápidas e estratégicas dos jogadores.

Turnos e Iniciativa

    Ao iniciar um combate, todos os jogadores e NPCs envolvidos rolam Iniciativa.


    A ordem definida pela iniciativa determina a sequência de turnos no combate.


    Cada personagem realiza suas ações durante seu turno, e o ciclo continua até que o combate se encerre.

Estrutura de Turno.
    Cada turno é composto por uma Ação de Movimento, e 3 Ações, e possíveis Reações conforme o contexto:
        1. Ações
            De acordo com o limite de ações por turno, podem ser uma das seguintes:

                Ação: Ataques, arremessos, uso de objetos pesados, recarregar armas, etc.


                Ação de movimento: Navegação, locomoção ou posicionamento do personagem pelo mapa de combate.

        2. Reações
            Mudam a ordem do turno, o personagem que teve a reação troca com o atual e perde a vez na rodada.


Posicionamento e Cobertura.
    A cobertura é vital para a sobrevivência e influencia diretamente na defesa.

    Pode ser parcial ou total, e varia de +1 a +10 em bônus defensivos, tudo de acordo com a estrutura e o seu material.



Encerrando o Combate
    O combate termina quando:

        Todos os inimigos foram neutralizados ou fugiram.

        Um novo evento narrativo interrompe o combate (ex: reforços chegam, estrutura colapsa).

        Os jogadores decidem recuar ou se rendem (dependendo da situação e do mestre).

"""

Regras_de_OffCombat = """
Regras Integradas de Exploração e Off-Combat

Ações no Off-Combat:
    No off-combat, os jogadores têm liberdade para realizar várias ações sem estarem em combate direto. As ações podem envolver interação com o ambiente, exploração, conversas e interações furtivas.

        Iniciativa: Mesmo no off-combat, por questão de ordem, a iniciativa será usada para definir a sequência de ações dos jogadores, especialmente se eles estiverem explorando áreas com ameaças, tomando decisões complexas ou se deparando com outros NPCs.

        Ação Livre: Cada jogador pode realizar uma ação livre por turno, como falar com outros personagens, interagir com objetos ou simplesmente observar o ambiente. No entanto, as ações livres podem ser limitadas dependendo das circunstâncias ou do que os jogadores estão fazendo no momento.

        Ação conjunta: O jogador que estiver no seu turno pode chamar um outro jogador para realizar uma ação em conjunto, a qual pode ou não envolver um teste dependendo do contexto, caso o jogador chamado já fez o seu turno, sofrerá uma penalidade no teste feito.

        Adiar ação: O jogador pode passar o seu turno caso queira ter uma ação durante o turno de outro jogador, contanto que este jogador permita.

        Conversa: O jogador que estiver no seu turno pode chamar um outro jogador para engajar em uma conversa entre personagens, não há nenhuma penalidade para o outro jogador mesmo caso esse já tenha feito seu turno.

        Investigação ou percepção: O jogador pode realizar testes para investigar o ambiente ao seu redor (buscando pistas, armas ou outros itens úteis). Um teste de investigação(int) ou percepção(pre) pode ser necessário.

        Interação com NPCs: Os jogadores podem conversar com NPCs para obter informações, negociar ou tentar manipular situações. Testes de Persuasão, Diplomacia, Enganação ou Intimidação podem ser usados.

        Sobrevivência: Se os jogadores estiverem em um ambiente selvagem, pode ser necessário fazer testes de sobrevivência para caçar, coletar recursos, se proteger de condições extremas ou navegar pelo ambiente.

        Movimentação: Jogadores podem interagir com o ambiente para superar obstáculos (como atravessar uma área inundada, escalar um prédio ou evitar armadilhas). Isso pode envolver testes de proficiencias ou atributos variados de acordo com o contexto.


Furtividade e Exploração
    Furtividade será uma das principais mecânicas para a exploração e interações furtivas no mundo. Ela entra em jogo quando os jogadores tentam evitar serem detectados por inimigos, ou quando buscam realizar ações discretas (como eliminar um guarda ou pegar algo sem ser notado).
        Movimentação Silenciosa (Furtividade):


        Teste de Furtividade (vs. Percepção do inimigo ou NPC) sempre que o jogador tentar se mover de forma discreta.

        Modificadores como ambiente (ruído, escuridão), itens (camuflagem, disfarces), habilidades de furtividade (ex. "Furtividade"), ou distância do inimigo podem aumentar ou diminuir a dificuldade.

        Caso o jogador falhe no teste de furtividade, ele será detectado, e o inimigo ou NPC reagirá, iniciando uma interação ou um combate.

    Cobertura e Posicionamento:

        Cobertura: Utilizar objetos do ambiente para se esconder pode garantir bônus a furtividade. O jogador pode usar paredes, árvores, ou qualquer tipo de estrutura para melhorar suas chances de passar despercebido.

        Posicionamento: Jogadores podem tentar entrar em uma posição estratégica para observar o ambiente (como se esconder atrás de uma janela ou de um canto) sem serem notados. Esse posicionamento pode oferecer vantagens em termos de cobertura e furtividade.
"""

Topicos = {
    "Combate": Regras_de_Combate,
    "Off-Combat": Regras_de_OffCombat,
}
from enum import unique, Enum
import random

def NameGen() -> str:
    lovecraft = ["ngy","shu",'suc"','ubbo',"Tulz","Xa'l","yibb","rakath","rath","aathla","sothoth","magn","tho", 
                "th", "ra", "oth", "ath", "sh'", "y", "aa", "ae", "ei", "ia", "ie", "io", "ua", "ue", "ui", "uo", "ya", "ye", "yi", 
                "yo", "yu", "ay", "ey", "iy", "uy", "ou", "ow", "au", "aw", "ai", "oi", "eu", "iau", "aou", "eau", "eou", "yau", 
                "iaw", "eaw", "uaw", "oui", "iou", "aai", "eai", "iai", "uai", "oai", "uia", "yia", "uie", "iue", "yie", "yui", 
                "idhra","yog", "aiueb", "gns", "hal", "alet","heia", "azathoth", "azhorra", "tha","cloud", "thing", "cthalpa", "cxax","ukluth", "dao""loth",  "dena" "rah", "ghroth", "hydra", "ialdagorth", 
                "kaaj","hka","albh", "luth", "mhi","thrha", "mlan","doth", "and", "mril", "thor","ion", "moth", "erofpus", "nam" "eless", "mist", 
                "ngyr," "korath", "nyar","latho","tep", "nyc","telios", "nyr", "olk","oth", "shab","bithka", "shubnig","gurath", "sta", "rmother", 
                "mother", "of", "all", "sucnaath", "tru", "nembra", "tulzscha", "ubbosathla", "uvhash", "xal", "igha", 
                "xexanoth", "ycnag","nniss","sz", "yeb", "yibb", "tsith", "yogg", "yuggoth", "zoth", "o'm", "rg'yn", "gh'onn"]
    return (random.choice(lovecraft) + "'" + random.choice(lovecraft) + random.choice(lovecraft)).capitalize()

@unique
class Alignment(Enum):
    """Enum for the alignment of a god."""
    GOOD = 0
    NEUTRAL = 1
    EVIL = 2

@unique
class Personality(Enum):
    """Enum for the personality of a god."""
    TRICKSTER = 0
    HONORABLE = 1
    WISE = 2
    BUMBLING = 3

@unique
class ElementalAffinity(Enum):
    """Enum for the elemental affinity of a god."""
    WATER = 0
    EARTH = 1
    AIR = 2
    FIRE = 3

class God:
    def __init__(self, name: str):
        self.name = NameGen()
        self.alignment = Alignment(random.randint(0, len(Alignment) - 1))       
        self.personality = Personality(random.randint(0, len(Personality) - 1))
        self.elemental_affinity = ElementalAffinity(random.randint(0, len(ElementalAffinity) - 1))
    #def  Proclamation(self):
    

    

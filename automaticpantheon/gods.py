from enum import unique, Enum
from typing import List, Dict,TypedDict
from persistent import Persistent
import random

from random import randrange


def NameGen() -> str:
    lovecraft = ["ngy","shu",'suc"','ubbo',"tulz","Xa'l","yibb","rakatmeh","rath","aathla","sothoth","magn","tho", 
                "th", "ra", "oth", "ath", "sh'", "y", "aa", "ae", "ei", "ia", "ie", "io", "ua", "ue", "ui", "uo", "ya", "ye", "yi", 
                "yo", "yu", "ay", "ey", "iy", "uy", "ou", "ow", "au", "aw", "ai", "oi", "eu", "iau", "aou", "eau", "eou", "yau", 
                "iaw", "eaw", "uaw", "oui", "iou", "aai", "eai", "iai", "uai", "oai", "uia", "yia", "uie", "iue", "yie", "yui", 
                "idhra","yog", "aiueb", "gns", "hal", "alet","heia", "azathoth", "azhorra", "tha","cloud", "thing", "cthalpa", "cxax","ukluth", "dao""loth",  "dena" "rah", "ghroth", "hydra", "ialdagorth", 
                "kaaj","hka","albh", "luth", "mhi","thrha", "mlan","doth", "and", "mril", "thor","ion", "moth", "erofpus", "nam", "eless", "mist", 
                "ngyr," "korath", "nyar","latho","tep", "nyc","telios", "nyr", "olk","oth", "shab","bithka", "shubnig","gurath", "sta", "rmother", 
                "mother", "of", "all", "sucnaath", "tru", "nembra", "tulzscha", "ubbosathla", "uvhash", "xal", "igha", 
                "xexanoth", "ycnag","nniss","sz", "yeb", "yibb", "tsith", "yogg", "yuggoth", "zoth", "o'm", "rg'yn", "gh'onn"]
    
    return (random.choice(lovecraft) + random.choice(["'","","","",""]) + random.choice(lovecraft)).capitalize()

@unique
class GodType(Enum):
    CHANGE = 0
    STASIS = 1
    CIVILITY = 2
    WAR = 3

class Pantheon(Persistent):
    def __init__(self) -> None:
        self.already_used_names = set()
        self.already_used_symbols = set()
        self.gods: Dict[GodType.value,God] = {}
        for god_type in GodType:
            self.gods[god_type.value] = God(god_type,self)
        self.gods[GodType.CHANGE.value].add_rival(GodType.STASIS)
        self.gods[god_type.CIVILITY.value].add_rival(GodType.WAR)

    def get_gods(self) -> List:
        return self.gods.values()

    def get_god(self,god_type: GodType):
        return self.gods[god_type.value]

class God():
    def __init__(self,god_type:GodType,pantheon:Pantheon) -> None:
        self.type = god_type
        self.pantheon = pantheon
        self.name = NameGen()

        while self.name in self.pantheon.already_used_names:
            self.name = NameGen()
        pantheon.already_used_names.add(self.name)

        self.symbol =  chr(randrange(0x1F300, 0x1F5FF))
        while self.symbol in pantheon.already_used_symbols:
            self.symbol =  chr(randrange(0x1F300, 0x1F5FF))
        pantheon.already_used_symbols.add(self.symbol)

        self.rivals: Dict[GodType,God] = {}
        self.user_id_to_points: Dict[int,int] = {}
        for god_type in GodType:
            self.rivals[god_type] = False

    def get_type(self) -> GodType:
        return self.type

    def add_rival(self, rival_type: GodType) -> None:
        self.pantheon.get_god(rival_type).rivals[self.type] = True
        self.rivals[rival_type] = True

    def remove_rival(self, rival_type: GodType) -> None:
        self.pantheon.get_god(rival_type).rivals[self.type] = False
        self.rivals[rival_type] = False

    def get_rivals(self) -> List[GodType]:
        #return [self.pantheon.gods[rival] for rival in self.rivals if self.rivals[rival] == True]
        rival_by_type = [rival for rival in self.rivals if self.rivals[rival] == True]
        return [self.pantheon.get_god(rival) for rival in rival_by_type]
    
    
    
    
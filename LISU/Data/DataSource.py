import re
from rdflib import *

class Controller:
    def __init__(self, vid, pid):
        self.vid = vid
        self.pid = pid
        self.header = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX lisu: <https://personalpages.manchester.ac.uk/staff/mario.sandovalolive/ontology/idoo.owl#>"""

    def Controller_Attributes(self):
        graph = Graph()
        graph.parse("C:/Users/mso_2/Documents/nDoF project/Ontologies/idoo.owl")

        query_string = """ %s
        SELECT ?controller ?level ?name ?VID ?PID
        WHERE
        {
        ?controller lisu:productName ?name  .
        ?controller lisu:VID ?VID .
        ?controller lisu:PID ?PID .
        ?controller lisu:isAppropriate ?level .
        FILTER(?VID = "%s" && ?PID="%s")
        }
        GROUP BY ?controller ?level ?name ?VID ?PID""" % (self.header, self.vid, self.pid)

        _query = graph.query(query_string)
        return _query

class ControllerManager:
    def __init__(self, Controller):
        self.vid = Controller.vid
        self.pid = Controller.pid
        self.header = Controller.header

        q = Controller.Controller_Attributes()
        for row in q:
            self.productName = str(row.name)
            self.level = re.sub(r'.*#', '#', str(row.level)).replace("#","")


# Retrieve all the controllers
def List_All_Controllers():
    graph = Graph()
    graph.parse("C:/Users/mso_2/Documents/nDoF project/Ontologies/idoo.owl")

    query_string = """ PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX lisu: <https://personalpages.manchester.ac.uk/staff/mario.sandovalolive/ontology/idoo.owl#>
    
    SELECT ?controller ?name ?VID ?PID ?level ?AXES ?BTNS ?HATS
    ?leftTriggerIdx ?rightTriggerIdx
    ?leftStickLRIdx ?leftStickUDIdx
    ?rightStickLRIdx ?rightStickUDIdx
    ?leftBtn1Idx ?rightBtn1Idx
    ?leftBtn2Idx ?rightBtn2Idx
    ?hatLeftIdx ?hatRightIdx ?hatUpIdx ?hatDownIdx ?hatIdx
    ?selectBtnIdx ?startBtnIdx ?triangleBtnIdx ?squareBtnIdx ?circleBtnIdx ?crossXBtnIdx

    WHERE
    {
       ?controller lisu:productName ?name  .
       ?controller lisu:VID ?VID .
       ?controller lisu:PID ?PID .
       ?controller lisu:isAppropriate ?level .
       ?controller lisu:DOF ?AXES .
       ?controller lisu:BTNS ?BTNS .
       ?controller lisu:HATS ?HATS .
       ?controller lisu:leftTriggerIdx ?leftTriggerIdx .
       ?controller lisu:rightTriggerIdx ?rightTriggerIdx .
       ?controller lisu:leftStickLRIdx ?leftStickLRIdx .
       ?controller lisu:leftStickUDIdx ?leftStickUDIdx .
       ?controller lisu:rightStickLRIdx ?rightStickLRIdx .
       ?controller lisu:rightStickUDIdx ?rightStickUDIdx .
       ?controller lisu:leftBtn1Idx ?leftBtn1Idx .
       ?controller lisu:rightBtn1Idx ?rightBtn1Idx .
       ?controller lisu:leftBtn2Idx ?leftBtn2Idx .
       ?controller lisu:rightBtn2Idx ?rightBtn2Idx .
       ?controller lisu:hatLeftIdx ?hatLeftIdx .
       ?controller lisu:hatRightIdx ?hatRightIdx .
       ?controller lisu:hatUpIdx ?hatUpIdx .
       ?controller lisu:hatDownIdx ?hatDownIdx .
       ?controller lisu:hatIdx ?hatIdx .
       ?controller lisu:selectBtnIdx ?selectBtnIdx .
       ?controller lisu:startBtnIdx ?startBtnIdx .
       ?controller lisu:triangleBtnIdx ?triangleBtnIdx .
       ?controller lisu:squareBtnIdx ?squareBtnIdx .
       ?controller lisu:circleBtnIdx ?circleBtnIdx .
       ?controller lisu:crossXBtnIdx ?crossXBtnIdx .
    }
    GROUP BY  ?controller ?name ?VID ?PID ?level ?AXES ?BTNS ?HATS
    ?leftTriggerIdx ?rightTriggerIdx
    ?leftStickLRIdx ?leftStickUDIdx
    ?rightStickLRIdx ?rightStickUDIdx
    ?leftBtn1Idx ?rightBtn1Idx
    ?leftBtn2Idx ?rightBtn2Idx
    ?hatLeftIdx ?hatRightIdx ?hatUpIdx ?hatDownIdx ?hatIdx
    ?selectBtnIdx ?startBtnIdx ?triangleBtnIdx ?squareBtnIdx ?circleBtnIdx ?crossXBtnIdx
    """
    _query = graph.query(query_string)
    return _query

# Testing
#object1 = Controller("0x11ff","0x3331")
#object2 = ControllerManager(object1)
#try:
#    print("{}, {}, {}, {}".format(object2.vid, object2.pid, object2.productName, object2.level))
#except AttributeError:
#    print("there is an error")
#res = not object2
#print("Is dictionary empty ? : " + str(res))

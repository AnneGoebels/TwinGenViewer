from rdflib.namespace import RDF, XSD, OWL
from rdflib import Literal, Namespace, URIRef, Graph
from rdflib.plugins.stores.memory import Memory
from rdflib.graph import ConjunctiveGraph
from rdflib.plugins.sparql import prepareQuery
import ifcopenshell
# from LBD_Query import getLDofGuid


def getLD(ifcguid):

    CT = Namespace("https://standards.iso.org/iso/21597/-1/ed-1/en/Container#")
    LS = Namespace ("https://standards.iso.org/iso/21597/-1/ed-1/en/Linkset#")
    IDX = Namespace("https://asbingowl.org/TwinGenDemo/index#")
    LNK = Namespace ("https://asbingowl.org/TwinGenDemo/links#")
    ANS = Namespace("https://w3id.org/asbingowl/core#")
    SIB = Namespace ("http://example.org/sibbw7936662#")
    SCH = Namespace ("http://schema.org/")
    LBD = Namespace ("https://www.asbingowl.org/BW452#")
    PROPS = Namespace("http://lbd.arch.rwth-aachen.de/props#")
    BOT = Namespace ("https://w3id.org/bot#")


    store = Memory()
    g = ConjunctiveGraph(store = store)


    g.bind("owl", OWL)
    g.bind("ct",CT)
    g.bind("index",IDX)
    g.bind("ls", LS)
    g.bind("asb", ANS)
    g.bind("sib",SIB)
    g.bind("link", LNK)
    g.bind("schema", SCH)
    g.bind("inst", LBD)
    g.bind("props", PROPS)
    g.bind("bot", BOT)

    idSib = URIRef("http://example.org/sibbw7936662")
    sib = Graph(store=store, identifier=idSib)
    sib.parse(r"ICCD_TwinGenDemo\Payload documents\SIBBauwerke RDF Data\SIB7936662_A99-BW_2021-12-16.ttl", format = "ttl")

    idOnt = URIRef("https://w3id.org/asbingowl/core")
    ont = Graph(store=store, identifier=idOnt)
    ont.parse(r"ASB_Ontology_Core.ttl", format = "ttl")

    idCt = URIRef("https://standards.iso.org/iso/21597/-1/ed-1/en/Container")
    ct = Graph(store=store, identifier=idCt)
    ct.parse(r"ICCD_TwinGenDemo\Ontology resources\Container.rdf", format = "xml")

    idIdx = URIRef("https://asbingowl.org/TwinGenDemo/index")
    index = Graph(store=store, identifier=idIdx)
    index.parse(r"ICCD_TwinGenDemo\index.ttl", format="ttl")

    idLs = URIRef("https://standards.iso.org/iso/21597/-1/ed-1/en/Linkset")
    ls = Graph(store=store, identifier =idLs)
    ls.parse(r"ICCD_TwinGenDemo\Ontology resources\Linkset.rdf", format = "xml")

    idLnk = URIRef("https://asbingowl.org/TwinGenDemo/links")
    links = Graph(store=store, identifier=idLnk)
    links.parse(r"ICCD_TwinGenDemo\Payload triples\links.ttl",format="ttl")

    idLbd = URIRef("https://www.asbingowl.org/BW452#")
    lbd = Graph(store=store, identifier=idLbd)
    lbd.parse(r"ICCD_TwinGenDemo\Payload documents\BW45-2_LBD.ttl",format="ttl")


    ifcGuidQuery = prepareQuery("""
                                select ?asbDamage ?jahr ?asbText ?damagetype ?size ?filename
                                where {
                                    ?botEle props:globalIdIfcRoot [ schema:value ?guid ].
                                    ?bauteildef a asb:ASBING13_BauteilDefinition;
                                                owl:sameAs ?botEle.
                                    ?schadObj asb:hatBauteilDefinition ?bauteildef;
                                              asb:hatPruefDokumentation ?asbDamage.
                                    ?asbDamage  asb:PruefungUeberwachung_Pruefjahr ?jahr;
                                                asb:ASBObjekt_Textfeld ?asbText;
                                                asb:Schaden_Schaden    ?damagetype;
                                                asb:Schaden_AllgemeineMengenangabe ?size.
                                    ?ident ls:uri ?asbDamage.
                                    ?LinkEle1 ls:hasIdentifier ?ident.
                                    ?Link ls:hasLinkElement ?LinkEle1, ?LinkEle2 .
                                    ?LinkEle2 ls:hasDocument ?pic.
                                    ?pic ct:filename ?filename.
                                    FILTER EXISTS {?asbDamage asb:Schaden_Foto ?fotostr.}
                                    FILTER (?LinkEle2 != ?LinkEle1)
                                }
                                """,initNs= {"props": PROPS, "schema": SCH, "asb": ANS, "owl": OWL, "ls": LS, "ct": CT})

    for row in g.query(ifcGuidQuery, initBindings={'guid': Literal(ifcguid)}):
        return row


#model = ifcopenshell.open(r"C:\Users\Anne\sciebo\2020_twingen_intern\TwinGenViewer\BW45-2.ifc")
#proxys = list(model.by_type("IfcBuildingelementProxy"))
#for p in proxys:
#    guid = p.GlobalId
 #   res = getLD(guid)
 ##  print(res)




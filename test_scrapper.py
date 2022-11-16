from scrapper import *


def test_getTitle():
    web = "https://www.youtube.com/watch?v=fmsoym8I-3o"
    soup, driver = get_page(web)
    assert getTitle(soup) == 'Pierre Niney : L’interview face cachée par HugoDécrypte'

def test_getName():
    web = "https://www.youtube.com/watch?v=fmsoym8I-3o"
    soup, driver = get_page(web)
    assert getName(soup) == "HugoDécrypte"


''' c'est inutile de tester le nombre de like puisqu'il change tout le temps
def test_getLikes():
    web = "https://www.youtube.com/watch?v=fmsoym8I-3o"
    soup, driver = get_page(web)
    assert getLikes(soup) == "30,528 "
'''

def test_getDescription(): 
    web = "https://www.youtube.com/watch?v=fmsoym8I-3o"
    soup, driver = get_page(web)
    assert getDescription(soup,driver).text == "🍿 L'acteur Pierre Niney est dans L’interview face cachée ! Ces prochains mois, le format revient plus fort avec des artistes, sportifs, etc.\n🔔 Abonnez-vous pour ne manquer aucune vidéo.\n\nInterview réalisée à l’occasion de la sortie du film « Mascarade » réalisé par Nicolas Bedos, le 1er novembre 2022 au cinéma. Avec Pierre Niney, Isabelle Adjani, François Cluzet, Marine Vacth.\n\nChaleureux remerciements au cinéma mk2 Bibliothèque pour son accueil.\n\n—\n\n00:00 Intro\n00:22 1\n03:32 2\n10:11 3\n14:09 4\n17:28 5\n20:10 6\n23:13 7\n39:22 8\n\n—\n\nPrésenté par Hugo Travers\n\nRéalisateur : Julien Potié\nJournalistes : Benjamin Aleberteau, Blanche Vathonne\n\nChargée de production déléguée : Romane Meissonnier\nAssistant de production déléguée : Clément Chaulet\nChargée de production exécutive : Marie Delvallée\n\nChef OPV : Lucas Stoll\nOPV : Pierre Amilhat, Vanon Borget\nElectricien : Alex Henry\nChef OPS : Victor Arnaud\nStagiaire image : Magali Faizeau\n\nMaquilleuse : Kim Desnoyers\nPhotographe plateau : Erwann Tanguy\n\nMonteur-étalonneur : Stan Duplan\nMixeuse : Romane Meissonnier\n\nCheffe de projets partenariats : Mathilde Rousseau\nAssistante cheffe de projets partenariats : Manon Montoriol\n\n—\n\n© HugoDécrypte / 2022"

def test_getLinks():
    web = "https://www.youtube.com/watch?v=fmsoym8I-3o"
    soup, driver = get_page(web)
    description = getDescription(soup,driver)
    assert getLinks(description) == [
                "https://www.youtube.com/watch?v=fmsoym8I-3o&t=0s",
                "https://www.youtube.com/watch?v=fmsoym8I-3o&t=22s",
                "https://www.youtube.com/watch?v=fmsoym8I-3o&t=212s",
                "https://www.youtube.com/watch?v=fmsoym8I-3o&t=611s",
                "https://www.youtube.com/watch?v=fmsoym8I-3o&t=849s",
                "https://www.youtube.com/watch?v=fmsoym8I-3o&t=1048s",
                "https://www.youtube.com/watch?v=fmsoym8I-3o&t=1210s",
                "https://www.youtube.com/watch?v=fmsoym8I-3o&t=1393s",
                "https://www.youtube.com/watch?v=fmsoym8I-3o&t=2362s"
            ]

def test_getId():
    web = "https://www.youtube.com/watch?v=fmsoym8I-3o"
    soup, driver = get_page(web)
    assert getId(web) == "fmsoym8I-3o"

def test_getComments():
    web = "https://www.youtube.com/watch?v=fmsoym8I-3o"
    soup, driver = get_page(web)
    assert getComments(soup, driver) == [
                "Pensez à vous abonner pour ne pas louper les vidéos suivantes et me soutenir. ",
                "Hugo Décrypte + Pierre Niney = forcément une super interview ! Merci à vous deux ",
                "C’est très plaisant et plutôt rare de trouver des journalistes aussi intéressés et impliqués, il n’y avait que de bonnes questions! Cette interview est de qualité, avec un invité de qualité! Merci beaucoup pour le travail derrière de l’équipe, merci pour ce partage! (Et hâte de te voir faire l’arbre )",
                "Oh la la !! Le \"mauvais doublage\" fait par Pierre, on en veut encoooore ! C'était hilarant !",
                "Pierre Niney est clairement le meilleur acteur de sa génération."
            ]



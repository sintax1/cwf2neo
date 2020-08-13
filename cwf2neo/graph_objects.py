from py2neo.ogm import GraphObject, Property, Related


class NISTFunction(GraphObject):
    """Neo4j Graph Object (node) representing a NIST Function
    """
    __primarykey__ = "id"

    id = Property()
    title = Property()


class NISTCategory(GraphObject):
    """Neo4j Graph Object (node) representing a NIST Category
    """
    __primarykey__ = "id"

    id = Property()
    title = Property()
    description = Property()

    nist_function = Related(NISTFunction)


class NISTSubCategory(GraphObject):
    """Neo4j Graph Object (node) representing a NIST Sub-Category
    """
    __primarykey__ = "id"

    id = Property()
    description = Property()
    nist_category = Related(NISTCategory)


class NISTReference(GraphObject):
    """Neo4j Graph Object (node) representing a NIST Reference
    """
    __primarykey__ = "reference"

    reference = Property()
    nist_subcategory = Related(NISTSubCategory)


class NICECategory(GraphObject):
    """Neo4j Graph Object (node) representing a NICE Category
    """
    __primarykey__ = "id"

    id = Property()
    title = Property()
    description = Property()

    nist_function = Related(NISTFunction)


class NICESpecialtyArea(GraphObject):
    """Neo4j Graph Object (node) representing a Specialty Area
    """
    __primarykey__ = "id"

    id = Property()
    title = Property()
    description = Property()

    nice_category = Related(NICECategory)


class NICEWorkrole(GraphObject):
    """Neo4j Graph Object (node) representing a NICE Workrole
    """
    __primarykey__ = "id"

    id = Property()
    title = Property()
    description = Property()
    opm_code = Property()

    nice_specialty_area = Related(NICESpecialtyArea)


class NICECompetencyGroup(GraphObject):
    """Neo4j Graph Object (node) representing a NICE Competency Group
    """
    #__primarykey__ = "id"

    # Competency Group ID removed in 30 June 2020 update
    # id = Property()
    name = Property()


class NICECompetency(GraphObject):
    """Neo4j Graph Object (node) representing a NICE Competency
    """
    __primarykey__ = "id"

    id = Property()
    name = Property()
    description = Property()

    nice_competency_group = Related(NICECompetencyGroup)


class KSAT(GraphObject):
    """Neo4j Graph Object (node) representing a NICE KSAT
    """
    __primarykey__ = "id"

    id = Property()
    type = Property()
    description = Property()

    nice_workrole = Related(NICEWorkrole)
    nice_competency = Related(NICECompetency)

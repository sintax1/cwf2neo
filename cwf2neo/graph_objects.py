from py2neo.ogm import GraphObject, Property, Related, RelatedFrom, RelatedTo


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

    function = RelatedFrom(NISTFunction, "CATEGORY")


class NISTSubCategory(GraphObject):
    """Neo4j Graph Object (node) representing a NIST Sub-Category
    """
    __primarykey__ = "id"

    id = Property()
    description = Property()
    category = RelatedFrom(NISTCategory, "SUBCATEGORY")


class NISTReference(GraphObject):
    """Neo4j Graph Object (node) representing a NIST Reference
    """
    __primarykey__ = "reference"

    reference = Property()
    subcategory = RelatedFrom(NISTSubCategory, "REFERENCE")


class KSAT(GraphObject):
    """Neo4j Graph Object (node) representing a NICE KSAT
    """
    __primarykey__ = "id"

    id = Property()
    type = Property()
    description = Property()

    nice_workrole = RelatedTo("NICEWorkrole", "WORKROLE")
    nice_competency = Related("NICECompetency", "COMPETENCY")


class NICECategory(GraphObject):
    """Neo4j Graph Object (node) representing a NICE Category
    """
    __primarykey__ = "id"

    id = Property()
    title = Property()
    description = Property()

    nist_function = RelatedTo(NISTFunction)


class NICESpecialtyArea(GraphObject):
    """Neo4j Graph Object (node) representing a Specialty Area
    """
    __primarykey__ = "id"

    id = Property()
    title = Property()
    description = Property()

    category = RelatedFrom("NICECategory", "SPECIALTY_AREA")


class NICEWorkrole(GraphObject):
    """Neo4j Graph Object (node) representing a NICE Workrole
    """
    __primarykey__ = "id"

    id = Property()
    title = Property()
    description = Property()
    opm_code = Property()

    specialty_area = RelatedFrom("NICESpecialtyArea", "WORKROLE")


class NICECompetencyGroup(GraphObject):
    """Neo4j Graph Object (node) representing a NICE Competency Group
    """
    __primarykey__ = "id"

    id = Property()
    name = Property()


class NICECompetency(GraphObject):
    """Neo4j Graph Object (node) representing a NICE Competency
    """
    __primarykey__ = "id"

    id = Property()
    name = Property()
    description = Property()

    competency_group = Related(NICECompetencyGroup)

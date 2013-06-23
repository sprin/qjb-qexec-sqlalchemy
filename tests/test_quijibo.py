from sqlalchemy import (
    Integer,
    select,
    String,
)
from sqlalchemy.sql import (
    table,
    column,
)
from sqlalchemy.sql.expression import (
    and_,
    or_,
    not_,
    asc,
    desc,
)

from quijibo import (
    construct_clauses,
    construct_query,
)

# Create a textual table clause that will suffice for constructing queries.
# See Alchemy docs: http://is.gd/vIHsXB
proj = table('project',
    column('project_name', String),
    column('project_year', Integer),
)

def clause_eq(raw_clause, expected_clause):
    clause = construct_clauses(proj, raw_clause)
    print expected_clause
    print clause
    print type(clause)
    assert str(clause) == str(expected_clause)

def query_eq(query_tree, expected_query):
    query = construct_query(proj, query_tree)
    print expected_query
    print query
    assert str(query) == str(expected_query)

def test_eq_clause():
    raw_clause = {
        'col': 'project_name',
        'op': 'eq',
        'other': 'quijibo',
    }
    expected_clause = proj.c.project_name == 'quijibo'
    clause_eq(raw_clause, expected_clause)

def test_is_null_clause():
    raw_clause = {
        'col': 'project_name',
        'op': 'eq',
        'other': None,
    }
    expected_clause = proj.c.project_name == None
    clause_eq(raw_clause, expected_clause)

def test_ne_clause():
    raw_clause = {
        'col': 'project_name',
        'op': 'ne',
        'other': 'quijibo',
    }
    expected_clause = proj.c.project_name != 'quijibo'
    clause_eq(raw_clause, expected_clause)

def test_not_null_clause():
    raw_clause = {
        'col': 'project_name',
        'op': 'ne',
        'other': None,
    }
    expected_clause = proj.c.project_name != None
    clause_eq(raw_clause, expected_clause)

def test_lt_clause():
    raw_clause = {
        'col': 'project_year',
        'op': 'lt',
        'other': 2012,
    }
    expected_clause = proj.c.project_year < 2012
    clause_eq(raw_clause, expected_clause)


def test_lte_clause():
    raw_clause = {
        'col': 'project_year',
        'op': 'lte',
        'other': 2012,
    }
    expected_clause = proj.c.project_year <= 2012
    clause_eq(raw_clause, expected_clause)

def test_gt_clause():
    raw_clause = {
        'col': 'project_year',
        'op': 'gt',
        'other': 2012,
    }
    expected_clause = proj.c.project_year > 2012
    clause_eq(raw_clause, expected_clause)

def test_gte_clause():
    raw_clause = {
        'col': 'project_year',
        'op': 'gte',
        'other': 2012,
    }
    expected_clause = proj.c.project_year >= 2012
    clause_eq(raw_clause, expected_clause)

def test_match_clause():
    raw_clause = {
        'col': 'project_name',
        'op': 'match',
        'other': 'quijibo',
    }
    expected_clause = proj.c.project_name.op('~')('quijibo')
    clause_eq(raw_clause, expected_clause)

def test_imatch_clause():
    raw_clause = {
        'col': 'project_name',
        'op': 'imatch',
        'other': 'quijibo',
    }
    expected_clause = proj.c.project_name.op('~*')('quijibo')
    clause_eq(raw_clause, expected_clause)

def test_and_clause():
    raw_clause = {
        'op': 'and',
        'clauses': [
            {
                'col': 'project_name',
                'op': 'eq',
                'other': 'quijibo',
            },
            {
                'col': 'project_year',
                'op': 'eq',
                'other': 2001,
            },
        ]
    }
    expected_clause = and_(
        proj.c.project_name == 'quijibo',
        proj.c.project_year == 2001)

    clause_eq(raw_clause, expected_clause)

def test_or_clause():
    raw_clause = {
        'op': 'or',
        'clauses': [
            {
                'col': 'project_name',
                'op': 'eq',
                'other': 'quijibo',
            },
            {
                'col': 'project_year',
                'op': 'eq',
                'other': 2001,
            },
            {
                'col': 'project_year',
                'op': 'eq',
                'other': 2002,
            },
        ]
    }
    expected_clause = or_(
        proj.c.project_name == 'quijibo',
        proj.c.project_year == 2001,
        proj.c.project_year == 2002)

    clause_eq(raw_clause, expected_clause)


def test_not_clause():
    raw_clause = {
        'op': 'not',
        'clause': {
                'col': 'project_name',
                'op': 'eq',
                'other': 'quijibo',
        },
    }
    expected_clause = not_(proj.c.project_name == 'quijibo')
    clause_eq(raw_clause, expected_clause)

def test_query_struct():
    query_tree = {
        'select': ['project_name', 'project_year'],
    }
    expected_query = select([
        proj.c.project_name,
        proj.c.project_year,
    ])
    query_eq(query_tree, expected_query)


def test_query_struct_where():
    query_tree = {
        'select': ['project_name', 'project_year'],
        'where': {
            'col': 'project_name',
            'op': 'eq',
            'other': 'quijibo',
        },
    }
    expected_query = select([
        proj.c.project_name,
        proj.c.project_year,
    ]).where(proj.c.project_name == 'quijibo')
    query_eq(query_tree, expected_query)

def test_query_struct_asc():
    query_tree = {
        'select': ['project_name', 'project_year'],
        'order_by': [
            {
                'type': 'asc',
                'col': 'project_name',
            }
        ]
    }
    expected_query = select([
        proj.c.project_name,
        proj.c.project_year,
    ]).order_by(asc(proj.c.project_name))
    query_eq(query_tree, expected_query)

def test_query_struct_desc():
    query_tree = {
        'select': ['project_name', 'project_year'],
        'order_by': [
            {
                'type': 'desc',
                'col': 'project_name',
            }
        ]
    }
    expected_query = select([
        proj.c.project_name,
        proj.c.project_year,
    ]).order_by(desc(proj.c.project_name))
    query_eq(query_tree, expected_query)

def test_query_struct_asc_desc():
    query_tree = {
        'select': ['project_name', 'project_year'],
        'order_by': [
            {
                'type': 'desc',
                'col': 'project_name',
            },
            {
                'type': 'asc',
                'col': 'project_year',
            }
        ]
    }
    expected_query = (
        select([
            proj.c.project_name,
            proj.c.project_year,
        ])
        .order_by(desc(proj.c.project_name))
        .order_by(asc(proj.c.project_year))
    )
    query_eq(query_tree, expected_query)

def test_query_struct_limit():
    query_tree = {
        'select': ['project_name', 'project_year'],
        'limit': 5,
    }
    expected_query = select([
        proj.c.project_name,
        proj.c.project_year,
    ]).limit(5)
    query_eq(query_tree, expected_query)

def test_kitchen_sink_query():
    query_tree = {
        'select': ['project_name', 'project_year'],
        'where': {
            'op': 'and',
            'clauses': [
                {
                    'col': 'project_name',
                    'op': 'eq',
                    'other': 'quijibo',
                },
                {
                    'op': 'or',
                    'clauses': [
                        {
                            'col': 'project_year',
                            'op': 'eq',
                            'other': 2001,
                        },
                        {
                            'col': 'project_year',
                            'op': 'eq',
                            'other': 2002,
                        },
                        {
                            'op': 'and',
                            'clauses': [
                                {
                                    'col': 'project_year',
                                    'op': 'gte',
                                    'other': 2010,
                                },
                                {
                                    'col': 'project_year',
                                    'op': 'lte',
                                    'other': 2013,
                                },
                            ],
                        },

                    ],
                },
            ],
        },
        'order_by': [
            {
                'type': 'desc',
                'col': 'project_name',
            },
            {
                'type': 'asc',
                'col': 'project_year',
            }
        ],
        'limit': 5,
    }
    expected_query = (
        select([
            proj.c.project_name,
            proj.c.project_year,
        ])
        .where(and_(
            proj.c.project_name == 'quijibo',
            or_(
                proj.c.project_year == 2001,
                proj.c.project_year == 2002,
                and_(
                    proj.c.project_year >= 2010,
                    proj.c.project_year <= 2013,
                ),
            )
        ))
        .order_by(desc(proj.c.project_name))
        .order_by(asc(proj.c.project_year))
        .limit(5)
    )
    query_eq(query_tree, expected_query)


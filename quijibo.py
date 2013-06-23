"""
Quijibo
A subset of SQL represented as JSON objects.
"""

from sqlalchemy import select
from sqlalchemy.sql.expression import (
    and_,
    or_,
    not_,
    asc,
    desc,
)

def col_list(table, col_names):
    if not col_names:
        return []
    return [c for cname in col_names
            for c in table.columns
            if c.name == cname]

def get_col(table, col_name):
    try:
        return col_list(table, (col_name,))[0]
    except IndexError:
        raise ValueError('no such column {}', col_name)

def construct_query(table, query_tree):

    select_list = query_tree.get('select')

    q = select(col_list(table, select_list))

    distinct = query_tree.get('distinct')

    if distinct:
        q = q.distinct()

    raw_where = query_tree.get('where')

    if raw_where:
        q = q.where(construct_clauses(table, raw_where))

    order_by = query_tree.get('order_by')

    if order_by:
        for order_col in order_by:
            col_name = order_col['col']
            type = order_col['type']
            col = get_col(table, col_name)

            if type == 'asc' or type == None:
                q = q.order_by(asc(col))
            elif type == 'desc':
                q = q.order_by(desc(col))

    limit = query_tree.get('limit')
    if limit:
        q = q.limit(limit)

    return q


def construct_clauses(table, clause):
    if not clause:
        return True

    op = clause['op']
    # Get sub-clause list, if any.
    sub_clauses = clause.get('clauses', [])

    if sub_clauses:
        # Handle operations that construct a ClauseList
        if op == 'and':
            return and_(*[construct_clauses(table, c) for c in sub_clauses])
        elif op == 'or':
            return or_(*[construct_clauses(table, c) for c in sub_clauses])
        else:
            return ValueError('invalid operation on clause list: {}', op)

    else:
        # Handle operations that construct a single Clause
        col_name = clause.get('col')
        op = clause.get('op')
        other = clause.get('other')
        if op == 'not':
            # not must have a singular clause to act on.
            not_clause = clause.get('clause')
            return not_(construct_clauses(table, not_clause))

        col = get_col(table, col_name)

        if op == 'eq':
            return col == other
        if op == 'ne':
            return col != other
        if op == 'lt':
            return col < other
        if op == 'lte':
            return col <= other
        if op == 'gt':
            return col > other
        if op == 'gte':
            return col >= other
        if op == 'in':
            return col.in_(other)
        if op == 'match':
            return col.op("~")(other)
        if op == 'imatch':
            return col.op("~*")(other)
        else:
            return ValueError('invalid clause operation: {}', op)


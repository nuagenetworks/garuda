# -*- coding:utf-8 -*-

from garuda.core.lib import GAPredicateConverter

from pypred.ast import LogicalOperator, CompareOperator, Literal, Number, Constant, Empty, Undefined

class GAMongoPredicateConverter(GAPredicateConverter):
    """
    """

    def __init__(self):
        super(GAMongoPredicateConverter, self).__init__()

        self._operators = {
            'and': '$and',
            'or': '$or',
            'is': '$eq',
            '=': '$eq',
            '<': '$lt',
            '<=': '$lte',
            '>': '$gt',
            '>=': '$gte',
            '!=': '$ne',
            'is not': '$ne'
        }

        self._keywords = {
            'ID': '_id'
        }

    def convert_tree(self, ast):
        """
        """
        ast_type = type(ast)

        if ast_type == Undefined:
            return 'null'

        if ast_type == Constant:
            if ast.value is None:
                return 'null'

            return ast.value

        if ast_type == Empty:
            return ''

        if ast_type == Number:
            return ast.value

        if ast_type == Literal:

            if ast.value in self._keywords:
                return self._keywords[ast.value]

            return ast.value.strip("'\"")

        if ast_type == CompareOperator:
            return {self.convert_tree(ast.left): {self._operators[ast.type]: self.convert_tree(ast.right)}}

        if ast_type == LogicalOperator:
            return {self._operators[ast.type]: [self.convert_tree(ast.left), self.convert_tree(ast.right)]}

        raise SyntaxError("%s not supported yet" % ast_type)  # pragma: no cover

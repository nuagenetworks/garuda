# -*- coding:utf-8 -*-

from pypred import parser as pypred_parser
from pypred.ast import Literal


class GAPredicateConverter(object):
    """
    """

    def convert(self, source):
        """
        """
        ast = None
        lexer = pypred_parser.get_lexer()
        parser = pypred_parser.get_parser()

        try:
            ast = parser.parse(source, lexer)
        except AttributeError:
            raise SyntaxError('Could not convert predicate %s' % source)

        if parser.errors or lexer.errors:
            raise SyntaxError('Could not convert due to the following errors %s' % (parser.errors + lexer.errors))

        if type(ast) == Literal:
            raise SyntaxError('Invalid predicate %s' % source)

        return self.convert_tree(ast)  # pragma: no cover

    def convert_tree(self, ast):
        """
        """
        raise NotImplementedError('convert_tree must be implemented.')

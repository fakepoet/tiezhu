#!/usr/bin/env python
# coding=utf-8
from markdown.parser.base import BlockElementParser
from markdown.parser.util import ParseUtil
from markdown.parser.leaves.paragraph_element import ParagraphElement
from markdown.parser.leaves.setext_heading_element import SetextHeadingElement
from markdown.parser.leaves.empty_line_element import EmptyLineElement


class ParagraphParser(BlockElementParser):
    """
    The paragraph parser.

    A sequence of non-blank lines that cannot be interpreted as other
    kinds of blocks forms a paragraph. The contents of the paragraph are
    the result of parsing the paragraph’s raw content as inlines. The
    paragraph’s raw content is formed by concatenating the lines and
    removing initial and final whitespace.
    """

    def __init__(self, config):
        super(ParagraphParser, self).__init__(config)

    def parse(self, code, index, auxiliary=None):
        elem = self.get_unclosed(auxiliary)
        start = index
        if elem is None:
            success, index = self.check_indent(code, index)
            if not success:
                return None
        while index < len(code) and code[index] != '\n':
            index += 1
        last = code[start:index]
        line = last.lstrip()
        index += 1
        if line == '':
            if elem is None:
                # Consumes the empty line.
                return EmptyLineElement()
            else:
                # The paragraph is closed by an empty line.
                elem.close()
                return elem
        if elem is None:
            elem = ParagraphElement()
        elem.append(line)
        if len(elem.get_lines()) >= 2:
            if ParseUtil.get_heading_space_num(last) < 4:
                line = line.rstrip()
                # Empty lines could not exist in paragraph.
                if line[0] in ['=', '-'] and all(c == line[0] for c in line):
                    elem.del_last_line()
                    elem.close()
                    heading_elem = SetextHeadingElement()
                    heading_elem.set_lines(elem.get_lines())
                    if line[0] == '=':
                        heading_elem.set_level(1)
                    else:
                        heading_elem.set_level(2)
                    return heading_elem
        return elem

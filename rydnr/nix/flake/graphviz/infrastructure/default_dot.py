"""
rydnr/nix/flake/graphviz/infrastructure/default_dot.py

This file defines DefaultDot class.

Copyright (C) 2023-today rydnr's nix-flake-to-graphviz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from rydnr.nix.flake.graphviz import Dot
from typing import Dict


class DefaultDot(Dot):
    """
    Creates a dot file representing the dependencies of a given Nix flake.

    Class name: DefaultDot

    Responsibilities:
        - Generate valid dot files from Nix flake's inputs.

    Collaborators:
        - None
    """

    _singleton = None

    def __init__(self):
        """
        Creates a new DefaultDot instance.
        """
        super().__init__()

    def _build_label(self, node, content: Dict) -> str:
        """
        Builds a label for given node.
        :param node: The node.
        :type node: Any
        :param content: The node content.
        :type content: Dict
        :return: The label.
        :rtype: str
        """
        return node

    @classmethod
    def enabled(cls) -> bool:
        """
        Checks if the class is enabled or not.
        :return: True in such case.
        :rtype: bool
        """
        return True

    @classmethod
    def priority(cls) -> int:
        """
        Retrieves the priority of the implementation.
        :return: The priority value. The lower, the more priorized.
        :rtype: int
        """
        return 99

    @classmethod
    def instance(cls):
        """
        Retrieves a new DefaultDot instance.
        :return: A new instance.
        :rtype: rydnr.nix.flake.graphviz.infrastructure.DefaultDot
        """
        return DefaultDot()

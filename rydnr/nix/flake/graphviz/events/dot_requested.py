"""
rydnr/nix/flake/graphviz/events/dot_requested.py

This file defines DotRequested class.

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
from pythoneda import Event


class DotRequested(Event):
    """
    A dot file representing a Nix flake dependency graph is requested.

    Class name: DotRequested

    Responsibilities:
        - Represent the moment in which a dot has been requested.

    Collaborators:
        - None
    """

    def __init__(self, flakeFolder: str, outputFile: str):
        """
        Creates a new DotRequested instance.
        :param flakeFolder: The flake folder.
        :type flakeFolder: str
        :param outputFile: The output file.
        :type outputFile: str
        """
        super().__init__()
        self._flake_folder = flakeFolder
        self._output_file = outputFile

    @property
    def flake_folder(self) -> str:
        """
        Retrieves the flake folder.
        :return: Such folder.
        :rtype: str
        """
        return self._flake_folder

    @property
    def output_file(self) -> str:
        """
        Retrieves the output file.
        :return: Such file.
        :rtype: str
        """
        return self._output_file

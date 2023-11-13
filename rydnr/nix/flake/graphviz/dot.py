"""
rydnr/nix/flake/graphviz/dot.py

This file defines Dot class.

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
from pythoneda import EventListener, listen, primary_key_attribute
from pythoneda.shared.nix_flake import NixFlakeMetadata
from rydnr.nix.flake.graphviz.events import DotRequested
from typing import Dict


class Dot(EventListener):
    """
    Creates a dot file representing the dependencies of a given Nix flake.

    Class name: Dot

    Responsibilities:
        - Generate valid dot files from Nix flake's inputs.

    Collaborators:
        - None
    """

    def __init__(self, flakeFolder: str, outputFile: str):
        """
        Creates a new Dot instance.
        :param flakeFolder: The flake folder.
        :type flakeFolder: str
        :param outputFile: The output file.
        :type outputFile: str
        """
        super().__init__()
        self._flake_folder = flakeFolder
        self._output_file = outputFile

    @property
    @primary_key_attribute
    def flake_folder(self) -> str:
        """
        Retrieves the flake folder.
        :return: Such folder.
        :rtype: str
        """
        return self._flake_folder

    @property
    @primary_key_attribute
    def output_file(self) -> str:
        """
        Retrieves the output file.
        :return: Such path.
        :rtype: str
        """
        return self._output_file

    def dot(self) -> str:
        """
        Retrieves a dot representation of the flake metadata.
        :return: Such content.
        :rtype: str
        """
        return self._convert_to_dot_format(
            NixFlakeMetadata.from_folder(self.flake_folder).metadata
        )

    def _convert_to_dot_format(self, metadata: Dict) -> str:
        """
        Converts given flake metadata to dot format.
        :param metadata: The Nix flake metadata.
        :type metadata: str
        :return: A dot-formatted representation of the Nix flake dependiencies.
        :rtype: str
        """
        title = metadata["locked"]["url"]
        result = f'digraph "{title}" {{\n'
        result += f'  rankdir=TD;\n  compound=true;\n  label="{title}";\n\n'
        result += '  root [label="inputs", shape="circle", fillcolor="black", fixedsize="false"];\n'

        deps = metadata.get("locks", {}).get("nodes", {})
        items = deps.items()
        transitive_nodes = []
        # Adding transitive nodes
        result += '  node [shape="ellipse", style="filled", fillcolor="green"];\n\n'
        for node, details in deps.get("root", {}).get("inputs", {}).items():
            nodeName = self.__class__.kebab_to_camel(node)
            transitive_nodes.append(node)
            result += f'  {nodeName} [label="{node}"];\n'
        # Adding non-transitive nodes
        result += '  node [shape="ellipse", style="filled", fillcolor="grey"];\n\n'
        for node, details in items:
            if node not in transitive_nodes:
                nodeName = self.__class__.kebab_to_camel(node)
                if "locked" in details:
                    result += f'  {nodeName} [label="{node}"];\n'

        result += "\n  // dependency graph\n"
        # Adding edges
        for node, details in items:
            nodeName = self.__class__.kebab_to_camel(node)
            for dep, ref in details.get("inputs", {}).items():
                if isinstance(ref, list):
                    depName = self.__class__.kebab_to_camel(dep)
                else:
                    depName = self.__class__.kebab_to_camel(ref)
                result += f"  {nodeName} -> {depName};\n"

        result += "}\n"
        return result

    def generate_output(self):
        """
        Generates the output file.
        """
        with open(self.output_file, "w") as file:
            file.write(self.dot())

        self.__class__.logger().info(f"{self.output_file} file created successfully")

    @classmethod
    @listen(DotRequested)
    async def listen(cls, event: DotRequested):
        """
        Receives a DotRequested event and generates a dot file.
        :param event: The event.
        :type event: rydnr.nix.flake.graphviz.events.DotRequested
        """
        dot = Dot(event.flake_folder, event.output_file)
        dot.generate_output()

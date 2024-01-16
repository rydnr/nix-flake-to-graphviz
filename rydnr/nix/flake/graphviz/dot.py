# vim: set fileencoding=utf-8
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
from .nix_flake_metadata_decorator import NixFlakeMetadataDecorator
import os
from pythoneda.shared import EventListener, listen, primary_key_attribute
from pythoneda.shared.nix_flake import NixFlakeMetadata
from rydnr.nix.flake.graphviz.events import DotRequested
from stringtemplate3 import StringTemplateGroup
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

    def __init__(self):
        """
        Creates a new Dot instance.
        """
        super().__init__()

    def dot(self, flakeRef: str) -> str:
        """
        Retrieves a dot representation of the flake metadata.
        :param flakeRef: The flake reference (either a folder or an url).
        :type flakeRef: str
        :return: Such content.
        :rtype: str
        """
        nix_flake_metadata = NixFlakeMetadata.from_ref(flakeRef)
        return self._convert_to_dot_format(nix_flake_metadata)

    def _build_label(self, node: str, version: str = None) -> str:
        """
        Builds a label for given node.
        :param node: The node name.
        :type node: str
        :param version: The version.
        :type version: Dict
        :return: The label.
        :rtype: str
        """
        if version is None:
            result = node
        else:
            result = f"{node}\n{version}"
        return result

    def _get_version(self, node, content: Dict) -> str:
        """
        Retrieves the node version.
        :param node: The node.
        :type node: Any
        :param content: The node content.
        :type content: Dict
        :return: The version.
        :rtype: str
        """
        return None

    def _get_template_path(self, fileName: str) -> str:
        """
        Retrieves the path of the template matching given name.
        :param fileName: The name of the file of the template.
        :type fileName: str
        :return: The path of the template.
        :rtype: str
        """
        return os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                )
            ),
            "templates",
            fileName,
        )

    def _convert_to_dot_format(self, metadata: NixFlakeMetadata) -> str:
        """
        Converts given flake metadata to dot format.
        :param metadata: The Nix flake metadata.
        :type metadata: pythoneda.shared.nix_flake.NixFlakeMetadata
        :return: A dot-formatted representation of the Nix flake dependiencies.
        :rtype: str
        """
        with open(self._get_template_path("dot.stg"), "r", encoding="utf-8") as f:
            # Create a group from the string content
            group = StringTemplateGroup(name="graph", file=f, rootDir="templates")

            root_template = group.getInstanceOf("graph")

        if root_template is not None:
            root_template["flake"] = NixFlakeMetadataDecorator(metadata)

        return str(root_template)

    def generate_output(self, flakeRef: str, outputFile: str):
        """
        Generates the output file.
        :param flakeRef: The flake reference (either a folder or an url).
        :type flakeRef: str
        :param outputFile: The output file.
        :type outputFile: str
        """
        content = self.dot(flakeRef)
        if content is not None:
            with open(outputFile, "w") as file:
                file.write(content)
            Dot.logger().info(
                f"{outputFile} file created successfully by {self.__class__}"
            )

    @classmethod
    @listen(DotRequested)
    async def listen(cls, event: DotRequested):
        """
        Receives a DotRequested event and generates a dot file.
        :param event: The event.
        :type event: rydnr.nix.flake.graphviz.events.DotRequested
        """
        cls().generate_output(event.flake_ref, event.output_file)

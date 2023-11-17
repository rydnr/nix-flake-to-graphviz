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
import abc
from .nix_flake_metadata_decorator import NixFlakeMetadataDecorator
from pathlib import Path
from pythoneda import EventListener, listen, Port, primary_key_attribute
from pythoneda.shared.nix_flake import NixFlakeMetadata
from rydnr.nix.flake.graphviz.events import DotRequested
from stringtemplate3 import StringTemplateGroup
from typing import Dict


class Dot(EventListener, Port, abc.ABC):
    """
    Creates a dot file representing the dependencies of a given Nix flake.

    Class name: Dot

    Responsibilities:
        - Generate valid dot files from Nix flake's inputs.

    Collaborators:
        - None
    """

    _enabled = True

    def __init__(self):
        """
        Creates a new Dot instance.
        """
        super().__init__()

    @classmethod
    def is_enabled(cls) -> bool:
        """
        Checks if the class is enabled or not.
        :return: True in such case.
        :rtype: bool
        """
        return cls._enabled

    @classmethod
    def set_enabled(cls, flag: bool):
        """
        Enables or disables all classes.
        :param flag: The flag.
        :type flag: bool
        """
        cls._enabled = flag

    enabled = property(is_enabled, set_enabled)

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
        result = None
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

    def _convert_to_dot_format(self, metadata: NixFlakeMetadata) -> str:
        """
        Converts given flake metadata to dot format.
        :param metadata: The Nix flake metadata.
        :type metadata: pythoneda.shared.nix_flake.NixFlakeMetadata
        :return: A dot-formatted representation of the Nix flake dependiencies.
        :rtype: str
        """
        root_template = None

        with open(Path("templates") / f"dot.stg", "r", encoding="utf-8") as f:
            # Create a group from the string content
            group = StringTemplateGroup(name="graph", file=f, rootDir="templates")

            root_template = group.getInstanceOf("graph")

        if root_template is not None:
            root_template["flake"] = NixFlakeMetadataDecorator(metadata)

        return str(root_template)

    def _old_convert_to_dot_format(self, metadata: NixFlakeMetadata) -> str:
        """
        Converts given flake metadata to dot format.
        :param metadata: The Nix flake metadata.
        :type metadata: pythoneda.shared.nix_flake.NixFlakeMetadata
        :return: A dot-formatted representation of the Nix flake dependiencies.
        :rtype: str
        """
        title = metadata.url()
        indirect_inputs = metadata.indirect_inputs()
        inputs = metadata.inputs()
        direct_inputs_with_duplicates = metadata.inputs_with_duplicates()
        duplicated_inputs = metadata.duplicated_inputs()

        result = f'digraph "{title}" {{\n'
        result += f'  rankdir=TD;\n  compound=true;\n  label="{title}";\n\n'
        result += '  root [label="inputs", shape="circle", fillcolor="black", fontcolor="black", fixedsize="false"];\n'

        # Direct nodes
        result += '  node [shape="ellipse", style="filled", fontcolor="black", fillcolor="green"];\n\n'
        for input in [input for input in inputs if not metadata.has_duplicates(input)]:
            normalized_name = metadata.normalized_input_name(input)
            node_name = self.__class__.kebab_to_camel(input.name)
            label = self._build_label(normalized_name, input.version)
            result += f'  {node_name} [label="{label}"];\n'

        result += '  node [shape="ellipse", style="filled", fontcolor="white", fillcolor="darkgreen"];\n\n'
        for input in [
            input
            for input in inputs
            if metadata.has_duplicates(input)
            and not metadata.has_duplicates_with_different_version(input)
        ]:
            node_name = self.__class__.kebab_to_camel(input.name)
            label = self._build_label(normalized_name, input.version)
            result += f'  {node_name} [label="{label}"];\n'

        result += '  node [shape="ellipse", style="filled", fillcolor="darkblue"];\n\n'
        for input in [
            input
            for input in inputs
            if metadata.has_duplicates(input)
            and metadata.has_duplicates_with_different_version(input)
        ]:
            node_name = self.__class__.kebab_to_camel(input.name)
            label = self._build_label(normalized_name, input.version)
            result += f'  {node_name} [label="{label}"];\n'

        # Indirect nodes
        result += '  node [shape="rectangle", style="filled", fontcolor="black", fillcolor="grey"];\n\n'
        for input in [
            input for input in indirect_inputs if not metadata.has_duplicates(input)
        ]:
            normalized_name = metadata.normalized_input_name(input)
            node_name = self.__class__.kebab_to_camel(input.name)
            label = self._build_label(normalized_name, input.version)
            result += f'  {node_name} [label="{label}"];\n'

        result += '  node [shape="rectangle", style="filled", fontcolor="black", fillcolor="orange"];\n\n'
        for input in [
            input
            for input in indirect_inputs
            if metadata.has_duplicates(input)
            and not metadata.has_duplicates_with_different_version(input)
        ]:
            normalized_name = metadata.normalized_input_name(input)
            node_name = self.__class__.kebab_to_camel(input.name)
            label = self._build_label(normalized_name, input.version)
            result += f'  {node_name} [label="{label}"];\n'

        # Duplicated indirect nodes
        result += '  node [shape="rectangle", style="filled", fillcolor="red"];\n\n'
        for input in [
            input
            for input in indirect_inputs
            if metadata.has_duplicates(input)
            and metadata.has_duplicates_with_different_version(input)
        ]:
            normalized_name = metadata.normalized_input_name(input)
            node_name = self.__class__.kebab_to_camel(input.name)
            label = self._build_label(normalized_name, input.version)
            result += f'  {node_name} [label="{label}"];\n'

        result += "\n  // dependency graph\n"
        # Adding edges
        for input in inputs:
            nodeName = self.__class__.kebab_to_camel(input.name)
            result += f"  root -> {nodeName};\n"

        all_inputs = []
        [
            all_inputs.append(input)
            for input in inputs + indirect_inputs
            if input not in all_inputs
        ]
        for input in all_inputs:
            nodeName = self.__class__.kebab_to_camel(input.name)
            for ref in input.inputs:
                depName = self.__class__.kebab_to_camel(ref.name)
                result += f"  {nodeName} -> {depName};\n"

        # duplicates
        links = {}
        for input in [input for input in all_inputs if metadata.has_duplicates(input)]:
            nodeName = self.__class__.kebab_to_camel(input.name)
            for ref in metadata.get_duplicates(input):
                depName = self.__class__.kebab_to_camel(ref.name)
                if links.get(depName, None) is None:
                    result += f"  {nodeName} -> {depName} [style=dotted];\n"
                    links[nodeName] = depName

        result += "}\n"

        return result

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
    @abc.abstractmethod
    def instance(cls):
        """
        Retrieves an instance.
        :return: A Dot instance.
        :rtype: rydnr.nix.flake.graphviz.Dot
        """
        pass

    @classmethod
    @abc.abstractmethod
    def priority(cls) -> int:
        """
        Retrieves the priority of the implementation.
        :return: The priority value. The lower, the more priorized.
        :rtype: int
        """
        pass

    @classmethod
    @listen(DotRequested)
    async def listen(cls, event: DotRequested):
        """
        Receives a DotRequested event and generates a dot file.
        :param event: The event.
        :type event: rydnr.nix.flake.graphviz.events.DotRequested
        """
        if Dot.enabled:
            instance = cls.instance()
            if instance is not None:
                instance.generate_output(event.flake_ref, event.output_file)

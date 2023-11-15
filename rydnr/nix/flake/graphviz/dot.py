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
from pythoneda import EventListener, listen, Port, primary_key_attribute
from pythoneda.shared.nix_flake import NixFlakeMetadata
import re
from rydnr.nix.flake.graphviz.events import DotRequested
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

    def dot(self, flakeFolder: str) -> str:
        """
        Retrieves a dot representation of the flake metadata.
        :param flakeFolder: The flake folder.
        :type flakeFolder: str
        :return: Such content.
        :rtype: str
        """
        return self._convert_to_dot_format(
            NixFlakeMetadata.from_folder(flakeFolder).metadata
        )

    def _normalize_node_name(self, nodeName: str) -> str:
        """
        Normalizes given name, according to Nix flake conventions.
        :param nodeName: The node name.
        :type nodeName: str
        :return: The normalized name.
        :rtype: str
        """
        return re.sub(r"_\d+$", "", nodeName)

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
        direct_nodes = []
        direct_nodes_with_duplicates = []
        duplicated_nodes = []
        node_versions = {}
        for node, details in deps.get("root", {}).get("inputs", {}).items():
            version = self._get_version(node, deps[node])
            normalized_name = self._normalize_node_name(node)
            node_versions[normalized_name] = version
            node_versions[node] = version
            direct_nodes.append(node)
        for node, details in items:
            if node not in direct_nodes:
                if "locked" in details:
                    normalized_name = self._normalize_node_name(node)
                    version = self._get_version(node, deps[node])
                    if node_versions.get(normalized_name, None) is None:
                        node_versions[normalized_name] = version
                    else:
                        direct_nodes_with_duplicates.append(normalized_name)
                        duplicated_nodes.append(node)
                    node_versions[node] = version

        print(direct_nodes_with_duplicates)
        # Direct nodes
        result += '  node [shape="ellipse", style="filled", fillcolor="green"];\n\n'
        for node, details in deps.get("root", {}).get("inputs", {}).items():
            normalized_name = self._normalize_node_name(node)
            if normalized_name not in direct_nodes_with_duplicates:
                node_name = self.__class__.kebab_to_camel(node)
                label = self._build_label(normalized_name, node_versions[node])
                result += f'  {node_name} [label="{label}"];\n'
        result += '  node [shape="ellipse", style="filled", fillcolor="darkgreen"];\n\n'
        for node, details in deps.get("root", {}).get("inputs", {}).items():
            normalized_name = self._normalize_node_name(node)
            if normalized_name in direct_nodes_with_duplicates:
                node_name = self.__class__.kebab_to_camel(node)
                label = self._build_label(normalized_name, node_versions[node])
                result += f'  {node_name} [label="{label}"];\n'

        # Indirect nodes
        result += '  node [shape="rectangle", style="filled", fillcolor="grey"];\n\n'
        for node, details in items:
            if node not in direct_nodes and node not in duplicated_nodes:
                normalized_name = self._normalize_node_name(node)
                node_name = self.__class__.kebab_to_camel(node)
                if "locked" in details:
                    label = self._build_label(normalized_name, node_versions[node])
                    result += f'  {node_name} [label="{label}"];\n'

        # Duplicated indirect nodes
        result += '  node [shape="rectangle", style="filled", fillcolor="red"];\n\n'
        for node, details in items:
            if node not in direct_nodes and node in duplicated_nodes:
                normalized_name = self._normalize_node_name(node)
                node_name = self.__class__.kebab_to_camel(node)
                if "locked" in details:
                    label = self._build_label(normalized_name, node_versions[node])
                    result += f'  {node_name} [label="{label}"];\n'

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

    def generate_output(self, flakeFolder: str, outputFile: str):
        """
        Generates the output file.
        :param flakeFolder: The flake folder.
        :type flakeFolder: str
        :param outputFile: The output file.
        :type outputFile: str
        """
        with open(outputFile, "w") as file:
            file.write(self.dot(flakeFolder))

        Dot.logger().info(f"{outputFile} file created successfully by {self.__class__}")

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
                instance.generate_output(event.flake_folder, event.output_file)

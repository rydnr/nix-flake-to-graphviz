# vim: set fileencoding=utf-8
"""
rydnr/nix/flake/graphviz/nix_flake_metadata_decorator.py

This file defines the NixFlakeMetadataDecorator class.

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
from pythoneda.shared import primary_key_attribute, ValueObject
from pythoneda.shared.nix_flake import (
    NixFlakeInput,
    NixFlakeInputRelationship,
    NixFlakeMetadata,
)
from typing import List


class NixFlakeMetadataDecorator(ValueObject):
    """
    Decorator to access metadata from Nix flakes in templates.

    Class name: NixFlakeMetadataDecorator

    Responsibilities:
        - Provide any Nix flake metadata information to templates.

    Collaborators:
        - rydnr.nix.flake.graphviz.Dot
    """

    def __init__(self, metadata: NixFlakeMetadata):
        """
        Creates a new NixFlakeMetadataDecorator instance.
        """
        super().__init__()
        self._metadata = metadata

    @property
    @primary_key_attribute
    def metadata(self) -> NixFlakeMetadata:
        """
        Retrieves the decorated NixFlakeMetadata.
        :return: Such instance.
        :rtype: pythoneda.shared.nix_flake.NixFlakeMetadata
        """
        return self._metadata

    @property
    def title(self) -> str:
        """
        Retrieves the title.
        :return: Such text.
        :rtype: str
        """
        return self.metadata.url()

    @property
    def inputs(self) -> List[NixFlakeInput]:
        """
        Retrieves the direct dependencies.
        :return: The list of direct dependencies.
        :rtype: List[pythoneda.shared.nix_flake.NixFlakeInput]
        """
        return self.metadata.inputs()

    @property
    def inputs_with_no_duplicates(self) -> List[NixFlakeInput]:
        """
        Retrieves the direct dependencies with no duplicates.
        :return: The list of inputs with no duplicates.
        :rtype: List[pythoneda.shared.nix_flake.NixFlakeInput]
        """
        return self.metadata.inputs_with_no_duplicates()

    @property
    def inputs_with_duplicates_with_same_version(self) -> List[NixFlakeInput]:
        """
        Retrieves the direct dependencies with duplicates sharing the same version.
        :return: The list of inputs with duplicates with the same version.
        :rtype: List[pythoneda.shared.nix_flake.NixFlakeInput]
        """
        return self.metadata.inputs_with_duplicates_with_same_version()

    @property
    def inputs_with_duplicates_with_different_versions(self) -> List[NixFlakeInput]:
        """
        Retrieves the direct dependencies with duplicates with different versions.
        :return: The list of inputs with duplicates with different version.
        :rtype: List[pythoneda.shared.nix_flake.NixFlakeInput]
        """
        return self.metadata.inputs_with_duplicates_with_different_versions()

    @property
    def indirect_inputs_with_no_duplicates(self) -> List[NixFlakeInput]:
        """
        Retrieves the indirect dependencies with no duplicates.
        :return: The list of indirect inputs with no duplicates.
        :rtype: List[pythoneda.shared.nix_flake.NixFlakeInput]
        """
        return self.metadata.indirect_inputs_with_no_duplicates()

    @property
    def indirect_inputs_with_duplicates_with_same_version(self) -> List[NixFlakeInput]:
        """
        Retrieves the indirect dependencies with duplicates sharing the same version.
        :return: The list of indirect inputs with duplicates with the same version.
        :rtype: List[pythoneda.shared.nix_flake.NixFlakeInput]
        """
        self.metadata.indirect_inputs_with_duplicates_with_same_version()
        return self.metadata.indirect_inputs_with_duplicates_with_same_version()

    @property
    def indirect_inputs_with_duplicates_with_different_versions(
        self,
    ) -> List[NixFlakeInput]:
        """
        Retrieves the indirect dependencies with duplicates with different versions.
        :return: The list of indirect inputs with duplicates with different versions.
        :rtype: List[pythoneda.shared.nix_flake.NixFlakeInput]
        """
        return self.metadata.indirect_inputs_with_duplicates_with_different_versions()

    @property
    def all_edges(self) -> List[NixFlakeInputRelationship]:
        """
        Retrieves the list of relationships between inputs.
        :return: Such list.
        :rtype: List[pythoneda.shared.nix_flake.NixFlakeInputRelationship]
        """
        return self.metadata.all_relationships()

    @property
    def edges_for_duplicated_nodes(self) -> List[NixFlakeInputRelationship]:
        """
        Retrieves a list of relationships linking dependencies with duplicates.
        :return: Such list.
        :rtype: List[pythoneda.shared.nix_flake.NixFlakeInputRelationship]
        """
        return self.metadata.relationships_for_duplicated_nodes()

"""
rydnr/nix/flake/graphviz/infrastructure/github_dot.py

This file defines GithubDot class.

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
from pythoneda.shared.git import GitRepo, GitTag
from pythoneda.shared.nix_flake import NixFlakeMetadata
from typing import Dict


class GithubDot(Dot):
    """
    Creates a dot file representing the dependencies of a given Nix flake,
    using Github API to retrieve the version of the dependencies.

    Class name: GithubDot

    Responsibilities:
        - Generate valid dot files from Nix flake's inputs.

    Collaborators:
        - None
    """

    _singleton = None

    def __init__(self, githubToken: str):
        """
        Creates a new Dot instance.
        :param githubToken: The github token.
        :type githubToken: str
        """
        super().__init__()
        self._github_token = githubToken

    @property
    def github_token(self) -> str:
        """
        Retrieves the github token.
        :return: Such token.
        :rtype: str
        """
        return self._github_token

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
        result = None
        locked = content.get("locked", None)
        if locked is not None:
            type = locked.get("type", None)
            rev = locked.get("rev", None)
            if type is not None and rev is not None:
                if type == "github":
                    owner = locked.get("owner", None)
                    repo = locked.get("repo", None)
                    version = GitTag.latest_github_tag(
                        self.github_token, owner, repo, rev
                    )
                    if version is not None:
                        result = version

        return result

    @classmethod
    def initialize(cls, token: str):
        """
        Initializes the singleton.
        :param token: The github token.
        :type token: str
        """
        if token is not None:
            cls._singleton = GithubDot(token)

    @classmethod
    def priority(cls) -> int:
        """
        Retrieves the priority of the implementation.
        :return: The priority value. The lower, the more priorized.
        :rtype: int
        """
        return 50

    @classmethod
    def enabled(cls) -> bool:
        """
        Checks if the class is enabled or not.
        :return: True in such case.
        :rtype: bool
        """
        return cls._singleton is not None

    @classmethod
    def instance(cls):
        """
        Retrieves the singleton instance.
        :return: Such instance.
        :rtype: Ports
        """
        result = cls._singleton
        if result is None:
            GithubDot.logger().error("GithubDot not yet bound to a Github token.")
        return result

    def generate_output(self, flakeFolder: str, outputFile: str):
        """
        Generates the output file.
        :param flakeFolder: The flake folder.
        :type flakeFolder: str
        :param outputFile: The output file.
        :type outputFile: str
        """
        super().generate_output(flakeFolder, outputFile)
        # to prevent DefaultDot to run
        Dot.enabled = False

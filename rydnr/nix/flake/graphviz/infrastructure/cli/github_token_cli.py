"""
rydnr/nix/flake/graphviz/infrastructure/cli/github_token_cli.py

This file defines the GithubTokenCli.

Copyright (C) 2023-today rydnr's https://github.com/rydnr/nix-flake-to-graphviz

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
import argparse
from pythoneda import BaseObject, PrimaryPort


class GithubTokenCli(BaseObject, PrimaryPort):

    """
    A PrimaryPort used to gather the github token.

    Class name: GithubTokenCli

    Responsibilities:
        - Parse the command-line to retrieve the github token.

    Collaborators:
        - PythonEDA subclasses: They are notified back with the information retrieved from the command line.
    """

    def priority(self) -> int:
        """
        Retrieves the priority of this port.
        :return: The priority.
        :rtype: int
        """
        return 80

    @classmethod
    @property
    def is_one_shot_compatible(cls) -> bool:
        """
        Retrieves whether this primary port should be instantiated when
        "one-shot" behavior is active.
        It should return False unless the port listens to future messages
        from outside.
        :return: True in such case.
        :rtype: bool
        """
        return True

    async def accept(self, app):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA instance.
        :type app: PythonEDA
        """
        parser = argparse.ArgumentParser(
            description="Provide a token to access the Github API"
        )

        parser.add_argument(
            "-t", "--github-token", required=False, help="The github token"
        )

        args, unknown_args = parser.parse_known_args()

        await app.accept_github_token(args.github_token)

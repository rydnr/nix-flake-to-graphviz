# vim: set fileencoding=utf-8
"""
rydnr/nix/flake/graphviz/infrastructure/cli/dot_requested_cli.py

This file declares the DotRequestedCli class.

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
from argparse import ArgumentParser
from pythoneda.shared import PrimaryPort
from pythoneda.shared.application import PythonEDA
from pythoneda.shared.infrastructure.cli import CliHandler
from rydnr.nix.flake.graphviz.events import DotRequested


class DotRequestedCli(CliHandler, PrimaryPort):
    """
    A PrimaryPort used to inject a DotRequested into nix-flake-to-graphviz application.

    Class name: FlakeFolderCli

    Responsibilities:
        - Parse the command-line to retrieve the information to build a DotRequested event.

    Collaborators:
        - pythoneda.shared.application.PythonEDA: It is notified back with the information retrieved from the command line.
    """

    def __init__(self):
        """
        Creates a new DotRequestedCli instance.
        """
        super().__init__(
            "Creates a dot file representing the dependency graph of a Nix flake"
        )

    @classmethod
    def priority(self) -> int:
        """
        Retrieves the priority of this port.
        :return: The priority.
        :rtype: int
        """
        return 90

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

    def add_arguments(self, parser: ArgumentParser):
        """
        Defines the specific CLI arguments.
        :param parser: The parser.
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument(
            "-f",
            "--flake-ref",
            required=True,
            help="The flake reference (either a folder or an url)",
        )
        parser.add_argument(
            "-o", "--output-file", required=True, help="The output file"
        )

    async def handle(self, app: PythonEDA, args):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA instance.
        :type app: pythoneda.shared.application.PythonEDA
        :param args: The CLI args.
        :type args: argparse.args
        """
        await app.accept(DotRequested(args.flake_ref, args.output_file))

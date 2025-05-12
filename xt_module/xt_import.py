#! /usr/bin/python3
###############################################################################
 #    BSD LICENSE
 #
 #    Copyright (c) Saul Han <2573789168@qq.com>
 #
 #    Redistribution and use in source and binary forms, with or without
 #    modification, are permitted provided that the following conditions
 #    are met:
 #
 #       Redistributions of source code must retain the above copyright
 #        notice, this list of conditions and the following disclaimer.
 #       Redistributions in binary form must reproduce the above copyright
 #        notice, this list of conditions and the following disclaimer in
 #        the documentation and/or other materials provided with the
 #        distribution.
 #
 #    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 #    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 #    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 #    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 #    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 #    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 #    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 #    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 #    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 #    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 #    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################
import os
import sys
import importlib.util
from pathlib import Path

class PathImport(object):
    def __init__(self, project_path):
        self.project_path = project_path

    def local_import_from_path(self, filepath, include_private=False):
        """
        Dynamically imports a module from the specified file path and returns its attributes and methods.

        Parameters:
            filepath (str): The file path of the module to be imported.
            include_private (bool, optional): Whether to include private attributes and methods (names starting with '_').
                                              Defaults to False, meaning private attributes and methods are excluded.

        Returns:
            dict: A dictionary containing all public (or optionally private) attributes and methods of the module,
                  with keys as attribute/method names and values as their corresponding values or functions.
        """
        # Resolve the file path and generate the module name
        path = Path(filepath).resolve()
        module_name = path.stem  # Use the file name without extension as the module name

        # Create the module specification and load the module
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # Execute the module code

        # Filter out private attributes (optional)
        namespace = {}
        for name in dir(module):
            if include_private or not name.startswith("_"):
                namespace[name] = getattr(module, name)

        return namespace


    def module_import_from_path(self, file_path, module_name=None):
        """
        Imports a module from the specified file path.

        :param file_path: The absolute path to the module file (.py file).
        :param module_name: Optional custom module name; defaults to the file name if not provided.
        :return: The imported module object.
        """
        # Check if the provided file path exists, if not, attempt to locate it within the project path
        if not os.path.exists(file_path):
            file_path = os.path.join(self.project_path, file_path)
            # Ensure the file exists after attempting to join with the project path
            assert os.path.exists(file_path), f"File not found: {file_path}"

        # Handle module name
        if module_name is None:
            # Extract the base module name from the file name
            module_name = os.path.splitext(os.path.basename(file_path))[0]

        # Create module specification
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        # Handle failure to create module specification
        if spec is None:
            raise ImportError(f"Failed to create module specification from path {file_path}")

        # Create and load the module
        module = importlib.util.module_from_spec(spec)
        # Add the newly created module to the global module cache
        sys.modules[module_name] = module
        # Execute the module to initialize it
        spec.loader.exec_module(module)

        # Return the initialized module object
        return module

    def global_import_all_from_path(self, file_path):
        """
        Imports all contents from a module at the specified path into the current namespace, avoiding duplicate imports.

        Parameters:
            file_path (str): The path to the module file to be imported.

        Returns:
            None, but updates the caller's global namespace with all public contents of the module.

        Raises:
            ImportError: If the module cannot be loaded from the specified path.
        """
        # Extract the module name (removing path and extension)
        module_name = os.path.splitext(os.path.basename(file_path))[0]

        # Check if the module already exists to avoid duplicate imports
        if module_name in sys.modules:
            module = sys.modules[module_name]
        else:
            # Create the module's spec based on the file location
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None:
                raise ImportError(f"Cannot load module from path {file_path}")

            # Create and execute the module object
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module  # Register in sys.modules before execution
            spec.loader.exec_module(module)

        # Get the list of names to export, prioritizing the module's __all__ attribute
        if hasattr(module, '__all__'):
            names = module.__all__
        else:
            names = [n for n in dir(module) if not n.startswith('_')]

        # Update the current global namespace with the module's contents
        caller_globals = sys._getframe(1).f_globals  # Get the caller's global namespace
        caller_globals.update({name: getattr(module, name) for name in names})












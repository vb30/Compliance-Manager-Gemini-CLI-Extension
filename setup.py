#!/usr/bin/env python
# Copyright 2025 Varun Bhardwaj
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

setup(
    name="compliance-manager-gemini-cli-extension",
    version="1.0.0",
    description="Gemini CLI extension for Google Cloud Compliance Manager",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Varun Bhardwaj",
    author_email="varun@example.com",
    url="https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension",
    license="Apache 2.0",
    packages=find_packages(),
    py_modules=["compliance_manager_mcp"],
    python_requires=">=3.11",
    install_requires=[
        "httpx>=0.28.1",
        "mcp[cli]>=1.4.1",
        "python-dotenv>=1.0.0",
        "typing-extensions>=4.8.0",
        "aiohttp>=3.9.0",
        "asyncio>=3.4.3",
        "google-cloud-cloudsecuritycompliance>=0.2.0",
        "uvicorn[standard]",
    ],
    entry_points={
        "console_scripts": [
            "compliance_manager_mcp=compliance_manager_mcp:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="google cloud compliance security mcp gemini-cli",
)


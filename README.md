pinto-pizzazz
=============

=============
TeX-freefrommacrofile
=============
A simple script that scans a TeX source file for uses of user-defined macros and moves them from separate macro files to the preamble of the TeX source file.

Usage: TeX-freefrommacrofile macros.tex file.tex

It crudely splits macros.tex into individual macro definitions (e.g. \newcommand\foo\bar), then for each macro definition searches file.tex for an appeal to that defined macro. It collects the ones that do appear in file.tex and adds those to the preamble of file.tex.

To-do: before writing macros above \begin{document} to new file, remove all lines beginning with % and empty lines.

To-do: expand to handle more than one macro file & more than one TeX file. [Easy]

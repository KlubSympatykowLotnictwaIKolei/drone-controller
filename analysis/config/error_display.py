from collections import deque
import logging as log
from typing import List, Tuple
from pydantic_core import ValidationError

class ErrorDisplay:
    def __find_in_file(self, field: str) -> str: 
        """
        For finding the entire line in the original file
        """
        for line in self.file_lines:
            if field in line:
                if line.strip().startswith('#'):
                    continue
                return line
        return None

    def __log_error_message(self, msg: str, lines: List[str], missing: List[str]) -> None:
        message_to_print = "Config validation error\n"
        starting_spaces = 0
        line_text_len = 0

        for line in lines:
            if len(line) > 0:
                line_text_len = len(line.lstrip())
                starting_spaces = len(line) - line_text_len
            message_to_print += f"{line}\n"
        spaces = " " * starting_spaces
        
        funky_arrows = "^" * (line_text_len)
        message_to_print +=(f"{spaces}\x1b[1;31m{funky_arrows}\x1b[0m\n")
        message_to_print +=(f"{msg}\n")
        if len(missing) > 0:
            message_to_print +=(f"Missing arguments: {missing}")
            message_to_print +=("\n")
        log.error(message_to_print)

    def __trim_yaml_line_keep_indent(self, line: str) -> str:
        """
        For trimming the line in the original file
        """
        if line.strip().startswith('#'):
            return ""
        comment_index = line.find(' #')
        if comment_index != -1:
            return line[:comment_index]
        return line

    def __generate_file_lines(self, file_lines: List[str], loc: List[str]) -> Tuple[List[str], List[str]]:
        def process_keyword(current_keyword: str, current_indent: int) -> None:
            nonlocal i, lines, dots_added, previous_loc
            if current_keyword == loc[i]:
                previous_loc = loc[i]
                i += 1
                lines.append(line)
                dots_added = False
            elif not dots_added:
                dots = current_indent * " " + "[...]"
                lines.append(dots)
                dots_added = True

        i = 0
        lines = []
        parents = deque()
        current_indent = -1 
        previous_loc = None
        dots_added = False
        
        for l in file_lines:
            line = self.__trim_yaml_line_keep_indent(l)
            if len(line) == 0:
                continue
            #? ig its fine to skip lists?
            if line.lstrip().startswith('-'):
                continue

            indent = len(line) - len(line.lstrip())

            if indent > current_indent:
                current_keyword = line.strip().split(':')[0]
                process_keyword(current_keyword, indent)
                parents.append((current_keyword, indent))
                current_indent = indent
            elif indent <= current_indent:
                while len(parents) > 0 and parents[-1][1] >= indent:
                    removed = parents.pop()
                    if removed[0] == previous_loc:
                        if dots_added:
                            lines.pop()
                        return lines, list(loc[i:])
                    current_indent = indent
                current_keyword = line.strip().split(':')[0]
                process_keyword(current_keyword, indent)
                parents.append((current_keyword, indent))

        return lines , []

    def __call__(self, error: ValidationError, file_lines: List[str], fancy_errors: bool = True) -> None:
        self.file_lines = file_lines
        
        errors = {i: (error['loc'], error['msg'])
                for i, error in enumerate(error.errors())}
        
        if fancy_errors is False:
            for error, (loc, msg) in errors.items():
                log.error(f"{msg} at {loc}")
            return

        for error, (loc, msg) in errors.items():
            #loc is a list of fields indicated in pydantic error message
            lines , missing = self.__generate_file_lines(file_lines, loc)
            self.__log_error_message(msg, lines, missing)

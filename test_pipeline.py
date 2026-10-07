from language.parser import CommandParser
from execution.executor import Executor

parser = CommandParser()
executor = Executor()

command = "wait"
intent = parser.parse(command)

print("Command:", command)
print("Intent:", intent)

result = executor.execute(intent)

print("Execution result:", result)
print("Parser -> Intent -> Executor: OK")

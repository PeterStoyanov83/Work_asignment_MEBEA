def arithmetic_arranger(problems, show_answers=False):
    # Check if there are too many problems
    if len(problems) > 5:
        return "Error: Too many problems."

    top_line = []
    bottom_line = []
    dash_line = []
    answer_line = []

    for problem in problems:
        # Parse the problem string
        num1, op, num2 = problem.split()

        # Check if the operator is valid
        if op not in ('+', '-'):
            return "Error: Operator must be '+' or '-'."

        # Check if the operands contain only digits
        if not num1.isdigit() or not num2.isdigit():
            return "Error: Numbers must only contain digits."

        # Check if the operands have at most 4 digits
        if len(num1) > 4 or len(num2) > 4:
            return "Error: Numbers cannot be more than four digits."

        # Calculate the answer if show_answers is True
        if show_answers:
            if op == '+':
                answer = str(int(num1) + int(num2))
            else:
                answer = str(int(num1) - int(num2))
            answer_line.append(answer.rjust(len(num2) + 2))

        # Format the problem vertically
        width = max(len(num1), len(num2)) + 2
        top_line.append(num1.rjust(width))
        bottom_line.append(op + num2.rjust(width - 1))
        dash_line.append('-' * width)

    # Join the lines for each problem
    arranged_problems = []
    arranged_problems.append('    '.join(top_line))
    arranged_problems.append('    '.join(bottom_line))
    arranged_problems.append('    '.join(dash_line))
    if show_answers:
        arranged_problems.append('    '.join(answer_line))

    return '\n'.join(arranged_problems)


problems = ["32 + 698", "3801 - 2", "45 + 43", "123 + 49"]
print(arithmetic_arranger(problems))

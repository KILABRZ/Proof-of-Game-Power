from random import randint

MathProblems = 2000

problemSheet = open('resource/quiz/problems.txt', 'w')

def pushProblem_Answer(problemSheet, problem, answer):
	problemSheet.write('{};{}\n'.format(problem, answer))

for i in range(MathProblems):
	x = randint(1, 499)
	y = randint(1, 499)
	z = x + y
	problem = '{} + {} ='.format(x, y)
	answer = '{}'.format(z)

	pushProblem_Answer(problemSheet, problem, answer)




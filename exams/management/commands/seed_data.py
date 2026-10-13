from django.core.management.base import BaseCommand
from exams.models import Subject, Exam, Question
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seed the database with sample subjects, exams, and questions'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database with development data...')
        
        # Create Subjects
        cs_subject, _ = Subject.objects.get_or_create(
            slug='computer-science',
            defaults={'name': 'Computer Science', 'description': 'All about computers and programming.'}
        )
        math_subject, _ = Subject.objects.get_or_create(
            slug='mathematics',
            defaults={'name': 'Mathematics', 'description': 'Numbers, quantities, shapes, and patterns.'}
        )
        
        # Create Exams
        exam1, _ = Exam.objects.get_or_create(
            slug='python-basics',
            defaults={
                'title': 'Python Basics',
                'description': 'A fundamental test on Python programming constructs.',
                'subject': cs_subject,
                'duration_minutes': 10,
                'total_marks': 10,
                'passing_marks': 5,
                'difficulty': 'Easy',
                'is_published': True,
            }
        )
        
        exam2, _ = Exam.objects.get_or_create(
            slug='advanced-algorithms',
            defaults={
                'title': 'Advanced Algorithms',
                'description': 'Test your knowledge on complex algorithms and data structures.',
                'subject': cs_subject,
                'duration_minutes': 30,
                'total_marks': 20,
                'passing_marks': 10,
                'negative_marking_enabled': True,
                'negative_marks': 0.5,
                'difficulty': 'Hard',
                'is_published': True,
            }
        )

        # Questions for Exam 1
        if not Question.objects.filter(exam=exam1).exists():
            Question.objects.create(
                exam=exam1, question_text='What is the output of print(2 ** 3)?',
                option_a='6', option_b='8', option_c='9', option_d='None',
                correct_option='B', marks=2, order=1
            )
            Question.objects.create(
                exam=exam1, question_text='Which keyword is used to define a function in Python?',
                option_a='func', option_b='def', option_c='define', option_d='function',
                correct_option='B', marks=2, order=2
            )
            Question.objects.create(
                exam=exam1, question_text='Is Python case-sensitive?',
                option_a='Yes', option_b='No', option_c='Only in variable names', option_d='Only in function names',
                correct_option='A', marks=2, order=3
            )
            Question.objects.create(
                exam=exam1, question_text='What data type is the result of: 10 / 2?',
                option_a='int', option_b='float', option_c='str', option_d='bool',
                correct_option='B', marks=2, order=4
            )
            Question.objects.create(
                exam=exam1, question_text='Which collection is ordered, changeable, and allows duplicate members?',
                option_a='Set', option_b='Tuple', option_c='Dictionary', option_d='List',
                correct_option='D', marks=2, order=5
            )
            
        # Questions for Exam 2
        if not Question.objects.filter(exam=exam2).exists():
            Question.objects.create(
                exam=exam2, question_text='What is the time complexity of binary search?',
                option_a='O(n)', option_b='O(1)', option_c='O(log n)', option_d='O(n^2)',
                correct_option='C', marks=4, order=1
            )
            Question.objects.create(
                exam=exam2, question_text='Which data structure uses LIFO?',
                option_a='Queue', option_b='Stack', option_c='Tree', option_d='Graph',
                correct_option='B', marks=4, order=2
            )
            Question.objects.create(
                exam=exam2, question_text='What algorithm is used to find the shortest path in a graph?',
                option_a='Merge Sort', option_b='Dijkstra', option_c='Quick Sort', option_d='Binary Search',
                correct_option='B', marks=4, order=3
            )
            Question.objects.create(
                exam=exam2, question_text='Which sorting algorithm has the worst-case time complexity of O(n^2)?',
                option_a='Merge Sort', option_b='Quick Sort', option_c='Heap Sort', option_d='Radix Sort',
                correct_option='B', marks=4, order=4
            )
            Question.objects.create(
                exam=exam2, question_text='What is a characteristic of a Red-Black Tree?',
                option_a='It is completely unbalanced', option_b='It does not allow deletion', option_c='It is a self-balancing binary search tree', option_d='It can only store integers',
                correct_option='C', marks=4, order=5
            )
            
        self.stdout.write(self.style.SUCCESS("Successfully seeded development data."))

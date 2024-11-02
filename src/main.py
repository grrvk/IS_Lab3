import copy
import random

from src.utils import read_groups, read_teachers, read_auditoriums, read_subjects, exportSchedule
from src.scheme import Lesson, Schedule

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
PERIODS = ['1', '2', '3']
PERIOD_CORRESPONDING = ['8:40-10:15', '10:35-12:10', '12:20-13:55']
TIME_SLOTS = [(day, period) for day in DAYS for period in PERIODS]

auditoriums = read_auditoriums()
groups = read_groups()
teachers = read_teachers()
subjects = read_subjects(groups)


def generateRandomSchedule():
    schedule = Schedule(TIME_SLOTS)

    for subject in subjects:
        for _ in range(subject.lectures_number):
            lesson = Lesson(subject=subject,
                            subject_type='Лекція',
                            group=subject.group)
            randomAssignment(lesson=lesson, schedule=schedule)
        if subject.requires_subgroups:
            for subgroup in subject.group.subgroups:
                for _ in range(subject.practice_number // len(subject.group.subgroups)):
                    lesson = Lesson(subject=subject,
                                    subject_type='Практика',
                                    group=subject.group,
                                    subgroup=f"{subject.group.group_name}_{subgroup}")
                    randomAssignment(lesson=lesson, schedule=schedule)
        else:
            for _ in range(subject.practice_number):
                lesson = Lesson(subject=subject,
                                subject_type='Практика',
                                group=subject.group)
                randomAssignment(lesson=lesson, schedule=schedule)
    return schedule


def randomAssignment(lesson: Lesson, schedule):
    time_slot = random.choice(TIME_SLOTS)
    auditorium = random.choice(auditoriums)
    available_teachers = [t for t in teachers if lesson.subject.subject_name in t.subjects_taught
                          and (lesson.subject_type == t.subject_type or t.subject_type == 'Обидва')]

    random_teacher = random.choice(available_teachers)

    lesson.time = time_slot
    lesson.teacher = random_teacher
    lesson.auditorium = auditorium

    schedule.timetable[time_slot].append(lesson)
    random_teacher.occupied_hours += 1.5


POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.2


def generateInitialPopulation(size=POPULATION_SIZE):
    population = []
    for _ in range(size):
        schedule = generateRandomSchedule()
        schedule.calculate_fitness()
        population.append(schedule)
    return population


def selectPopulationPart(population, split=0.5):
    population.sort(key=lambda x: x.fitness, reverse=True)
    selected = population[:int(POPULATION_SIZE * split)]
    return selected


def crossoverPopulations(parent1, parent2):
    child = Schedule(TIME_SLOTS)
    crossover_point = len(TIME_SLOTS) // 2
    for idx, time_slot in enumerate(TIME_SLOTS):
        if idx < crossover_point:
            child.timetable[time_slot] = copy.deepcopy(parent1.timetable[time_slot])
        else:
            child.timetable[time_slot] = copy.deepcopy(parent2.timetable[time_slot])
    return child


def herbivore_smoothing(population, best_schedule):
    new_population = []
    for _ in range(len(population)):
        new_schedule = copy.deepcopy(best_schedule)
        mutateSchedule(new_schedule, 0.1)
        new_population.append(new_schedule)
    return new_population


def predator_approach(population):
    population = selectPopulationPart(population, 0.5)
    return population


def rain(population):
    new_population = random.choices(population, k=int(POPULATION_SIZE*0.75))
    rain_population = generateInitialPopulation(size=POPULATION_SIZE-len(new_population))
    return new_population + rain_population


def mutateSchedule(schedule, mutation_rate=MUTATION_RATE):
    amountOfMutations = 0
    for time_slot in schedule.timetable:
        amountOfMutations += len(schedule.timetable[time_slot])
    amountOfMutations *= mutation_rate

    for _ in range(int(amountOfMutations)):
        available_timeslots = [t for t in list(schedule.timetable.keys()) if len(schedule.timetable[t]) != 0]
        time_slot = random.choice(available_timeslots)
        lesson = random.choice(schedule.timetable[time_slot])

        mutation_type = random.choice(['time_slot', 'auditorium', 'teacher'])
        if mutation_type == 'time_slot':
            new_time_slot = random.choice(TIME_SLOTS)
            schedule.timetable[time_slot].remove(lesson)
            lesson.time_slot = new_time_slot
            schedule.timetable[new_time_slot].append(lesson)
        elif mutation_type == 'auditorium':
            new_auditorium = random.choice(auditoriums)
            lesson.auditorium = new_auditorium
        elif mutation_type == 'lecturer':
            random_teacher = random.choice(teachers)
            lesson.teacher = random_teacher

    return schedule


def genetic_algorithm():
    population = generateInitialPopulation()

    for generation in range(GENERATIONS):
        predatorPopulation = predator_approach(population)
        selectedPopulations = rain(predatorPopulation)

        new_population = []
        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(selectedPopulations, 2)
            child = crossoverPopulations(parent1, parent2)
            child = mutateSchedule(child)
            child.calculate_fitness()
            new_population.append(child)

        population = new_population
        best_fitness = max(schedule.fitness for schedule in population)
        scheduleMaxFitness = next((schedule for schedule in population if schedule.fitness == best_fitness), None)
        least_conflicts = scheduleMaxFitness.numOfConflicts

        population = herbivore_smoothing(population, scheduleMaxFitness)

        if (generation + 1) % 10 == 0 or best_fitness == 1.0:
            print(f'Generation {generation + 1}: ConflictRate = {least_conflicts}')

    best_schedule = max(population, key=lambda x: x.fitness)
    return best_schedule


best_schedule = genetic_algorithm()
print('Generation finished')

print('Exporting')
exportSchedule(best_schedule)
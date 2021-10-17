from sched_package.task import Task
import plotly.figure_factory as ff


class IScheduleMultiples:
    """this class will analyze with constraint that tasks can be done in multiple times """
    def __init__(self, tasks_dict):
        self.tasks_dict = tasks_dict

    def comp_max_tasks(self, tasks_name_to_exclude=None):
        """compute maximum number of tasks inside one schedule
            O(n^2)
            Args:
                tasks_name_to_exclude: tasks not to include in calculation
            Returns:
                list of compatible tasks
        """
        if tasks_name_to_exclude is None:
            tasks_name_to_exclude = []

        # dict unfold into list
        # tasks_list = [t for tasks in self.tasks_dict.values() for t in tasks if t not in tasks_to_exclude]
        tasks_list = []
        for tasks in self.tasks_dict.values():
            for t in tasks:
                if t.name not in tasks_name_to_exclude:
                    tasks_list.append(t)

        if len(tasks_list) == 0:
            return None

        final_times = sorted(tasks_list, key=lambda t: t.end)
        res = [final_times[0]]

        # "visited tasks" marks the name of the person which is already scheduled.
        taken_tasks = [res[-1].name]

        for task in final_times:
            if task.start >= res[-1].end and task.name not in taken_tasks:
                res.append(task)
                taken_tasks.append(task.name)

        return res

    def comp_min_resources(self):
        """calculates the minimum number of machines such that all the tasks would run
            O(n^3)

            Args:
                None
            Returns:
                number of machines
        """
        resource = 0
        tasks_to_exclude = []

        while True:
            compatible_tasks = self.comp_max_tasks(tasks_name_to_exclude=tasks_to_exclude)
            if compatible_tasks is None:
                break
            tasks_to_exclude.extend([t.name for t in compatible_tasks])
            resource += 1
        return resource

    def show_opt_schedule(self, tasks=None):
        """plot gantt chart with optimal schedule

            Args:
                tasks: tasks to plot
            Returns:
                gantt chart

        """
        if tasks is None:
            tasks = self.comp_max_tasks()

        df = []
        for t in tasks:
            df.append(dict(Task=t.name, Start=f'2021-10-14 {t.start}:00:00', Finish=f'2021-10-14 {t.end}:00:00'))

        fig = ff.create_gantt(df)
        fig.show()

    def show_sched_multiple_showers(self):
        already_plotted = []
        for _ in range(self.comp_min_resources()):
            tasks = self.comp_max_tasks(tasks_name_to_exclude=already_plotted)
            already_plotted.extend([t.name for t in tasks])
            self.show_opt_schedule(tasks=tasks)


if __name__ == '__main__':
    tasks = {
        'Leela': [Task("Leela", 8, 10), Task("Leela", 17, 19)],
        'Fry': [Task("Fry", 9, 10), Task('Fry', 20, 22)],
        'Bender': [Task('Bender', 18, 19)],
        'Hermes': [Task('Hermes', 12, 13), Task("Hermes", 15, 17)],
        'Amy': [Task('Amy', 10, 16)],
        'Zoidberg': [Task('Zoidberg', 16, 17)],
        'Nibbler': [Task('Nibbler', 19, 21)]
    }

    s = IScheduleMultiples(tasks)
    res = s.comp_max_tasks()
    for x in res:
        print(x)
    # print(s.comp_min_resources())
    # s.show_sched_multiple_showers()
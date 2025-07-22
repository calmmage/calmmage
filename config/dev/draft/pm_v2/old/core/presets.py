class Preset:
    dirs: list
    softlinks: dict

    def build(self, root_dir):
        for dir in self.dirs:
            # create dir
            pass
        for source, target in self.softlinks.items():
            # create softlink
            pass


presets = []


class PresetJan2024(Preset):
    def build(self, root_dir):
        super().build(root_dir)

        # todo: build the first seasonal dir, add all soflinks

    dirs = [
        # "code",
        # "code/structured",
        "structured",
        "structured/lib",
        "structured/tools",
        # "structured/projects",
        "projects",
        "structured/unsorted",
        "structured/archive",
        "structured/beta",
        # "code/seasonal",
        # "code/seasonal/past",
        # "workspace/launchd/scripts",
        # "workspace/launchd/logs",
        "structured/dev",
        "structured/actual",
    ]
    # softlinks = {
    #       # "code/seasonal/latest": "code/seasonal/YYYY_MM_MMM",
    #       "code/seasonal/latest/experiments": "playground",
    #       "code/seasonal/latest/add_new_project": "~calmlib/tools/add_new_project.py",
    # }
    # this is the path that the 'new_project' tool will use
    seasonal_projects_dir = "projects/calmmage-private/seasonal/"
    new_projects_dir = "projects/calmmage-private/seasonal/latest/experiments"
    project_unsorted_dir = "structured/unsorted"
    # scripts_dir = "workspace/launchd/scripts"
    scripts_dir = "scripts"
    # all_projects_dir = "code/structured/projects"
    all_projects_dir = "projects"


presets.append(PresetJan2024)

# preset = Preset(
#     dirs=[
#         "code",
#         "code/structured",
#         "code/structured/lib",
#         "code/structured/tools",
#         "code/structured/projects",
#         "code/structured/unsorted",
#         "code/structured/archive",
#         "code/seasonal",
#         "code/seasonal/latest",
#         "code/seasonal/latest/p1",
#         "code/seasonal/latest/p2",
#         "code/seasonal/latest/experiments",
#         "code/seasonal/latest/refs",
#         "code/seasonal/past",
#         "playground",
#         ],
#     softlinks={
# #         # "code/seasonal/latest",
#         "code/seasonal/latest/experiments": "playground",
#         },
#     )
# presets.append(preset)

# class PresetJan2024(Preset):
#     """
#     dirs:
#     code/
#       structured/
#         lib/
#         tools/
#         projects/
#         unsorted/
#         archive/
#       seasonal/
#         YYYY_MM_MMM/
#           p1
#           p2
#           experiments/
#           refs
#           new_project -> ~calmlib/tools/new_project.py ...
#         latest/
#         past/
#     playground -> seasonal/latest/experiments

#     README.md "This is a managed dev environment, for more info see ..."
#     """

#     dirs = [
#         "code/structured/lib",
#         "code/structured/tools",
#         "code/structured/projects",
#         "code/structured/unsorted",
#         "code/structured/archive",
#         "code/seasonal/YYYY_MM_MMM/p1",
#         "code/seasonal/YYYY_MM_MMM/p2",
#         "code/seasonal/YYYY_MM_MMM/experiments",
#         "code/seasonal/YYYY_MM_MMM/refs",
#         "code/seasonal/YYYY_MM_MMM/new_project",
#         "code/seasonal/past",
#         # "playground",
#         ]
#     softlinks = {
#         # "code/seasonal/latest",
#         "code/seasonal/latest/experiments": "playground",
#         "code/seasonal/YYYY_MM_MMM/new_project": "~calmlib/tools/new_project.py",
#         }


# let's describe it better

# 1) static dirs
# 2) static soflinks
# 3) tools/jobs
# 4)

# class Dir:
#   pass

# class StaticDir(Dir):
#   def __init__(self, path):
#     self.path = path

# class StaticSoftlink(Dir):
#   def __init__(self, path, target):
#     self.path = path
#     self.target = target

# class StructuredDir(Dir):
#   def __init__(self, path, ):
#     self.path = path

# class DirTemplate(Dir):
#   def __init__(self, pattern):
#     self.pattern = pattern

latest_preset = presets[-1]

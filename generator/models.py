from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    emp_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    summary = models.TextField()
    technical_skills = models.TextField(help_text="Enter skills separated by commas")

    def __str__(self):
        return f"{self.name} ({self.emp_id})"

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class EmployeeProjectMapping(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='project_mappings')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.employee.name} -> {self.project.title}"
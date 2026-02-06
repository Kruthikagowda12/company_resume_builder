from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Employee, Project, EmployeeProjectMapping


def search_view(request):
    """Display search page"""
    return render(request, 'generator/search.html')


def dashboard(request):
    """Display and handle dashboard operations"""
    if request.method == "POST":
        # Check which form was submitted
        if 'create_emp' in request.POST:
            eid = request.POST['emp_id']
            
            # Check if ID already exists
            if Employee.objects.filter(emp_id=eid).exists():
                return HttpResponse("<h2>Error: Employee ID already exists!</h2><a href='/dashboard/'>Try again</a>")
            
            Employee.objects.create(
                name=request.POST['name'],
                emp_id=eid,
                email=request.POST['email'],
                summary=request.POST['summary'],
                technical_skills=request.POST['skills']
            )
        elif 'create_project' in request.POST:
            Project.objects.create(
                title=request.POST['title'],
                description=request.POST['desc']
            )
        elif 'assign_project' in request.POST:
            emp = Employee.objects.get(id=request.POST['emp_select'])
            proj = Project.objects.get(id=request.POST['proj_select'])
            EmployeeProjectMapping.objects.create(
                employee=emp,
                project=proj,
                role=request.POST['role']
            )
        return redirect('dashboard')

    # Fetch data to populate the "Assign" dropdowns
    employees = Employee.objects.all()
    projects = Project.objects.all()
    return render(request, 'generator/dashboard.html', {
        'employees': employees,
        'projects': projects
    })


def delete_employee(request, emp_id):
    """Delete an employee"""
    employee = get_object_or_404(Employee, id=emp_id)
    employee.delete()
    return redirect('dashboard')


def generate_resume(request):
    """Generate and display/download resume"""
    query = request.GET.get('query', '')
    action = request.GET.get('action', 'view')  # Default to view
    
    # Search by name or employee ID
    employee = Employee.objects.filter(name__icontains=query).first() or \
               Employee.objects.filter(emp_id=query).first()

    if not employee:
        return HttpResponse("<h2>Employee Not Found</h2><a href='/'>Go Back</a>")

    # Get mapped projects
    projects = EmployeeProjectMapping.objects.filter(employee=employee)
    context = {'emp': employee, 'projects': projects}

    # If user clicks "View", show the HTML page
    if action == 'view':
        return render(request, 'generator/resume_template.html', context)

    # If user clicks "Download", generate the PDF
    template = get_template('generator/resume_template.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{employee.name}_Resume.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF: <pre>' + html + '</pre>')
    return response

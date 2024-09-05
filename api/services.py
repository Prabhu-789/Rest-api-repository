# service.py
from rest_framework.exceptions import ValidationError,NotFound
from .models import Student
from .serializers import StudentSerializer

class StudentService:
    """
    Service layer for handling business logic related to Students.
    """
    
    def __init__(self):
        self.queryset = Student.objects.all()

    def create_student(self, data):
        """
        Creates a student using the provided data.
        """
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            student = serializer.save()
            return student
        else:
            # Validation failed, raise an exception with the validation errors
            raise ValidationError(serializer.errors)
        
    def get_all_students(self):
        """
        Retrieves a list of all students.
        """
        students = self.queryset
        serializer = StudentSerializer(students, many=True)
        return serializer.data
    
    def delete_student(self, student_id):
        """
        Deletes a student by ID and returns the deleted student data.
        """
        try:
            student = self.queryset.get(id=student_id)
            serializer = StudentSerializer(student)
            student_data = serializer.data  # Capture the student data before deletion
            student.delete()
            return student_data
        except Student.DoesNotExist:
            raise NotFound(f"Student with ID {student_id} does not exist.")
        
    def retrieve_student(self, student_id):
        """
        Retrieves a student by ID.
        """
        try:
            student = self.queryset.get(id=student_id)
            serializer = StudentSerializer(student)
            return serializer.data
        except Student.DoesNotExist:
            raise NotFound(f"Student with ID {student_id} does not exist.")
    
    def update_student(self, student_id, data):
        """
        Updates a student by ID using the provided data.
        """
        try:
            student = self.queryset.get(id=student_id)
            serializer = StudentSerializer(student, data=data, partial=True)
            if serializer.is_valid():
                updated_student = serializer.save()
                return updated_student
            else:
                raise ValidationError(serializer.errors)
        except Student.DoesNotExist:
            raise NotFound(f"Student with ID {student_id} does not exist.")
        
    def search_students(self, search_params):
        """
        Search students based on name, roll, or city with sorting and pagination.
        """
        # Construct filter conditions dynamically based on input
        filters = {
            'name__icontains': search_params.get('name', ''),
            'roll': search_params.get('roll'),
            'city__icontains': search_params.get('city', '')
        }

        # Remove None filters
        filters = {k: v for k, v in filters.items() if v is not None}

        # Perform search with filters if provided
        students = Student.objects.filter(**filters)

        # Apply ordering if specified, defaults to 'name'
        ordering = search_params.get('ordering', 'name')
        students = students.order_by(ordering)

        return students

class StudentSearchService:
    """
    Service layer for handling search, sorting, and pagination for Students.
    """
    def search_students(self, params):
        """
        Search students dynamically based on query parameters.

        :param params: dict of query parameters including filters, sorting, and pagination.
        :return: Queryset of filtered, sorted, and paginated students.
        """
        # Extract query parameters
        name = params.get('name', '')
        roll = params.get('roll', None)
        city = params.get('city', '')
        sort_by = params.get('sortBy', 'name')  # default sort field
        sort_order = params.get('sortOrder', 'asc').lower()  # default to ascending
        page = int(params.get('page', 1))
        page_size = int(params.get('pageSize', 20))

        # Construct filter conditions dynamically based on input
        filters = {
            'name__icontains': name,
            'city__icontains': city
        }
        if roll is not None:
            filters['roll'] = roll

        # Remove empty filters
        filters = {k: v for k, v in filters.items() if v}

        # Get the queryset with filters applied
        students = Student.objects.filter(**filters)

        # Apply sorting
        ordering = f"-{sort_by}" if sort_order == 'desc' else sort_by
        students = students.order_by(ordering)

        # Paginate the results
        offset = (page - 1) * page_size
        paginated_students = students[offset:offset + page_size]

        return paginated_students, students.count()  # return the queryset and the total count
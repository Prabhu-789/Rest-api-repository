from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, \
    RetrieveUpdateDestroyAPIView
from .models import Student
from .serializers import StudentSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .pagination import CustomLimitOffsetPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView
from .services import StudentService,StudentSearchService
from rest_framework.exceptions import ValidationError,NotFound

class StudentList(ListAPIView):
    """
    View to retrieve a list of all students.
    """
    serializer_class = StudentSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.student_service = StudentService()

    def get_queryset(self):
        # Correctly define the queryset
        return self.student_service.queryset

    @swagger_auto_schema(operation_description="Retrieve a list of all the students present in the table")
    def get(self, request, *args, **kwargs):
        students = self.student_service.get_all_students()
        return Response(students, status=status.HTTP_200_OK)


class StudentCreate(CreateAPIView):
    """
    View to create a new student entry.
    """
    serializer_class = StudentSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.student_service = StudentService()

    @swagger_auto_schema(
        operation_description="Create a new student entry in GVP College of Engineering",
        tags=['Students_Create'],
        request_body=StudentSerializer,
        responses={201: StudentSerializer, 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        try:
            student = self.student_service.create_student(request.data)
            return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class StudentRetrieve(RetrieveAPIView):
    """
    View to retrieve details of a specific student by ID.
    """

    serializer_class = StudentSerializer  # Define the serializer class

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.student_service = StudentService()

    def get_queryset(self):
        # This method is required by DRF's RetrieveAPIView, but we override the actual retrieval.
        return self.student_service.queryset

    @swagger_auto_schema(operation_description="Retrieve details of a specific student by ID")
    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('pk')
        try:
            student_data = self.student_service.retrieve_student(student_id)
            return Response(student_data, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

class StudentUpdate(APIView):
    """
    View to update a student entry by ID.
    """
    serializer_class = StudentSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.student_service = StudentService()

    @swagger_auto_schema(
        operation_description="Update a student entry by ID",
        tags=['Students_Update'],
        request_body=StudentSerializer,
        responses={200: StudentSerializer, 400: 'Bad Request', 404: 'Not Found'}
    )
    def put(self, request, *args, **kwargs):
        student_id = kwargs.get('pk')
        try:
            updated_student = self.student_service.update_student(student_id, request.data)
            return Response(StudentSerializer(updated_student).data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)


class StudentDestroy(DestroyAPIView):
    """
    View to delete a specific student by ID.
    """

    serializer_class = StudentSerializer  # Define the serializer class

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.student_service = StudentService()

    def get_queryset(self):
        # Define the queryset attribute required by DRF's DestroyAPIView
        return self.student_service.queryset

    @swagger_auto_schema(operation_description="Delete a specific student by ID")
    def delete(self, request, *args, **kwargs):
        student_id = kwargs.get('pk')
        try:
            deleted_student = self.student_service.delete_student(student_id)
            return Response(deleted_student, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
    
# class StudentListCreate(ListCreateAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     # filter_backends = [SearchFilter]  # Adding SearchFilter for search functionality
#     # search_fields = ['name', 'city','roll']  # Specify fields that are searchable

#     # @swagger_auto_schema(
#     #     operation_description="Retrieve a list of all students or create a new student entry",
#     #     manual_parameters=[
#     #         openapi.Parameter(
#     #             'search',
#     #             openapi.IN_QUERY,
#     #             description="Search by name or city",
#     #             type=openapi.TYPE_STRING
#     #         ),
#     #         openapi.Parameter(
#     #             'page',
#     #             openapi.IN_QUERY,
#     #             description="Page number for pagination",
#     #             type=openapi.TYPE_INTEGER
#     #         )
#     #     ]
#     # )
#     def get(self, request, *args, **kwargs):
#         # Handles GET requests with optional search functionality
#         return super().get(request, *args, **kwargs)

#     @swagger_auto_schema(
#         operation_description="Create a new student entry or search for students dynamically",
#         responses={201: StudentSerializer, 400: 'Bad Request'},
#     )
#     # @swagger_auto_schema(operation_description="Create a new student entry")
#     def post(self, request, *args, **kwargs):
#         # Handles POST requests for creating new student records
#         return super().post(request, *args, **kwargs)
    

# class StudentRetrieveUpdate(RetrieveUpdateAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

#     @swagger_auto_schema(operation_description="Retrieve and update details of a specific student by ID")
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)

#     @swagger_auto_schema(operation_description="Update details of a specific student by ID")
#     def put(self, request, *args, **kwargs):
#         return super().put(request, *args, **kwargs)

# class StudentRetrieveDestroy(RetrieveDestroyAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

#     @swagger_auto_schema(operation_description="Retrieve and delete a specific student by ID")
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)

#     @swagger_auto_schema(operation_description="Delete a specific student by ID")
#     def delete(self, request, *args, **kwargs):
#         return super().delete(request, *args, **kwargs)

# class StudentRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

#     @swagger_auto_schema(operation_description="Retrieve, update, or delete a specific student by ID")
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)

#     @swagger_auto_schema(operation_description="Update details of a specific student by ID")
#     def put(self, request, *args, **kwargs):
#         return super().put(request, *args, **kwargs)

#     @swagger_auto_schema(operation_description="Delete a specific student by ID")
#     def delete(self, request, *args, **kwargs):
#         return super().delete(request, *args, **kwargs)


class StudentSearchView(APIView):
    """
    View to search, sort, and paginate students based on various query parameters using POST method.
    """
    student_search_service = StudentSearchService()

    # Define the query parameters for Swagger UI
    page_param = openapi.Parameter(
        'page', openapi.IN_QUERY, description="Page number for pagination", type=openapi.TYPE_INTEGER, default=1
    )
    page_size_param = openapi.Parameter(
        'pageSize', openapi.IN_QUERY, description="Number of results per page", type=openapi.TYPE_INTEGER, default=20
    )
    sort_by_param = openapi.Parameter(
        'sortBy', openapi.IN_QUERY, description="Field to sort by (e.g., name, roll, city)", type=openapi.TYPE_STRING, default='name'
    )
    sort_order_param = openapi.Parameter(
        'sortOrder', openapi.IN_QUERY, description="Sort order ('asc' or 'desc')", type=openapi.TYPE_STRING, default='asc'
    )

    @swagger_auto_schema(
        operation_description="Search for students dynamically based on name, roll, or city with sorting and pagination.",
        manual_parameters=[page_param, page_size_param, sort_by_param, sort_order_param],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Search by student name'),
                'roll': openapi.Schema(type=openapi.TYPE_INTEGER, description='Search by roll number'),
                'city': openapi.Schema(type=openapi.TYPE_STRING, description='Search by city name'),
            },
            required=[]
        ),
        responses={200: StudentSerializer(many=True), 400: 'Bad Request'},
        tags=['Students_Search']
    )
    def post(self, request, *args, **kwargs):
        # Retrieve pagination and sorting parameters from query params
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('pageSize', 20))
        sort_by = request.query_params.get('sortBy', 'name')
        sort_order = request.query_params.get('sortOrder', 'asc')

        # Retrieve the search parameters from the request body
        search_params = request.data

        # Prepare parameters to be passed to the service
        search_params.update({
            'page': page,
            'pageSize': page_size,
            'sortBy': sort_by,
            'sortOrder': sort_order,
        })

        # Use the service to get the filtered, sorted, and paginated students
        students, total_count = self.student_search_service.search_students(search_params)

        # Serialize the paginated students
        serializer = StudentSerializer(students, many=True)

        # Construct the response with pagination details
        response_data = {
            'total_count': total_count,
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
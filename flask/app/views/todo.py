from flask import request
from flask_restx import Namespace, Resource
from app.helpers.response import get_success_response, parse_request_body, validate_required_fields
from app.helpers.decorators import login_required
from common.services.todo import TodoService
from common.app_config import config
from common.app_logger import logger

# Create the todo blueprint
todo_api = Namespace('todo', description="Todo-related APIs")

todo_service = TodoService(config)


@todo_api.route('/')
class TodoList(Resource):

    @login_required()
    def get(self, person):
        todos = todo_service.get_all_todos_by_person_id(person.entity_id)
        return get_success_response(todos=[todo.as_dict() for todo in todos])

    @login_required()
    @todo_api.expect({
        'type': 'object',
        'properties': {
            'title': {'type': 'string'},
        },
        'required': ['title']
    })
    def post(self, person):
        parsed_body = parse_request_body(request, ['title'])
        validate_required_fields(parsed_body)

        todo = todo_service.save_todo(
            person_id=person.entity_id,
            title=parsed_body['title']
        )

        return get_success_response(message="Todo created successfully.", todo=todo.as_dict())


@todo_api.route('/<string:todo_id>')
class TodoItem(Resource):

    @login_required()
    def patch(self, todo_id):
        logger.info(todo_id)
        parsed_body = parse_request_body(request, ['title', 'is_completed'])
        validate_required_fields(parsed_body)
        todo = todo_service.update_todo(todo_id, 
                                        parsed_body['title'],
                                        parsed_body['is_completed'])
        return get_success_response(message="Todo updated successfully.", todo=todo.as_dict())

    @login_required()
    def delete(self, todo_id):
        print(f"ID : {todo_id}")
        todo_service.delete_todo(todo_id)
        return get_success_response(message="Todo deleted successfully.")


@todo_api.route('/clear-completed')
class ClearCompleted(Resource):
    @login_required()
    def delete(self, person):
        todo_service.delete_completed_todos(person.entity_id)
        return get_success_response(message="Completed todos cleared.")
    
class FilteredTodoBase(Resource):
    filter_type = None

    @login_required()
    def get(self, person):
        if self.filter_type == "active":
            todos = todo_service.get_active_todos(person.entity_id)
        elif self.filter_type == "completed":
            todos = todo_service.get_completed_todos(person.entity_id)
        else:
            todos = []
        return get_success_response(todos=[todo.as_dict() for todo in todos])

@todo_api.route('/active')
class ActiveTodos(FilteredTodoBase):
    filter_type = "active"

@todo_api.route('/completed')
class CompletedTodos(FilteredTodoBase):
    filter_type = "completed"